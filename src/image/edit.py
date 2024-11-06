from PIL import Image

def center_crop(image: Image.Image, target_width: float, target_height: float) -> tuple[float, float, float, float]:
    width, height = image.size
    left = (width - target_width) / 2
    top = (height - target_height) / 2
    right = (width + target_width) / 2
    bottom = (height + target_height) / 2

    return (left, top, right, bottom)

def offset_crop(image: Image.Image, x: float, y: float, target_width: float, target_height: float) -> tuple[float, float, float, float]:
    left = x
    top = y
    right = x + target_width
    bottom = y + target_height

    if left < 0 or top < 0 or right > image.width or bottom > image.height:
        raise ValueError("Crop box is out of image bounds")
    
    return (left, top, right, bottom)

def crop_image(image: Image.Image, box: tuple[float, float, float, float]):
    return image.crop(box)

def pad_image(image: Image.Image, target_width: float, target_height: float, background_color: tuple[int, int, int]=(255, 255, 255)):
    width, height = image.size
    new_image = Image.new("RGB", (target_width, target_height), background_color)
    new_image.paste(image, ((target_width - width) // 2, (target_height - height) // 2))
    return new_image

def fill_image(image: Image.Image, target_width: float, target_height: float):
    # Resize the image to fill the target dimensions (stretched)
    return image.resize((target_width, target_height), Image.Resampling.LANCZOS)

def fit_image(image: Image.Image, target_width: float, target_height: float, background_color: tuple[int, int, int]=(255, 255, 255)):
    # Resize image to fit within target dimensions while maintaining aspect ratio
    image.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
    return pad_image(image, target_width, target_height, background_color)

###############################################################################################################################################################

def edit_image(image: Image.Image, target_width: float, target_height: float, mode: str, background_color: tuple[int, int, int]=(255, 255, 255)):
    if mode == "CROP":
        return crop_image(image, 0, 0, target_width, target_height)
    elif mode == "FILL":
        return fill_image(image, target_width, target_height)
    elif mode == "FIT":
        return fit_image(image, target_width, target_height, background_color)

def process_image(image: Image.Image, output_path: str, target_width: float, target_height: float, mode: str, background_color: tuple[int, int, int]=(255, 255, 255)):
    if getattr(image, "is_animated", False):
        frames = []
        for frame in range(image.n_frames):
            image.seek(frame)
            edited_frame = edit_image(image.copy(), target_width, target_height, mode, background_color)
            frames.append(edited_frame)
        frames[0].save(output_path, save_all=True, append_images=frames[1:], loop=0)
    else:
        edited_image = edit_image(image, target_width, target_height, mode, background_color)
        edited_image.show()
        edited_image.save(output_path)

if __name__ == "__main__":
    input_image_path = "test.gif"  # Replace with your input image path
    output_image_path = "output.gif"  # Replace with your desired output image path
    target_width = 1000  # Desired width
    target_height = 600  # Desired height

    user_choice = input("Choose operation (CROP, FILL, FIT): ").upper()

    image = Image.open(input_image_path)
    process_image(image, output_image_path, target_width, target_height, user_choice)
    print("Image edited and saved successfully.")
