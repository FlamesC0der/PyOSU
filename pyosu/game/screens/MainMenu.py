import pygame
import os

from pyosu.settings import ROOT_DIR
from pyosu.game.utils.fonts import render_text
from pyosu.game.utils.image_loader import load_image
from pyosu.log import logger


class MainMenu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

        self.bottom_buttons = [(self.game.skin_manager.get_skin(f"{b}"), self.game.skin_manager.get_skin(f"{b}-over"))
                               for b
                               in ["selection-mode", "selection-mods", "selection-random", "selection-options"]]

        # Sprites
        self.songs = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()

        # temp
        self.song = Song(self.songs, game=self.game, name="Waldschrein", difficulty=10)
        self.bg = load_image(os.path.join(ROOT_DIR, "songs/369354 Equilibrium - Waldschrein/folk folk folk folk.jpg"))
        self.bg = pygame.transform.scale(self.bg, (self.game.width, self.game.height))

        for i in range(len(self.bottom_buttons)):
            BottomButton(self.buttons, buttons=self.bottom_buttons, game=self.game, index=i)

        logger.info("MainMenu screen Initialized")

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_screen("IntroScreen")

    def update(self):
        self.songs.update()
        self.buttons.update()

    def render(self, screen):
        # screen.fill((255, 255, 255))
        screen.fill((0, 0, 0))
        screen.blit(self.bg, (0, 0))

        # Ui above
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, self.game.width, 100))
        pygame.draw.rect(screen, (0, 0, 0), (0, self.game.height - 100, self.game.width, self.game.height))
        pygame.draw.line(screen, (0, 0, 255), (0, 100), (self.game.width, 100), 3)
        pygame.draw.line(screen, (0, 0, 255), (0, self.game.height - 100), (self.game.width, self.game.height - 100), 3)

        self.songs.draw(screen)

        self.buttons.draw(screen)


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


class BottomButton(pygame.sprite.Sprite):
    def __init__(self, *groups, buttons, game, index):
        super().__init__(*groups)

        self.buttons = buttons
        self.game = game
        self.index = index

        self.original_image = self.buttons[self.index][0]
        self.hover_image = self.buttons[self.index][1]

        self.image = self.original_image.copy()

        self.rect = self.image.get_rect()
        self.rect.x = 317 + self.index * 77
        if self.index == 0:
            self.rect.x = 300
        self.rect.y = self.game.height - 100

        self.last_click_time = 0
        self.cooldown_duration = 500

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Hold

        if self.rect.collidepoint(mouse_x, mouse_y):
            self.image = self.hover_image
        else:
            self.image = self.original_image

        # Click

        if pygame.mouse.get_pressed()[0]:
            current_time = pygame.time.get_ticks()
            if self.rect.collidepoint(mouse_x, mouse_y):
                if current_time - self.last_click_time >= self.cooldown_duration:
                    self

                    self.last_click_time = current_time
