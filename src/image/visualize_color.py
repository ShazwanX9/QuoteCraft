from PIL import Image, ImageDraw

def show_palette(palette):
    # Create a new image for the palette
    palette_img = Image.new('RGB', (len(palette) * 100, 100))
    draw = ImageDraw.Draw(palette_img)
    
    for i, color in enumerate(palette):
        draw.rectangle([i * 100, 0, (i + 1) * 100, 100], fill=color)
    
    palette_img.show(title='Extracted Color Palette')

def show_gradient(gradient):
    # Create a new image for the gradient
    gradient_img = Image.new('RGB', (1000, 100))
    draw = ImageDraw.Draw(gradient_img)
    
    for i in range(1000):
        color = gradient[int(i / 1000 * len(gradient))]
        draw.line([(i, 0), (i, 100)], fill=color)

    gradient_img.show(title='Color Gradient')