import json
import os
import random
import time
import argparse
import subprocess
import requests
from tqdm import tqdm
import ollama
from comfy_api_simplified import ComfyApiWrapper, ComfyWorkflowWrapper


def clear_comfyui_gpu_usage():
    url = "http://127.0.0.1:8188/easyuse/cleangpu"
    headers = {
        "accept": "*/*",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,hu;q=0.7,nl;q=0.6",
        "comfy-user": "undefined",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"127\", \"Chromium\";v=\"127\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin"
    }
    try:
        response = requests.post(url, headers=headers)
    except Exception as e:
        print(f"Error while clearing ComfyUI VRAM: {e}")
    time.sleep(2)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate and process image prompts.')
    parser.add_argument('--count', type=int, default=50, help='Number of images to generate.')
    parser.add_argument('--workflow', type=str, default='workflows/workflow-cartoon.json',
                        help='Path to the workflow file.')
    parser.add_argument('--example_prompts', type=str, default='prompts/example-cartoon.txt',
                        help='Path to the file containing example prompts.')
    parser.add_argument('--prompt_file', type=str, default='prompts/llm-json-prompt.txt',
                        help='Path to the prompt template file.')
    parser.add_argument('--style', type=str, default='base', help='Style to use.')
    parser.add_argument('--outdir', type=str, default='output', help='Output directory to save images to.')
    parser.add_argument('--llm', type=str, default='gemma2', help='LLM to generate prompts.')
    parser.add_argument('--prompt_prefix', type=str,
                        default='<lora:Childrens_book_illustration_v2.1.safetensors:1> childrens_book_illustration ',
                        help='Prefix for prompts. Good for LoRA and trigger words.')
    parser.add_argument('--kill_processes', action='store_true', help='Kill ollama processes after generating prompts.')
    parser.add_argument('--clean_comfy_vram', action='store_true',
                        help='Attempts clearing VRAM used by ComfyUI before calling Ollama')
    parser.add_argument('--run_examples', action='store_true',
                        help='If set to true, examples from the --example_prompts file will be queued first. These do not count in the --count value')
    parser.add_argument('--save_prompt_txt', action='store_true', help='If set, saves prompt text next to the picture.')
    return parser.parse_args()


def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def save_prompts(file_path, prompts):
    with open(file_path, 'w') as f:
        for prompt in prompts:
            f.write(prompt + '\n')


def generate_prompts(prompt_template, example_prompts, n, prompt_prefix, model):
    prompt = prompt_template.format(example=example_prompts, n=max(n, 20))
    prompt_list = []
    past_prompts = []

    pbar = tqdm(total=n, desc='Generating prompts', unit='prompt')
    while len(prompt_list) < n:
        if past_prompts:
            recent_prompts = '\n'.join(past_prompts[-5:])  # get the last 5 prompts
            prompt = prompt_template.format(example=example_prompts + '\n' + recent_prompts, n=max(n, 12))
        stream = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0.8},
            stream=True
        )

        response = ""
        for chunk in stream:
            response += chunk['message']['content']
            if response.endswith('\n'):
                new_prompt = response.replace('\n', '').strip()
                pbar.update(1)
                prompt_list.append(prompt_prefix + " " + new_prompt)
                past_prompts.append(new_prompt)
                response = ""
            if len(prompt_list) >= n:
                break

    return prompt_list[:n]  # Just in case


def kill_ollama_processes():
    processes_to_kill = ['ollama.exe', 'ollama_llama_server.exe']
    for process in processes_to_kill:
        try:
            subprocess.run(['taskkill', '/IM', process, '/F'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error killing process {process}: {e}")


def generate_image(wf, args, api, prompt):
    try:
        try:
            wf.set_node_param("SDXL Prompt Styler", "text_positive", prompt)
            wf.set_node_param("SDXL Prompt Styler", "prompt", prompt)
        except Exception as e:
            print(f"Error setting prompt: {e}")
        try:
            wf.set_node_param("KSampler (Advanced) - BASE", "noise_seed", random.randint(0, 1024 * 1024))
        except Exception as e:
            pass

        results = api.queue_and_wait_images(wf, output_node_title="SaveImage")
        for filename, image_data in results.items():
            current_time = int(time.time())
            output_image_path = f"{args.outdir}/{current_time}-{args.style}.png"
            with open(output_image_path, "wb") as f:
                f.write(image_data)
            if args.save_prompt_txt:
                with open(f"{args.outdir}/{current_time}-{args.style}.txt", "w") as f:
                    f.write(prompt)
    except Exception as e:
        print(f"⚠️ Could not generate prompt {prompt}: error: {e}")


def main():
    args = parse_arguments()

    # Create output directory
    if not os.path.exists(args.outdir):
        print(f"Creating output directory {args.outdir}")
        os.makedirs(args.outdir)

    # Load files
    print("Loading workflow...")
    prompt_template = load_text_file(args.prompt_file)
    example_prompts = load_text_file(args.example_prompts)

    # Optionally kill ollama processes
    if args.clean_comfy_vram:
        print("Freeing VRAM...")
        clear_comfyui_gpu_usage()

    # Generate prompts
    prompt_list = generate_prompts(prompt_template, example_prompts, args.count, args.prompt_prefix, args.llm)
    for prompt in prompt_list:
        print(prompt)

    # Optionally kill ollama processes
    if args.kill_processes:
        print("Killing ollama processes...")
        kill_ollama_processes()

    api = ComfyApiWrapper("http://127.0.0.1:8188/")
    wf = ComfyWorkflowWrapper(args.workflow)

    if args.run_examples:
        for prompt in tqdm(example_prompts.split('\n'), desc='Generating examples', unit='image'):
            generate_image(wf, args, api, prompt)

    for prompt in tqdm(prompt_list, desc='Generating images', unit='image'):
        generate_image(wf, args, api, prompt)


if __name__ == '__main__':
    main()
