import pygame
import os
import sys
import random

from pyosu.settings import ROOT_DIR
from pyosu.game.utils.image_loader import load_image
from pyosu.game.core import quit
from pyosu.log import logger


class IntroScreen:
    def __init__(self, game):
        logger.info("Screen: IntroScreen")
        self.game = game
        self.screen = game.screen

        self.bg = pygame.Surface((game.width, game.height))
        self.bg.fill((0, 0, 0))

        self.bgs = [load_image(os.path.join(ROOT_DIR, f"game/resources/bg/{img}")) for img in
                    os.listdir(os.path.join(ROOT_DIR, 'game/resources/bg'))]
        self.bg_timer = pygame.time.get_ticks()
        self.change_bg()

        self.buttons = [(load_image(os.path.join(ROOT_DIR, f"game/resources/sprites/{b}.png")),
                         load_image(os.path.join(ROOT_DIR, f"game/resources/sprites/{b}_hover.png"))) for b in
                        ["play", "options", "exit"]]

        # Sprites
        self.sprites = pygame.sprite.Group()
        self.menu_buttons = pygame.sprite.Group()

        self.osu_button = OsuButton(self.sprites, game=self.game)

        for i, button_img in enumerate(self.buttons):
            MenuButton(
                self.menu_buttons,
                buttons=self.buttons,
                index=i,
                game=self.game,
                osu_button=self.osu_button
            )

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()

    def change_bg(self):
        self.bg = random.choice(self.bgs)
        self.bg = pygame.transform.scale(self.bg, (self.game.width, self.game.height))

    def update(self):
        current_time = pygame.time.get_ticks()

        if self.bg_timer + 15000 < current_time:
            self.bg_timer = current_time
            self.change_bg()
        self.menu_buttons.update()
        self.sprites.update()

    def render(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.bg, (0, 0))

        self.menu_buttons.draw(self.screen)
        self.sprites.draw(self.screen)


class OsuButton(pygame.sprite.Sprite):
    def __init__(self, *groups, game):
        super().__init__(*groups)

        self.game = game

        self.image = load_image(os.path.join(ROOT_DIR, "game/resources/sprites/Osu.png"))
        self.image = pygame.transform.scale(self.image, (600, 600))
        self.original_image = self.image.copy()

        self.rect = self.image.get_rect()
        self.rect.centerx = self.game.width // 2
        self.rect.centery = self.game.height // 2

        self.opened = False
        self.last_click_time = 0
        self.cooldown_duration = 500

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0]:
            current_time = pygame.time.get_ticks()
            if self.rect.collidepoint(mouse_x, mouse_y):
                if current_time - self.last_click_time >= self.cooldown_duration:
                    self.opened = not self.opened

                    self.last_click_time = current_time

        if self.rect.collidepoint(mouse_x, mouse_y) or self.opened:
            self.image = pygame.transform.scale(self.original_image, (700, 700))
        else:
            current_size = self.image.get_size()

            new_size = (
                current_size[0] + 1,
                current_size[1] + 1
            )

            if new_size[0] > 650:
                new_size = self.original_image.get_size()
            self.image = pygame.transform.scale(self.original_image, new_size)

        self.rect = self.image.get_rect()
        self.rect.centerx = self.game.width // 2
        self.rect.centery = self.game.height // 2

        if self.opened:
            self.rect.x = self.game.width // 2 - 600


class MenuButton(pygame.sprite.Sprite):
    def __init__(self, *groups, buttons, index, game, osu_button):
        super().__init__(*groups)

        self.buttons = buttons
        self.index = index
        self.game = game
        self.osu_button = osu_button

        self.original_image = self.buttons[self.index][0]
        ratio = self.original_image.get_height() / self.original_image.get_width()
        self.original_image = pygame.transform.scale(self.original_image, (700, ratio * 700))

        self.hover_image = self.buttons[self.index][1]
        self.hover_image = pygame.transform.scale(self.hover_image, (700, ratio * 700))

        self.image = self.original_image.copy()

        self.rect = self.image.get_rect()
        self.rect.centerx = self.game.width // 2 + 200
        self.rect.y = 250 + self.index * (ratio * 700 + 50)

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Open/close
        if self.osu_button.opened:
            self.image.set_alpha(255)
            self.hover_image.set_alpha(255)
        else:
            self.image.set_alpha(0)
            self.hover_image.set_alpha(0)

        # Hold
        if self.rect.collidepoint(mouse_x, mouse_y) and self.osu_button.opened:
            self.image = self.hover_image
            self.rect.centerx = self.game.width // 2 + 250
        else:
            self.image = self.original_image
            self.rect.centerx = self.game.width // 2 + 200

        # Onclick
        if pygame.mouse.get_pressed()[0] and self.osu_button.opened:
            if self.rect.collidepoint(mouse_x, mouse_y):
                if self.index == 0:
                    self.game.change_screen("MainMenu")
                if self.index == 1:
                    pass
                if self.index == 2:
                    quit()
