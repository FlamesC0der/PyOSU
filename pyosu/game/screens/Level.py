import pygame
import os

from pyosu.settings import ROOT_DIR
from pyosu.game.utils.fonts import render_text
from pyosu.game.utils.image_loader import load_image
from pyosu.log import logger


class Level:
    def __init__(self, game):
        self.game = game

        # Sprites

        logger.info("Level screen Initialized")

    def handle_events(self, event):
        pass

    def update(self):
        pass

    def render(self, screen):
        pass