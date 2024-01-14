import pygame
import os

from pyosu.settings import ROOT_DIR


def render_text(surface: pygame.Surface, text: str | int | float, font_name: str, size: int, position: tuple) -> None:
    text = str(text)
    font = pygame.font.Font(os.path.join(ROOT_DIR, f"game/resources/fonts/{font_name}.ttf"), size)
    text_render = font.render(text, True, (255, 255, 255))
    surface.blit(text_render, position)
