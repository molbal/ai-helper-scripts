### Batch Generate

#### Overview
The `batch-generate.py` script automates the process of generating image prompts and creating images based on these prompts. It integrates a local language model for prompt generation and uses a workflow to generate images, saving them to a specified directory.

#### High-Level Functionality
1. **Parse arguments**: The script accepts several command-line arguments to configure the prompt generation and image creation process.
2. **Load files**: Reads the workflow file, example prompts, and prompt template from specified paths.
3. **Generate prompts**: Uses a local language model to generate a specified number of image prompts based on example prompts and a template.
4. **Create images**: Runs a workflow to generate images from the generated prompts, saving the images and optionally the prompts.
5. **Optional cleanup**: Can kill specific processes related to the language model after generating prompts.

#### Dependencies
Ensure the following dependencies are installed before running the script:

- Python 3.6 or higher
- `tqdm` for progress bars
- `ollama` for local language model interaction
- `comfy_api_simplified` for workflow execution
- `websockets` for API communication

Install them using pip:
```sh
pip install tqdm ollama comfy_api_simplified websockets
```

#### CLI Parameters

| Parameter           | Description                                                                                           | Default                                                                               | Example Usage                                                               |
|---------------------|-------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| `--count`           | Number of images to generate.                                                                         | 50                                                                                    | `python batch-generate.py --count 100`                                      |
| `--workflow`        | Path to the workflow file.                                                                            | `workflows/workflow-cartoon.json`                                                     | `python batch-generate.py --workflow workflows/custom-workflow.json`        |
| `--example_prompts` | Path to the file containing example prompts.                                                          | `prompts/example-cartoon.txt`                                                         | `python batch-generate.py --example_prompts prompts/my-example-prompts.txt` |
| `--prompt_file`     | Path to the prompt template file.                                                                     | `prompts/llm-json-prompt.txt`                                                         | `python batch-generate.py --prompt_file prompts/custom-prompt.txt`          |
| `--style`           | Style to use for generating images.                                                                   | `base`                                                                                | `python batch-generate.py --style anime`                                    |
| `--outdir`          | Output directory to save images to.                                                                   | `output`                                                                              | `python batch-generate.py --outdir /path/to/output`                         |
| `--llm`             | Local language model to generate prompts.                                                             | `gemma2`                                                                              | `python batch-generate.py --llm my-local-model`                             |
| `--prompt_prefix`   | Prefix for prompts, useful for LoRA and trigger words.                                                | `<lora:Childrens_book_illustration_v2.1.safetensors:1.0> childrens_book_illustration` | `python batch-generate.py --prompt_prefix '<lora:MyStyle.safetensors:1.0>'` |
| `--kill_processes`  | Kill specific processes after generating prompts.                                                     | N/A                                                                                   | `python batch-generate.py --kill_processes`                                 |
| `--save_prompt_txt` | Save the prompt text next to the generated image.                                                     | N/A                                                                                   | `python batch-generate.py --save_prompt_txt`                                |
| `--run_examples`    | If this flag is set, then the example prompt will run first.  These do not count in the --count value | `true`                                                                                | `python batch-generate.py --run_examples`                                   |

#### Usage

To use this script, run it from the command line with the appropriate parameters:

```sh
python ./inference/batch-generate.py --count=<number_of_images> --workflow=<workflow_file> --example_prompts=<example_prompts_file> --prompt_file=<prompt_template_file> --style=<image_style> --outdir=<output_directory> --llm=<local_language_model> --prompt_prefix=<prompt_prefix> [--kill_processes] [--save_prompt_txt]
```

Some examples:
```sh
python ./inference/batch-generate.py --kill_processes --save_prompt_txt --count 30 --outdir=output/2024-07-20 --llm llama3:8b-instruct-q6_K
python ./inference/batch-generate.py --kill_processes --run_examples --count 10 --outdir=output/2024-07-21/apocalyptic --llm llama3:8b-instruct-q6_K --style=sai-photographic --workflow workflows/workflow-ultrawide-apoc.json --example_prompts prompts/example-apoc.txt --prompt_prefix "<lora:Apocalyptic:1.5> <lora:add-detail-xl.safetensors:1.8> apocalyptic, 32k UHD resolution, RAW, best quality, ultrawide"
python ./inference/batch-generate.py --kill_processes --clean_comfy_vram --save_prompt_txt --count 25 --outdir=output/2024-08-07/flux --llm llama3.1:8b-instruct-q5_1 --workflow workflows/workflow-flex.json --example_prompts prompts/example-flux.txt --prompt_prefix " "
python ./inference/batch-generate.py --kill_processes --count 30 --outdir=output/2024-07-24/apocalyptic --llm llama3.1:8b-instruct-q5_1 --style="sai-digital art" --workflow workflows/workflow-ultrawide-apoc-v2.json --example_prompts prompts/example-apoc.txt --prompt_prefix "<lora:Apocalyptic-v2-albedobase.safetensors:0.65> <lora:add-detail-xl.safetensors:1.2>,  apocalyptic "
```

#### Notes
- The script supports various image generation workflows by specifying different workflow files.
- The script will create the output directory if it does not exist.
- If the `--kill_processes` flag is used, the script will attempt to terminate Ollama processes related to the language model after generating prompts, to free up VRAM to load other models
- The script will look for 'KSampler (Advanced) - BASE' titled node and attempt to set its seed to a random number each iteration

