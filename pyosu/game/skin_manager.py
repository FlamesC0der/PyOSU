import pygame
import os

from pyosu.settings import ROOT_DIR
from pyosu.game.utils.image_loader import load_image
from pyosu.log import logger


class SkinManager:
    def __init__(self, skin_pack_name):
        self.skin_pack_name = skin_pack_name
        self.assets = {}

        for asset in os.listdir(os.path.join(ROOT_DIR, f'skins/{self.skin_pack_name}')):
            if os.path.isfile(os.path.join(ROOT_DIR, f'skins/{self.skin_pack_name}/{asset}')):
                file_data = asset.split(".")
                if file_data[1] in ["png", "jpg", "jpeg"]:
                    self.assets[file_data[0]] = load_image(
                        os.path.join(ROOT_DIR, f'skins/{self.skin_pack_name}/{asset}'))
                elif file_data[1] in ["mp3", "ogg"]:
                    self.assets[file_data[0]] = pygame.mixer.Sound(f"skins/{self.skin_pack_name}/{asset}")

        logger.info("Loaded skin assets")

    def get_skin(self, image_name) -> pygame.Surface:
        try:
            return self.assets[image_name]
        except IndexError as e:
            logger.error(f"Failed to get skin, {image_name}, \n {e}")
