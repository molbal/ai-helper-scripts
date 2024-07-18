import os
import sys
import argparse
from PIL import Image, ImageOps, ExifTags
from tqdm import tqdm


def correct_image_orientation(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break

        exif = image._getexif()
        if exif is not None:
            orientation = exif.get(orientation, 1)

            if orientation == 3:
                image = image.rotate(180, expand=True)
            elif orientation == 6:
                image = image.rotate(270, expand=True)
            elif orientation == 8:
                image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # Cases where image does not have EXIF data or any other issue
        pass
    return image


def resize_and_pad_image(image, max_size=1536):
    # Correct the image orientation
    image = correct_image_orientation(image)

    # Resize the image while maintaining aspect ratio
    image.thumbnail((max_size, max_size))

    # Calculate padding to make the image square
    width, height = image.size
    max_dim = max(width, height)

    # Create a new white background image
    new_image = Image.new("RGB", (max_dim, max_dim), (255, 255, 255))

    # Paste the resized image onto the white background
    new_image.paste(image, ((max_dim - width) // 2, (max_dim - height) // 2))

    return new_image


def process_images(input_directory, max_size=1536):
    for filename in tqdm(os.listdir(input_directory)):
        if filename.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
            file_path = os.path.join(input_directory, filename)
            with Image.open(file_path) as img:
                new_img = resize_and_pad_image(img, max_size)
                new_img.save(file_path)  # Overwrite the original image


def main():
    parser = argparse.ArgumentParser(description="Resize and pad images to be square with a white background.")
    parser.add_argument("input_directory", type=str, help="Directory containing images to process.")
    parser.add_argument("max_size", type=int, help="Maximum dimension (width or height) for resizing images.")

    args = parser.parse_args()

    if not os.path.isdir(args.input_directory):
        print(f"The directory {args.input_directory} does not exist.")
        sys.exit(1)

    process_images(args.input_directory, args.max_size)
    print("Image processing complete.")


if __name__ == "__main__":
    main()
