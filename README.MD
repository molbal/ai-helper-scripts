# AI Helper Scripts

A collection of scripts to aid in various tasks related to data preparation and inference.

## Overview

This repository contains a set of Python scripts designed to simplify and automate tasks such as data preparation, and image processing. These scripts are intended to be used as tools to help with the development and training of AI models.

## Scripts

The following scripts are included in this repository:

* `article.py`: Generates articles based on the style and content of provided Substack article URLs. [View Documentation](docs/article.md)
* `batch-generate.py`: Automates the process of generating image prompts and creating images based on these prompts. [View Documentation](docs/batch-generate.md)
* `description-to-tags.py`: Converts image descriptions to tags for use in image classification models. [View Documentation](docs/description-to-tags.md)
* `img-to-square.py`: Resizes images to a square shape while maintaining their aspect ratio. [View Documentation](docs/img-to-square.md)
* `upscale-dataset.py`: Upscales a dataset of images using a specified model. [View Documentation](docs/upscale-dataset.md)
* `vae-process.py`: Reencodes images using a Variational Autoencoder (VAE) model. [View Documentation](docs/vae-process.md)

## Requirements

* Python 3.6 or higher
* Various dependencies specific to each script (see documentation for details)
* The script assumes that you have Ollama and ComfyUI installed. ComfyUI should have developer mode enabled.

## Usage

To use these scripts, simply clone this repository and navigate to the directory containing the script you want to use. Run the script using Python, following the usage instructions in the documentation.

## License

These scripts are released under the MIT License. See the LICENSE file for details.
