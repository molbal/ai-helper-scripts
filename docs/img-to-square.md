## Padding to square

### Overview

This script resizes images so that their height or width does not exceed a specified maximum size. It also pads the images to be square, filling the background with white. The script overwrites the original images with the processed images.

### Dependencies

Ensure the following dependencies are installed before running the script:
- Python 3.6 or higher
- Pillow library for image processing

```sh
pip install pillow
```

### Usage

To use this script, run it from the command line with the appropriate parameters. The script processes all images in the specified directory, resizing and padding them as needed, and overwrites the original images.

### Command-Line Parameters

| Parameter         | Description                                              | Example                    |
|-------------------|----------------------------------------------------------|----------------------------|
| `input_directory` | Directory containing images to process.                  | `/path/to/input_directory` |
| `max_size`        | Maximum dimension (width or height) for resizing images. | `1536`                     |

### Example Command

```bash
python data-prep/img-to-square.py D:\ML\training\illustration-square 1536
```

Replace `/path/to/input_directory` with the path to your directory containing images. The script will resize and pad all images in that directory, overwriting the original images.

### Notes

- `png`, `jpg`, `jpeg`, `bmp`, and `gif` files will be processed.
- The script will overwrite the original images with the processed versions.
- If the specified input directory does not exist, the script will terminate with an error message.