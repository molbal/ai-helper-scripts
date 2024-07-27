# molbal's collection of image genai scrips

## Training related scripts
### Upscale
The script is designed to upscale images within a specified directory that have dimensions 
smaller than or equal to a given size. It leverages the ComfyUI backend and two separate
upscale models to achieve this. 

#### Dependencies

The script requires several Python libraries: tqdm, Pillow, comfy_api_simplified, and websockets.
```sh
pip install tqdm Pillow comfy_api_simplified websockets
```

#### Usage

```sh
python ./data-prep/upscale-dataset.py /path/to/your/directory --max-size 256
```

#### CLI Parameters

| Flag         | Type | Description                                                                                                                                   | Default | Example Usage                                                                  |
|--------------|------|-----------------------------------------------------------------------------------------------------------------------------------------------|---------|--------------------------------------------------------------------------------|
| `directory`  | str  | The path to the directory containing the images you want to upscale.                                                                          | N/A     | `python ./data-prep/upscale-dataset.py /path/to/your/directory`                |
| `--max-size` | int  | The maximum size of the smaller dimension of the images. Images with either width or height less than or equal to this size will be upscaled. | 256     | `python ./data-prep/upscale-dataset.py /path/to/your/directory --max-size 512` |

### Description to tags
#### Overview
This script processes text files in a specified directory, rewriting their descriptions into a tag-based format using a local language model. The script takes three command-line arguments: the directory containing the text files, the name of the language model, and a file containing few-shot examples.

#### High-Level Functionality
1. **Read few-shot examples**: The script reads examples from a specified file to understand how descriptions should be rewritten.
2. **Process each file**: For each text file in the specified directory, the script reads the original content, sends it to the language model along with the few-shot examples, and receives a rewritten description.
3. **Overwrite files**: The original content of each file is replaced with the rewritten description.

#### Dependencies
To run the script, you need to install the following dependencies:

1. **tqdm**: Used for displaying a progress bar.
2. **ollama**: Client library for interacting with local language models.

Install them using pip:
```sh
pip install tqdm ollama
```


#### CLI Parameters

| Parameter           | Description                                    | Example                                    | Default                                    |
|---------------------|------------------------------------------------|--------------------------------------------|:-------------------------------------------|
| `<directory>`       | Path to the directory containing text files.   | `C:\tools\training\illustration_pending`   | -                                          |
| `--model_name`    | Name of the language model to use.             | `llama3:8b-instruct-q6_K`                  | `llama3`                                   |
| `--examples_file` | Path to the file containing few-shot examples. | `prompts/description-to-tags-examples.txt` | `prompts/description-to-tags-examples.txt` |

#### Usage

Use the command line to run the script, providing the required arguments:
```sh
python data-prep/description-to-tags.py <directory> --model_name=<model_name> --examples_file=<examples_file>
```

- `<directory>`: Path to the directory containing text files.
- `--model_name`: Name of the language model to use. I have 8GB of VRAM, and for me Q6 Llama3 works well. For people with lower VRAM, Phi3 mini is recommended as it still follows instructions well.
- `--examples_file`: Path to the file containing few-shot examples.

Example:
```sh
python data-prep/description-to-tags.py D:\ML\training\pending --model_name=llama3:8b-instruct-q6_K
```


### Padding to square

#### Overview

This script resizes images so that their height or width does not exceed a specified maximum size. It also pads the images to be square, filling the background with white. The script overwrites the original images with the processed images.

#### Dependencies

Ensure the following dependencies are installed before running the script:
- Python 3.6 or higher
- Pillow library for image processing

```sh
pip install pillow
```

#### Usage

To use this script, run it from the command line with the appropriate parameters. The script processes all images in the specified directory, resizing and padding them as needed, and overwrites the original images.

##### Command-Line Parameters

| Parameter         | Description                                              | Example                    |
|-------------------|----------------------------------------------------------|----------------------------|
| `input_directory` | Directory containing images to process.                  | `/path/to/input_directory` |
| `max_size`        | Maximum dimension (width or height) for resizing images. | `1536`                     |

##### Example Command

```bash
python data-prep/img-to-square.py D:\ML\training\illustration-square 1536
```

