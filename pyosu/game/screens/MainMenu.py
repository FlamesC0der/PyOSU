import pygame
import os

from pyosu.settings import ROOT_DIR
from pyosu.game.utils.fonts import render_text
from pyosu.game.utils.image_loader import load_image
from pyosu.log import logger


class MainMenu:
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen

        self.intro_music_skipped = False

        self.bottom_buttons = [(self.game.skin_manager.get_skin(f"{b}"), self.game.skin_manager.get_skin(f"{b}-over"))
                               for b
                               in ["selection-mode", "selection-mods", "selection-random", "selection-options"]]

        # Sprites
        self.songs = pygame.sprite.Group()
        self.layer_1 = pygame.sprite.Group()

        BackButton(self.layer_1, game=self.game)
        PlayButton(self.layer_1, game=self.game)

        # temp
        self.song = Song(self.songs, game=self.game, name="Waldschrein", difficulty=10)
        self.bg = load_image(os.path.join(ROOT_DIR, "songs/369354 Equilibrium - Waldschrein/folk folk folk folk.jpg"))
        self.bg = pygame.transform.scale(self.bg, (self.game.width, self.game.height))

        for i in range(len(self.bottom_buttons)):
            BottomButton(self.layer_1, buttons=self.bottom_buttons, game=self.game, index=i)

        logger.info("MainMenu screen Initialized")

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_screen("IntroScreen")

    def update(self):
        if not self.intro_music_skipped:
            self.game.intro_music.stop()

        self.songs.update()
        self.layer_1.update()

    def render(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.bg, (0, 0))

        # Ui above
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, self.game.width, 100))
        pygame.draw.rect(screen, (0, 0, 0), (0, 100, 300, 100))
        pygame.draw.polygon(screen, (0, 0, 0), ((300, 100), (400, 100), (300, 200)))
        pygame.draw.rect(screen, (0, 0, 0), (0, self.game.height - 100, self.game.width, self.game.height))

        pygame.draw.line(screen, (0, 0, 255), (0, 200), (300, 200), 3)
        pygame.draw.line(screen, (0, 0, 255), (300, 200), (400, 100), 3)
        pygame.draw.line(screen, (0, 0, 255), (400, 100), (self.game.width, 100), 3)
        pygame.draw.line(screen, (0, 0, 255), (0, self.game.height - 100), (self.game.width, self.game.height - 100), 3)

        self.songs.draw(screen)

        self.layer_1.draw(screen)


class Song(pygame.sprite.Sprite):
    def __init__(self, *groups, game, name, difficulty):
        super().__init__(*groups)

        self.game = game
        self.name = name
        self.difficulty = difficulty

        self.image = self.game.skin_manager.get_skin("menu-button-background")
        self.image = pygame.transform.scale(self.image, (1000, 150))
        self.rect = self.image.get_rect()

        self.rect.right = self.game.width + 400
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
        self.rect.x = 367 + self.index * 77
        if self.index == 0:
            self.rect.x = 350
        self.rect.y = self.game.height - 100

        self.last_click_time = 0
        self.cooldown_duration = 500

        if self.index == 0:
            self.mode = load_image(os.path.join(ROOT_DIR, "game/resources/sprites/mode_osu.png"))
            self.mode = pygame.transform.scale(self.mode, (35, 35))

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
                    # todo create menu for each button

                    self.last_click_time = current_time

        if self.index == 0:
            self.image.blit(self.mode, (30, 20))


class BackButton(pygame.sprite.Sprite):
    def __init__(self, *groups, game):
        super().__init__(*groups)

        self.game = game

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

        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(mouse_x, mouse_y):
                self.game.change_screen("IntroScreen")


class PlayButton(pygame.sprite.Sprite):
    def __init__(self, *groups, game):
        super().__init__(*groups)

        self.game = game

        self.image = load_image(os.path.join(ROOT_DIR, "game/resources/sprites/Osu.png"))
        self.image = pygame.transform.scale(self.image, (300, 300))
        self.original_image = self.image.copy()

        self.rect = self.image.get_rect()
        self.rect.centerx = self.game.width - 100
        self.rect.centery = self.game.height - 50

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_x, mouse_y):
            self.image = pygame.transform.scale(self.original_image, (350, 350))
        else:
            current_size = self.image.get_size()

            new_size = (
                current_size[0] + 2,
                current_size[1] + 2
            )

            if new_size[0] > 350:
                new_size = self.original_image.get_size()
            self.image = pygame.transform.scale(self.original_image, new_size)

        self.rect = self.image.get_rect()
        self.rect.centerx = self.game.width - 100
        self.rect.centery = self.game.height - 50
