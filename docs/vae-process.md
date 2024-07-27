## VAE Processing

### Overview

The `vae-process.py` script is designed to process images in a specified directory by reencoding them with a Variational Autoencoder (VAE) model. This is useful for creating training data for an Enhanced Super-Resolution Generative Adversarial Network (ESRGAN) model.

### High-Level Functionality

1. **List images**: Scans the specified directory for images (png or jpg) and creates a list of files to process.
2. **VAE passthrough**: Copies each image to the ComfyUI input directory, sets the image as input for the VAE workflow, and queues the workflow for processing. The resulting reencoded image is then saved to the original directory with a "vae-" prefix.

### Dependencies

Ensure the following dependencies are installed before running the script:

- Python 3.6 or higher
- `tqdm` for progress bars
- `PIL` for image processing
- `comfy_api_simplified` for interacting with the ComfyUI API

Install them using pip:
```sh
pip install tqdm pillow comfy_api_simplified
```

### CLI Parameters

| Parameter | Description | Example |
| --- | --- | --- |
| `directory` | The directory to list images from and process | `/path/to/images` |

### Usage

To use this script, run it from the command line with the directory path as an argument:
```sh
python data-prep/vae-process.py /path/to/images
```
Replace `/path/to/images` with the actual path to the directory containing the images you want to process.

### Notes

- The script assumes that the ComfyUI API is running on `http://127.0.0.1:8188/` and that the VAE workflow is defined in `./workflows/vae-reencode.json`.
- The script will overwrite any existing files with the same name in the original directory.
- The script will print a progress bar while scanning the directory and processing images.

### Workflow Requirements

The VAE workflow should be defined in a JSON file (e.g., `workflows/vae-reencode.json`) and should contain the following nodes:

* `Load Image`: Loads the input image from the ComfyUI input directory.
* `Save Image`: Saves the reencoded image to the output directory.

The workflow should be configured to take the input image from the `Load Image` node and pass it through the VAE model, then save the resulting reencoded image to the `Save Image` node.