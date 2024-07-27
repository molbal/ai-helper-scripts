## Description to tags
### Overview
This script processes text files in a specified directory, rewriting their descriptions into a tag-based format using a local language model. The script takes three command-line arguments: the directory containing the text files, the name of the language model, and a file containing few-shot examples.

### High-Level Functionality
1. **Read few-shot examples**: The script reads examples from a specified file to understand how descriptions should be rewritten.
2. **Process each file**: For each text file in the specified directory, the script reads the original content, sends it to the language model along with the few-shot examples, and receives a rewritten description.
3. **Overwrite files**: The original content of each file is replaced with the rewritten description.

### Dependencies
To run the script, you need to install the following dependencies:

1. **tqdm**: Used for displaying a progress bar.
2. **ollama**: Client library for interacting with local language models.

Install them using pip:
```sh
pip install tqdm ollama
```


### CLI Parameters

| Parameter           | Description                                    | Example                                    | Default                                    |
|---------------------|------------------------------------------------|--------------------------------------------|:-------------------------------------------|
| `<directory>`       | Path to the directory containing text files.   | `C:\tools\training\illustration_pending`   | -                                          |
| `--model_name`    | Name of the language model to use.             | `llama3:8b-instruct-q6_K`                  | `llama3`                                   |
| `--examples_file` | Path to the file containing few-shot examples. | `prompts/description-to-tags-examples.txt` | `prompts/description-to-tags-examples.txt` |

### Usage

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

