# Copyright (c) FlamesCoder. Licensed under the MIT Licence.
# See the LICENCE file in the repository root for full licence text.

import pygame
import os

from pyosu.settings import ROOT_DIR


def render_text(surface: pygame.Surface, text: str | int | float, font_name: str = "Aller_Lt", size: int = 30,
                position: tuple = (10, 10)) -> None:
    text = str(text)
    font = pygame.font.Font(os.path.join(ROOT_DIR, f"game/resources/fonts/{font_name}.ttf"), size)
    text_render = font.render(text, True, (255, 255, 255))
    surface.blit(text_render, position)


def get_text(text: str | int | float, font_name: str = "Aller_Lt", size: int = 30) -> pygame.Surface:
    text = str(text)
    font = pygame.font.Font(os.path.join(ROOT_DIR, f"game/resources/fonts/{font_name}.ttf"), size)
    text_render = font.render(text, True, (255, 255, 255))
    return text_render
