import math
import numpy as np
from PIL import Image

def color_distance(color1: tuple[int,int,int], color2: tuple[int,int,int]):
    """Calculate the Euclidean distance between two RGB colors."""
    return np.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)))

def extract_palette(image: Image.Image, num_colors: int=4) -> list[tuple[int,int,int]]:
    # Resize the image to speed up processing (optional)
    image = image.resize((100, 100))
    
    # Get the colors in the image and convert to a list
    colors = list(set(image.getdata()))  # Use set to get unique colors

    # Find distinct highlight colors
    highlight_colors = []
    
    while len(highlight_colors) < num_colors and colors:
        if not highlight_colors:
            # Start with the first color
            highlight_colors.append(colors.pop(0))
        else:
            # Find the color that is farthest from already selected highlight colors
            distances = [min(color_distance(color, h_color) for h_color in highlight_colors) for color in colors]
            max_distance_index = distances.index(max(distances))
            highlight_colors.append(colors.pop(max_distance_index))
    
    return highlight_colors

def create_gradient(start_color: tuple[int,int,int], end_color: tuple[int,int,int], steps:int) -> Image.Image:
    gradient = []
    for i in range(steps):
        ratio = i / float(steps - 1)
        r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
        gradient.append((r, g, b))
    return gradient

def create_rgba_gradient(width: float, height: float, color1: tuple[int,int,int], color2: tuple[int,int,int], angle: int) -> Image.Image:
    # Create a new image with an RGBA mode
    image = Image.new("RGBA", (width, height))

    # Convert angle to radians
    angle_rad = math.radians(angle)

    for x in range(width):
        for y in range(height):
            # Calculate the ratio based on the angle
            ratio = (math.sin(angle_rad) * (x / width) + math.cos(angle_rad) * (y / height)) / (math.sin(angle_rad) + math.cos(angle_rad))

            # Ensure ratio is within the range [0, 1]
            ratio = max(0, min(1, ratio))

            # Interpolate colors (normalized to 0-1)
            r = int((color1[0] * (1 - ratio) + color2[0] * ratio) * 255)
            g = int((color1[1] * (1 - ratio) + color2[1] * ratio) * 255)
            b = int((color1[2] * (1 - ratio) + color2[2] * ratio) * 255)
            a = int((color1[3] * (1 - ratio) + color2[3] * ratio) * 255)

            # Set the pixel color
            image.putpixel((x, y), (r, g, b, a))

    return image

def normalize_palette(palette: tuple[int,int,int], alpha=1.0) -> tuple[float, float, float, float]:
    # Normalize the RGB values to the range [0.0, 1.0]
    r_normalized = palette[0] / 255.0
    g_normalized = palette[1] / 255.0
    b_normalized = palette[2] / 255.0
    return (r_normalized, g_normalized, b_normalized, alpha)

def denormalize_palette(normalized_palette: tuple[float, float, float, float]) -> tuple[int, int, int]:
    """Convert normalized RGBA values back to the range of 0-255."""
    r = int(normalized_palette[0] * 255)
    g = int(normalized_palette[1] * 255)
    b = int(normalized_palette[2] * 255)
    return (r, g, b)

def overlay_gradient_on_image(image: Image.Image, color1: tuple[int,int,int], color2: tuple[int,int,int], angle: int):
    base_image = image.convert("RGBA")
    gradient_image = create_rgba_gradient(base_image.width, base_image.height, color1, color2, angle)
    combined_image = Image.alpha_composite(base_image, gradient_image)
    return combined_image
