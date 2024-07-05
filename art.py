import cv2
from PIL import Image
import numpy as np
import os
import sys

# ASCII characters used to build the output text
ASCII_CHARS = "@%#*+=-:. "

def gray_to_ascii(gray_value):

    return ASCII_CHARS[gray_value * (len(ASCII_CHARS) - 1) // 255]

def resize_image(image, new_width=100):
    
    (old_width, old_height) = image.size
    aspect_ratio = old_height / float(old_width)
    new_height = int(aspect_ratio * new_width)
    return image.resize((new_width, new_height))

def convert_to_grayscale(image):
    
    return image.convert("L")

def image_to_ascii(image, new_width=100):
    
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
    
    image = resize_image(image, new_width)
    
    
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    
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

def display_ascii_art(ascii_str):

    os.system('cls' if os.name == 'nt' else 'clear')
    print(ascii_str)

def main(new_width=100, colored=False):
    
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        sys.exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)

        if colored:
            ascii_str = image_to_colored_ascii(image, new_width)
        else:
            ascii_str = image_to_ascii(image, new_width)

        display_ascii_art(ascii_str)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Capture video and display ASCII art in real-time.")
    parser.add_argument("--width", type=int, default=100, help="Width of the ASCII art (default: 100)")
    parser.add_argument("--colored", action="store_true", help="Generate colored ASCII art")
    args = parser.parse_args()
    main(args.width, args.colored)

