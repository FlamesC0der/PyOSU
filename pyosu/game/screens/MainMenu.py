import pygame
import os
import math
import random

from pyosu.settings import ROOT_DIR
from pyosu.game.utils.fonts import render_text
from pyosu.game.utils.image_loader import load_image
from pyosu.game.level import get_levels
from pyosu.game.core import handle_click
from pyosu.game.utils.sprites import BackButton, Text
from pyosu.log import logger


class MainMenu:
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen

        self.intro_music_skipped = False

        self.bottom_buttons_list = [
            (self.game.skin_manager.get_skin(f"{b}"), self.game.skin_manager.get_skin(f"{b}-over"))
            for b
            in ["selection-mode", "selection-mods", "selection-random", "selection-options"]]

        # Sprites
        self.song_list = pygame.sprite.Group()
        self.bottom_buttons = pygame.sprite.Group()
        self.layer_1 = pygame.sprite.Group()

        self.back_button = BackButton(self.layer_1, game=self.game, screen_to_change="IntroScreen")
        self.play_button = PlayButton(self.layer_1, game=self.game)

        self.bg = pygame.Surface((self.game.width, self.game.height))
        self.bg.fill((0, 0, 0))

        # Song list

        self.levels = []

        for level in get_levels():
            for song_data in level["levels"]:
                self.levels.append((level, song_data))
                Song(self.song_list, game=self.game, name=song_data["name"], author=song_data["author"],
                     bg=level["bg"], difficulty=song_data["data"]["OverallDifficulty"],
                     difficulty_title=song_data["difficulty"],
                     music=pygame.mixer.Sound(
                         os.path.join(ROOT_DIR,
                                      f"songs/{level['level_name']}/{song_data['data']['AudioFilename']}"))
                     )

        self.selected_song_index = random.randint(0, len(self.song_list.sprites()) - 1)
        self.scroll_offset = 0

        self.song_last_clicked = pygame.time.get_ticks()

        # Render bottom buttons

        for i in range(len(self.bottom_buttons_list)):
            BottomButton(
                self.bottom_buttons,
                buttons=self.bottom_buttons_list,
                game=self.game,
                index=i
            )

        self.music_playing = False

        logger.info("MainMenu screen Initialized")

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_screen("IntroScreen")
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset += event.y * 10

    def change_song(self, i):
        self.selected_song_index = i
        if self.game.current_music:
            self.game.current_music.stop()
        self.game.current_music = self.song_list.sprites()[i].music
        self.game.current_music.play(-1)
        self.scroll_offset = 0

    def update(self, events):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        self.song_list.update()
        self.bottom_buttons.update()
        self.layer_1.update()

        # handle songs
        for i, song in enumerate(self.song_list.sprites()):
            target_y = (self.game.height - 150) // 2 + (i - self.selected_song_index) * (
                    120 - min(5, abs(self.selected_song_index - i)) * 5) - self.scroll_offset
            current_y = song.rect.y
            song.rect.y += (target_y - current_y) // 5
            song.rect.right = self.game.width + 200 + min(5, abs(self.selected_song_index - i)) * 15

            if i == self.selected_song_index:
                self.bg = song.bg

            if handle_click(song, mouse_x, mouse_y):
                if not self.play_button.rect.collidepoint(mouse_x,
                                                          mouse_y) and (
                        current_time - self.song_last_clicked >= 500):
                    self.song_last_clicked = pygame.time.get_ticks()
                    self.change_song(i)

            # start playing music if not playing
            if not self.music_playing:
                if self.selected_song_index == i:
                    self.game.current_music.stop()
                    self.game.current_music = song.music
                    self.game.current_music.play(-1)
                    self.music_playing = True

        # handle bottom buttons
        for i, button in enumerate(self.bottom_buttons.sprites()):
            if pygame.mouse.get_pressed()[0] or keys[pygame.K_z] or keys[pygame.K_x]:
                current_time = pygame.time.get_ticks()
                if button.rect.collidepoint(mouse_x,
                                            mouse_y) and (
                        current_time - button.last_click_time >= button.cooldown_duration):
                    if button.index == 0:
                        pass
                    elif button.index == 1:
                        pass
                    elif button.index == 2:
                        self.change_song(random.randint(0, len(self.song_list.sprites()) - 1))
                    elif button.index == 3:
                        pass

        # Play button
        if pygame.mouse.get_pressed()[0] or keys[pygame.K_z] or keys[pygame.K_x]:
            if self.play_button.rect.collidepoint(mouse_x, mouse_y):
                self.music_playing = False
                self.game.change_screen("Level", self.levels[self.selected_song_index])

        self.bg = pygame.transform.scale(self.bg, (self.game.width, self.game.height))

    def render(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))
        screen.blit(self.bg, (0, 0))

        self.song_list.draw(screen)

        # Ui above
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, self.game.width, 100))
        pygame.draw.rect(screen, (0, 0, 0), (0, 100, 400, 100))
        pygame.draw.polygon(screen, (0, 0, 0), ((400, 100), (500, 100), (400, 200)))
        pygame.draw.rect(screen, (0, 0, 0), (0, self.game.height - 100, self.game.width, self.game.height))

        pygame.draw.line(screen, (0, 0, 255), (0, 200), (400, 200), 3)
        pygame.draw.line(screen, (0, 0, 255), (400, 200), (500, 100), 3)
        pygame.draw.line(screen, (0, 0, 255), (500, 100), (self.game.width, 100), 3)
        pygame.draw.line(screen, (0, 0, 255), (0, self.game.height - 100), (self.game.width, self.game.height - 100), 3)

        self.bottom_buttons.draw(screen)
        self.layer_1.draw(screen)

        for i, song in enumerate(self.song_list.sprites()):
            if i == self.selected_song_index:
                render_text(self.screen, song.name, "Aller_Lt", 30, (50, 10))
                render_text(self.screen, f"Mapped by {song.author}", "Aller_Lt", 20, (50, 40))


class Song(pygame.sprite.Sprite):
    def __init__(self, *groups, game, name, author, difficulty_title, difficulty, bg, music):
        super().__init__(*groups)

        self.game = game
        self.name = name
        self.author = author
        self.difficulty_title = difficulty_title
        self.difficulty = difficulty
        self.bg = bg
        self.music = music

        self.image = self.game.skin_manager.get_skin("menu-button-background")
        self.image = pygame.transform.scale(self.image, (800, 160))
        self.rect = self.image.get_rect()

        self.rect.right = self.game.width + 400
        self.rect.y = self.game.height // 2

        aspect_ratio = self.bg.get_width() / self.bg.get_height()
        self.logo = pygame.transform.scale(self.bg, (min(100 * aspect_ratio, 120), 100))
        self.image.blit(self.logo, (15, 30))

        render_text(self.image, self.name, "Aller_Lt", 25, (150, 30))
        render_text(self.image, self.author, "Aller_Lt", 23, (150, 55))
        render_text(self.image, self.difficulty_title, "Aller_Rg", 20, (150, 80))

    def update(self):
        # Stars
        for i in range(math.ceil(float(self.difficulty))):
            star = self.game.skin_manager.get_skin("star")
            star = pygame.transform.scale(star, (25, 30))
            self.image.blit(star, (150 + 35 * i, 100))


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
        self.cooldown_duration = 1000

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

        if self.index == 0:
            self.image.blit(self.mode, (30, 20))


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

        # hover/animation
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
