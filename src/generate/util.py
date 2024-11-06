import os
import requests
from .gpic import GPic

def generate_image_url(prompt: str, width: int, height: int, seed: int, model: str, nologo: bool) -> str:
    return f"https://pollinations.ai/p/{prompt}?width={width}&height={height}&seed={seed}&model={model}&nologo={str(nologo).lower()}"

def download_image(image_url, image_name="cache.jpg", dirname=GPic.CACHE_DIR):
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    response = requests.get(image_url)
    with open(os.path.join(dirname, image_name), 'wb') as file:
        file.write(response.content)
    # print('Download Completed')
