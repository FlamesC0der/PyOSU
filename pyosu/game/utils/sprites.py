# Copyright (c) FlamesCoder. Licensed under the MIT Licence.
# See the LICENCE file in the repository root for full licence text.

import pygame
from pyosu.game.core import handle_click
from pyosu.game.utils.fonts import get_text


class BackButton(pygame.sprite.Sprite):
    def __init__(self, *groups, game, screen_to_change: str):
        super().__init__(*groups)

        self.game = game
        self.screen_to_change = screen_to_change

        self.frames = [self.game.skin_manager.get_skin(f"menu-back-{i}") for i in range(8 + 1)]
        self.current_frame_index = 0
        self.frame = 0

        self.image = self.frames[self.current_frame_index]
        self.image = pygame.transform.scale(self.image, (250, 250))

        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.bottom = self.game.height

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.frame += 1
        if self.frame >= 5:
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
            self.frame = 0
        self.image = self.frames[self.current_frame_index]
        self.image = pygame.transform.scale(self.image, (250, 250))

        if handle_click(self, mouse_x, mouse_y):
            self.game.change_screen(self.screen_to_change)


class Text(pygame.sprite.Sprite):
    def __init__(self, *groups, text: str | int | float, font_name: str = "Aller_Lt", size: int = 30,
                 position: tuple = (0, 0)):
        super().__init__(*groups)

        self.image = get_text(text, font_name, size)
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = position
