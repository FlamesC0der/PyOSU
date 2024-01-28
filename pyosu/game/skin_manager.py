import pygame
import os
from pprint import pprint

from pyosu.settings import ROOT_DIR
from pyosu.game.utils.image_loader import load_image
from pyosu.log import logger


class SkinManager:
    def __init__(self, skin_pack_name):
        self.skin_pack_name = skin_pack_name
        self.assets = {}

        for asset in os.listdir(os.path.join(ROOT_DIR, f'skins/{self.skin_pack_name}')):
            if os.path.isfile(os.path.join(ROOT_DIR, f'skins/{self.skin_pack_name}/{asset}')):
                name, extension = asset.rsplit(".")

                if extension in ["png", "PNG", "jpg", "jpeg"]:
                    self.assets[name] = load_image(
                        os.path.join(ROOT_DIR, f'skins/{self.skin_pack_name}/{asset}'))
                elif extension in ["mp3", "ogg", "wav"]:
                    try:
                        self.assets[name] = pygame.mixer.Sound(f"skins/{self.skin_pack_name}/{asset}")
                    except pygame.error:
                        logger.warning(f"Failed to load sound {name}")

        logger.info("Loaded skin assets")

    def get_skin(self, image_name) -> pygame.Surface | None:
        try:
            return self.assets[image_name]
        except Exception as e:
            logger.error(f"Failed to get skin, {image_name}, \n {e}")
            return None
