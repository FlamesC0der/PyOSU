import pygame
import os
import sys
import random

from pyosu.settings import ROOT_DIR
from pyosu.game.utils.image_loader import load_image
from pyosu.game.effects import fade_in, fade_out
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

        # fade_in(self.screen, self.bg, 2)

        # Sprites
        self.sprites = pygame.sprite.Group()

        OsuButton(self.sprites, game=self.game)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sound = pygame.mixer.Sound("game/resources/sounds/see_you_next_time.mp3")
                sound.play()

                fade_out(self.game.screen, self.bg, 2)

                pygame.quit()
                sys.exit()

    def change_bg(self):
        self.bg = random.choice(self.bgs)
        self.bg = pygame.transform.scale(self.bg, (self.game.width, self.game.height))

    def update(self):
        current_time = pygame.time.get_ticks()

        if self.bg_timer + 15000 < current_time:
            self.bg_timer = current_time
            self.change_bg()

    def render(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.bg, (0, 0))

        self.sprites.draw(self.screen)


class OsuButton(pygame.sprite.Sprite):
    def __init__(self, *groups, game):
        super().__init__(*groups)

        self.image = load_image(os.path.join(ROOT_DIR, "game/resources/sprites/Osu.png"))
        self.image = pygame.transform.scale(self.image, (600, 600))

        self.rect = self.image.get_rect()
        self.rect.centerx = game.width // 2
        self.rect.centery = game.height // 2

    def update(self):
        pass