Replace `/path/to/input_directory` with the path to your directory containing images. The script will resize and pad all images in that directory, overwriting the original images.

### Notes

- `png`, `jpg`, `jpeg`, `bmp`, and `gif` files will be processed.
- The script will overwrite the original images with the processed versions.
- If the specified input directory does not exist, the script will terminate with an error message.

## Inference related scripts 

## Inference related scripts 

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

| Parameter           | Description                                            | Default                                                                               | Example Usage                                                               |
|---------------------|--------------------------------------------------------|---------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| `--count`           | Number of images to generate.                          | 50                                                                                    | `python batch-generate.py --count 100`                                      |
| `--workflow`        | Path to the workflow file.                             | `workflows/workflow-cartoon.json`                                                     | `python batch-generate.py --workflow workflows/custom-workflow.json`        |
| `--example_prompts` | Path to the file containing example prompts.           | `prompts/example-cartoon.txt`                                                         | `python batch-generate.py --example_prompts prompts/my-example-prompts.txt` |
| `--prompt_file`     | Path to the prompt template file.                      | `prompts/llm-json-prompt.txt`                                                         | `python batch-generate.py --prompt_file prompts/custom-prompt.txt`          |
| `--style`           | Style to use for generating images.                    | `base`                                                                                | `python batch-generate.py --style anime`                                    |
| `--outdir`          | Output directory to save images to.                    | `output`                                                                              | `python batch-generate.py --outdir /path/to/output`                         |
| `--llm`             | Local language model to generate prompts.              | `gemma2`                                                                              | `python batch-generate.py --llm my-local-model`                             |
| `--prompt_prefix`   | Prefix for prompts, useful for LoRA and trigger words. | `<lora:Childrens_book_illustration_v2.1.safetensors:1.0> childrens_book_illustration` | `python batch-generate.py --prompt_prefix '<lora:MyStyle.safetensors:1.0>'` |
| `--kill_processes`  | Kill specific processes after generating prompts.      | N/A                                                                                   | `python batch-generate.py --kill_processes`                                 |
| `--save_prompt_txt` | Save the prompt text next to the generated image.      | N/A                                                                                   | `python batch-generate.py --save_prompt_txt`                                |

#### Usage

To use this script, run it from the command line with the appropriate parameters:

```sh
python ./inference/batch-generate.py --count=<number_of_images> --workflow=<workflow_file> --example_prompts=<example_prompts_file> --prompt_file=<prompt_template_file> --style=<image_style> --outdir=<output_directory> --llm=<local_language_model> --prompt_prefix=<prompt_prefix> [--kill_processes] [--save_prompt_txt]
```

Some examples:
```sh
python ./inference/batch-generate.py --kill_processes --save_prompt_txt --count 30 --outdir=output/2024-07-20 --llm llama3:8b-instruct-q6_K
python ./inference/batch-generate.py --kill_processes --save_prompt_txt --count 5 --outdir=output/2024-07-21/apocalyptic --llm llama3:8b-instruct-q6_K --style=sai-photographic --workflow workflows/workflow-ultrawide-apoc.json --example_prompts prompts/example-apoc.txt --prompt_prefix "<lora:Apocalyptic:1.5> <lora:add-detail-xl.safetensors:1.8> apocalyptic, 32k UHD resolution, RAW, best quality, ultrawide"
python ./inference/batch-generate.py --kill_processes --count 30 --outdir=output/2024-07-24/apocalyptic --llm llama3.1:8b-instruct-q5_1 --style="sai-digital art" --workflow workflows/workflow-ultrawide-apoc-v2.json --example_prompts prompts/example-apoc.txt --prompt_prefix "<lora:Apocalyptic-v2-albedobase.safetensors:0.65> <lora:add-detail-xl.safetensors:1.2>,  apocalyptic "
```

#### Notes
- The script supports various image generation workflows by specifying different workflow files.
- The script will create the output directory if it does not exist.
- If the `--kill_processes` flag is used, the script will attempt to terminate Ollama processes related to the language model after generating prompts, to free up VRAM to load other models
- The script will look for 'KSampler (Advanced) - BASE' titled node and attempt to set its seed to a random number each iteration
```
