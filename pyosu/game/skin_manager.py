import pygame
import pathlib
import os

from pyosu.settings import ROOT_DIR
from pyosu.game.utils.image_loader import load_image
from pyosu.log import logger


class SkinManager:
    def __init__(self, skin_pack_name):
        self.skin_pack_name = skin_pack_name
        self.images = {}

        for image in os.listdir(os.path.join(ROOT_DIR, f'skins/{self.skin_pack_name}')):
            if os.path.isfile(os.path.join(ROOT_DIR, f'skins/{self.skin_pack_name}/{image}')):
                file_data = image.split(".")
                if file_data[1] in ["png", "jpg", "jpeg"]:
                    self.images[file_data[0]] = load_image(
                        os.path.join(ROOT_DIR, f'skins/{self.skin_pack_name}/{image}'))

        logger.info("Loaded skins")

    def get_skin(self, image_name):
        try:
            return self.images[image_name]
        except IndexError as e:
            logger.error(f"Failed to get skin, {image_name}, \n {e}")
