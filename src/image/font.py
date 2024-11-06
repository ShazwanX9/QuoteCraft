from PIL import Image, ImageDraw, ImageFont

def wrap_text(text: str, font: ImageFont, max_width: int) -> list:
    """Wrap text to fit within a specified width."""
    lines = []
    words = text.split()
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        # Using textbbox for width
        if ImageDraw.Draw(Image.new("RGB", (1, 1))).textbbox((0, 0), test_line, font=font)[2] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())  # Append trimmed line
            current_line = word + " "

    if current_line:
        lines.append(current_line.strip())  # Append last line

    return lines

def calculate_text_height(text: str, font: ImageFont, max_width: int, line_height: int) -> int:
    """Calculate the number of lines needed to fit the text within a specified width."""
    wrapped_text = wrap_text(text, font, max_width)
    return len(wrapped_text)*line_height+len(wrapped_text)*font.size

def draw_wrapped_text(image: Image.Image, text: str, position: tuple[int, int], font: ImageFont.ImageFont, 
                      color: tuple[int, int, int], max_width: int, line_height: int) -> Image.Image:
    """Draw wrapped text on an image at a specified position."""
    draw = ImageDraw.Draw(image)
    wrapped_text = wrap_text(text, font, max_width)

    y_text = position[1]
    for line in wrapped_text:
        draw.text((position[0], y_text), line, fill=color, font=font)
        # Calculate line height with added spacing
        y_text += (draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1]) + line_height

    return image


def draw_wrapped_outline_text(image: Image.Image, text: str, position: tuple[int, int], font: ImageFont.ImageFont, 
                      color: tuple[int, int, int], outline_color: tuple[int, int, int], 
                      max_width: int, line_height: int) -> Image.Image:
    """Draw wrapped text on an image at a specified position with an outline."""
    draw = ImageDraw.Draw(image)
    wrapped_text = wrap_text(text, font, max_width)

    y_text = position[1]
    for line in wrapped_text:
        # Draw the outline by drawing the text multiple times with offsets
        offsets = [-1, 0, 1]  # x-offsets for outline (left, center, right)
        for dx in offsets:
            draw.text((position[0] + dx, y_text), line, fill=outline_color, font=font)
        
        offsets = [-1, 0, 1]  # y-offsets for outline (top, center, bottom)
        for dy in offsets:
            draw.text((position[0], y_text + dy), line, fill=outline_color, font=font)

        # Draw the actual text on top
        draw.text((position[0], y_text), line, fill=color, font=font)
        
        # Calculate line height with added spacing
        y_text += (draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1]) + line_height

    return image