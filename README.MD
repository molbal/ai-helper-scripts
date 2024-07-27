# AI Helper Scripts

A collection of scripts to aid in various tasks related to AI model training and data preparation.

## Overview

This repository contains a set of Python scripts designed to simplify and automate tasks such as data preparation, model training, and image processing. These scripts are intended to be used as tools to help with the development and training of AI models.

## Scripts

The following scripts are included in this repository:

| Script                   | Description                                                                                   | Documentation                                     |
|--------------------------|-----------------------------------------------------------------------------------------------|---------------------------------------------------|
| `article.py`             | Generates articles based on the style and content of provided Substack article URLs.          | [View Documentation](docs/article.md)             |
| `batch-generate.py`      | Automates the process of generating image prompts and creating images based on these prompts. | [View Documentation](docs/batch-generate.md)      |
| `description-to-tags.py` | Converts image descriptions to tags for use in image classification models.                   | [View Documentation](docs/description-to-tags.md) |
| `img-to-square.py`       | Resizes images to a square shape while maintaining their aspect ratio.                        | [View Documentation](docs/img-to-square.md)       |
| `upscale-dataset.py`     | Upscales a dataset of images using a specified model.                                         | [View Documentation](docs/upscale-dataset.md)     |
| `vae-process.py`         | Reencodes images using a Variational Autoencoder (VAE) model.                                 | [View Documentation](docs/vae-process.md)         |

## Requirements

* Python 3.6 or higher
* Various dependencies specific to each script (see documentation for details)

## Usage

To use these scripts, simply clone this repository and navigate to the directory containing the script you want to use. Run the script using Python, following the usage instructions in the documentation.

## Contributing

Contributions are welcome! If you have a script that you think would be useful to others, feel free to submit a pull request.

## License

These scripts are released under the MIT License. See the LICENSE file for details.

## Author

* [molbal](https://github.com/molbal)