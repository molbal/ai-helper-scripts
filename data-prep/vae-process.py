import os
import argparse
import shutil
from tqdm import tqdm
from PIL import Image
from comfy_api_simplified import ComfyApiWrapper, ComfyWorkflowWrapper

COMFYUI_INPUT_DIR = "C:/tools/data/Packages/ComfyUI/input"

def vae_passthrough(path, filename):
    api = ComfyApiWrapper("http://127.0.0.1:8188/")
    wf = ComfyWorkflowWrapper("D:/ML/sd-scripts/workflows/vae-reencode.json")

    shutil.copy(path + "/" + filename, COMFYUI_INPUT_DIR + "/" + filename)
    wf.set_node_param("Load Image", "image", filename)
    results = api.queue_and_wait_images(wf, output_node_title="Save Image")
    for filename2, image_data in results.items():
        with open(f"{path}/vae-{filename}", "wb+") as f:
            f.write(image_data)

def list_images(directory):
    # Check if the directory exists
    if not os.path.isdir(directory):
        print(f"The directory {directory} does not exist.")
        return

    # List all files in the directory
    files = os.listdir(directory)

    # Filter out the images (png or jpg) and check their dimensions
    images = []
    for file in tqdm(files, desc="Scanning directory"):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            images.append(file)

    # Print the list of images
    if images:
        for image in tqdm(images, desc="Processing images"):
            vae_passthrough(directory, image)
    else:
        print(f"No images found in the directory.")


if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description="List all images (png or jpg) in a directory "
                    "to reencode them with a VAE")
    parser.add_argument('directory', type=str, help="The directory to list images from.")

    # Parse the arguments
    args = parser.parse_args()

    # Call the function with the provided directory and max size
    list_images(args.directory)
