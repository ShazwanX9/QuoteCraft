from src.generate.gpic import GPic 
from src.generate.util import generate_image_url, download_image
from src.image.font import draw_wrapped_outline_text, calculate_text_height, ImageFont
from src.image.edit import crop_image, offset_crop, Image
from src.image.color import extract_palette, overlay_gradient_on_image
from src.image.color import normalize_palette, denormalize_palette
from src.image.visualize_color import show_palette

import os
import random
from PIL import Image, ImageFont

class ImageManipulator(GPic):
    def __init__(self, prompt, width=800, height=900, seed=random.randint(1, 50)):
        super().__init__(prompt, width, height, seed, GPic.FLUX, True)
        self.image = None
        self.palette = []
        self.font_size = 64
        self.font_path = 'assets/fonts/VeganStylePersonalUse-5Y58.ttf'
        self.process_image()

    def generate_image(self, addon: str=""):
        download_image(
            generate_image_url(
                prompt=addon+self.prompt,
                width=self.width,
                height=self.height,
                seed=self.seed,
                model=GPic.FLUX,
                nologo=False
            ), 
            self.get_name(), 
            GPic.CACHE_DIR
        )
        self.image = Image.open(str(self))

    def crop_to_square(self):
        wh = min(self.image.width, self.image.height)
        self.image = crop_image(self.image, offset_crop(self.image, 0, 0, wh, wh))

    def apply_gradient(self, angle=90):
        self.palette = sorted(extract_palette(self.image, 5))
        color1 = normalize_palette(self.palette[0], .8)
        color2 = normalize_palette(self.palette[2], .6)
        self.image = overlay_gradient_on_image(self.image, color1, color2, angle=angle)

    def add_caption(self):
        while True:
            line_height = 30
            max_width = 450
            font = ImageFont.truetype(self.font_path, self.font_size)
            text_height = calculate_text_height(self.prompt, font, max_width, line_height)
            starting_y = self.image.height - text_height - 160
            if starting_y>80:
                break
            line_height*=.9
            self.font_size=int(self.font_size*.9)
        starting_y = max(starting_y, 80)
        self.image = draw_wrapped_outline_text(
            image=self.image,
            text=self.prompt,
            position=(80, starting_y), 
            font=font,
            color=self.palette[3],
            outline_color=self.palette[0],
            max_width=max_width,
            line_height=line_height
        )

    def add_author(self, author: str):
        line_height = 10
        max_width = 100
        font = ImageFont.truetype(self.font_path, int(self.font_size*.7))
        w = self.font_size*3
        self.image = draw_wrapped_outline_text(
            image=self.image,
            text=author,
            position=(self.image.width-w-max_width, 600-len(author.split())*line_height), 
            font=font,
            color=self.palette[3],
            outline_color=self.palette[0],
            max_width=max_width,
            line_height=line_height
        )

    def process_image(self):
        self.generate_image("JUST BACKGROUND FOR: ")
        self.crop_to_square()
        self.apply_gradient(45)
        self.add_caption()

    def save_image(self, filename):
        self.image.save(filename)

    def show_image(self):
        self.image.show()

# Usage
if __name__ == "__main__":
    prompt = 'Success is not final, failure is not fatal: It is the courage to continue that counts.'
    print(str(prompt))
    manipulator = ImageManipulator(prompt, seed=4)
    manipulator.show_image()
    # manipulator.change_variation()
    # manipulator.show_image()
    # manipulator.change_variation()
    # manipulator.show_image()
    # manipulator.reset()
    # manipulator.show_image()
    # # manipulator.save_image(f"{prompt.replace(' ', '_')}.png")
    # manipulator.save_image(str(prompt))