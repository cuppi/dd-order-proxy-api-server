import base64
from os import path
from .file_manager import save_file


class ImageHandler:
    @staticmethod
    def save_image(file_str):
        image_dir = path.join(path.dirname(path.abspath(__file__)), '..', 'tmp')
        image_file = 'image.png'
        save_file(path.join(image_dir, image_file), base64.b64decode(file_str), file_type='img')
