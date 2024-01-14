import pygame
import os

from pyosu.game.utils.fonts import render_text
from pyosu.log import logger


class MainMenu:
    def __init__(self, game):
        logger.info("Screen: MainMenu")
        self.game = game
        self.screen = game.screen

        # Sprites
        self.songs = pygame.sprite.Group()

        # temp
        self.song = Song(self.songs, game=self.game, name="Waldschrein", difficulty=10)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_screen("IntroScreen")

    def update(self):
        self.songs.update()

    def render(self, screen):
        # screen.fill((255, 255, 255))
        screen.fill((0, 0, 0))
        pygame.draw.line(screen, (0, 0, 255), (0, 100), (self.game.width, 100), 3)
        pygame.draw.line(screen, (0, 0, 255), (0, self.game.height - 100), (self.game.width, self.game.height - 100), 3)

        self.songs.draw(screen)


class Song(pygame.sprite.Sprite):
    def __init__(self, *groups, game, name, difficulty):
        super().__init__(*groups)

        self.game = game
        self.name = name
        self.difficulty = difficulty

        self.image = self.game.skin_manager.get_skin("menu-button-background")
        self.image = pygame.transform.scale(self.image, (724, 150))
        self.rect = self.image.get_rect()

        self.rect.right = self.game.width + 100
        self.rect.y = self.game.height // 2

    def update(self):
        render_text(self.image, self.name, "Aller_Lt", 25, (150, 30))

        for i in range(self.difficulty):
            star = self.game.skin_manager.get_skin("star")
            star = pygame.transform.scale(star, (30, 30))
            self.image.blit(star, (150 + 40 * i, 90))

