import json
import os
import time
import argparse
import subprocess
from tqdm import tqdm
import ollama
from comfy_api_simplified import ComfyApiWrapper, ComfyWorkflowWrapper


def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate and process image prompts.')
    parser.add_argument('--count', type=int, default=50, help='Number of images to generate.')
    parser.add_argument('--workflow', type=str, default='workflows/workflow-cartoon.json', help='Path to the workflow file.')
    parser.add_argument('--example_prompts', type=str, default='prompts/example-cartoon.txt', help='Path to the file containing example prompts.')
    parser.add_argument('--prompt_file', type=str, default='prompts/llm-json-prompt.txt', help='Path to the prompt template file.')
    parser.add_argument('--style', type=str, default='base', help='Style to use.')
    parser.add_argument('--outdir', type=str, default='output', help='Output directory to save images to.')
    parser.add_argument('--llm', type=str, default='gemma2', help='LLM to generate prompts.')
    parser.add_argument('--prompt_prefix', type=str, default='<lora:Childrens_book_illustration_v2.1.safetensors:1.0> childrens_book_illustration', help='Prefix for prompts. Good for LoRA and trigger words.')
    parser.add_argument('--kill_processes', action='store_true', help='Kill ollama processes after generating prompts.')
    parser.add_argument('--save_prompt_txt', action='store_true', help='If yes, saves prompt text next to the picture.')
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
    prompt = prompt_template.format(example=example_prompts, n=n)

    for i in range(5):
        response = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0.8}
        )

        content = response['message']['content']
        prompts = [line.strip() for line in content.split('\n') if line.strip()]  # split by newline and strip whitespace

        if prompts:
            prompt_list = [prompt_prefix + p for p in prompts]
            return prompt_list
        else:
            print(f"No prompts found in response (attempt {i+1}/5): {content}")

        if i == 4:
            return []  # give up after 5 attempts
        else:
            continue  # try again


def kill_ollama_processes():
    processes_to_kill = ['ollama.exe', 'ollama_llama_server.exe']
    for process in processes_to_kill:
        try:
            subprocess.run(['taskkill', '/IM', process, '/F'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error killing process {process}: {e}")


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

    # Generate prompts
    print("Generating prompts...")
    prompt_list = generate_prompts(prompt_template, example_prompts, args.count, args.prompt_prefix, args.llm)
    for prompt in prompt_list:
        print(prompt)

    # Optionally kill ollama processes
    if args.kill_processes:
        print("Killing ollama processes...")
        kill_ollama_processes()

    api = ComfyApiWrapper("http://127.0.0.1:8188/")
    wf = ComfyWorkflowWrapper(args.workflow)
    for prompt in tqdm(prompt_list, desc='Generating images', unit='image'):
        try:
            wf.set_node_param("SDXL Prompt Styler", "text_positive", prompt)
            results = api.queue_and_wait_images(wf, output_node_title="Image Save with Prompt (WLSH)")
            for filename, image_data in results.items():
                current_time = int(time.time())
                output_image_path = f"{args.outdir}/{current_time}-{args.style}.png"
                with open(output_image_path, "wb") as f:
                    f.write(image_data)
                if args.save_prompt_txt:
                    with open(f"{args.outdir}/{current_time}-{args.style}.txt", "w") as f:
                        f.write(prompt)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
