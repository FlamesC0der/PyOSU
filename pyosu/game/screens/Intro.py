import pygame
import os

from pyosu.settings import ROOT_DIR
from pyosu.game.utils.image_loader import load_image
from pyosu.log import logger


class Intro:
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen

        self.bg = pygame.Surface((self.game.width, self.game.height))
        self.bg.fill((0, 0, 0))

        self.sprites = pygame.sprite.Group()

        Welcome(self.sprites, game=game)

    def handle_events(self, event):
        pass

    def update(self):
        self.sprites.update()

    def render(self, screen):
        screen.fill((0, 0, 0))

        self.sprites.draw(screen)


class Welcome(pygame.sprite.Sprite):
    def __init__(self, *groups, game):
        super().__init__(*groups)

        self.game = game

        self.image = load_image(os.path.join(ROOT_DIR, "game/resources/sprites/welcome.png"))
        self.image = pygame.transform.scale(self.image, (300, 62))

        self.rect = self.image.get_rect()
        self.rect.centerx = self.game.width // 2
        self.rect.centery = self.game.height // 2

        self.frame = 0
        logger.info("Intro screen Initialized")

    def update(self):
        self.game.cursor.hide()
        self.frame += 1

        if self.frame >= 150:
            self.game.change_screen("IntroScreen")
