import cv2
from PIL import Image
import numpy as np

# ASCII characters used to build the output text
ASCII_CHARS = "@%#*+=-:. "

def gray_to_ascii(gray_value):
    """Convert a grayscale value to an ASCII character."""
    return ASCII_CHARS[gray_value * (len(ASCII_CHARS) - 1) // 255]

def resize_image(image, new_width=100):
    """Resize the image while maintaining the aspect ratio."""
    (old_width, old_height) = image.size
    aspect_ratio = old_height / float(old_width)
    new_height = int(aspect_ratio * new_width)
    return image.resize((new_width, new_height))

def convert_to_grayscale(image):
    """Convert the image to grayscale."""
    return image.convert("L")

def image_to_ascii(image, new_width=100):
    """Convert an image to ASCII art."""
    image = resize_image(image, new_width)
    image = convert_to_grayscale(image)

    pixels = np.array(image)
    ascii_str = ""
    for row in pixels:
        for pixel in row:
            ascii_str += gray_to_ascii(pixel)
        ascii_str += "\n"
    return ascii_str

def image_to_colored_ascii(image, new_width=100):
    """Convert an image to colored ASCII art."""
    image = resize_image(image, new_width)
    pixels = np.array(image)

    ascii_str = ""
    for row in pixels:
        for pixel in row:
            r, g, b = pixel
            gray_value = int(0.299 * r + 0.587 * g + 0.114 * b)
            ascii_char = gray_to_ascii(gray_value)
            ascii_str += f"\033[38;2;{r};{g};{b}m{ascii_char}\033[0m"
        ascii_str += "\n"
    return ascii_str

def save_ascii_art(ascii_str, output_file="ascii_art.txt"):
    """Save the ASCII art to a text file."""
    with open(output_file, "w") as f:
        f.write(ascii_str)

def save_colored_ascii_as_html(ascii_str, output_file="ascii_art.html"):
    """Save the colored ASCII art to an HTML file."""
    html_content = f"<pre style='font: 10px/5px monospace;'>{ascii_str}</pre>"
    with open(output_file, "w") as f:
        f.write(html_content)

def main(image_path, new_width=100, output_file="ascii_art.txt", colored=False):
    """Main function to convert an image to ASCII art."""
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Unable to open image file {image_path}.")
        print(e)
        return

    if colored:
        ascii_str = image_to_colored_ascii(image, new_width)
        save_colored_ascii_as_html(ascii_str, output_file.replace(".txt", ".html"))
    else:
        ascii_str = image_to_ascii(image, new_width)
        save_ascii_art(ascii_str, output_file)
    print(f"ASCII art saved to {output_file}")

    if colored:
        print(ascii_str)  # This will display colored ASCII art in the terminal

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert an image to ASCII art.")
    parser.add_argument("image_path", help="Path to the image file")
    parser.add_argument("--width", type=int, default=100, help="Width of the ASCII art (default: 100)")
    parser.add_argument("--output", default="ascii_art.txt", help="Output file for the ASCII art (default: ascii_art.txt)")
    parser.add_argument("--colored", action="store_true", help="Generate colored ASCII art")
    args = parser.parse_args()
    main(args.image_path, args.width, args.output, args.colored)
