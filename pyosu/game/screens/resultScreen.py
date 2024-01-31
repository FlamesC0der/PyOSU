# Copyright (c) FlamesCoder. Licensed under the MIT Licence.
# See the LICENCE file in the repository root for full licence text.

import pygame
import os
import datetime

from pyosu.settings import ROOT_DIR
from pyosu.game.utils.fonts import render_text, get_text
from pyosu.game.utils.sprites import BackButton, Text
from pyosu.game.utils.rating import get_rating
from pyosu.log import logger
from pprint import pprint


class ResultScreen:
    def __init__(self, game, args):
        self.game = game
        self.screen = self.game.screen
        self.args = args

        self.score = self.args[1]

        self.bg = self.args[0][0]["bg"]
        self.bg = pygame.transform.scale(self.bg, (self.game.width, self.game.height))
        self.ranking_panel = self.game.skin_manager.get_skin("ranking-panel")
        self.ranking_panel = pygame.transform.scale(self.ranking_panel, (self.game.width, self.game.height - 100))

        self.applause_sound = self.game.skin_manager.get_skin("applause")
        self.applause_sound.play()
        self.played_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

        # Sprites
        self.layer_1 = pygame.sprite.Group()

        self.back_button = BackButton(self.layer_1, game=self.game, screen_to_change="MainMenu")
        Rating(
            self.layer_1,
            game=self.game,
            rating=get_rating(self.score['accuracy'])
        )

        Text(self.layer_1, text=self.args[0][0]["level_name"], size=30, position=(5, 5))
        Text(self.layer_1, text=f"Beatmap by {self.args[0][0]['levels'][0]['author']}", size=30, position=(5, 35))
        Text(self.layer_1, text=f"Played by Flame on {self.played_time}", size=18, position=(5, 55))
        Text(self.layer_1, text=" ".join([n for n in f"{self.score['score']:010}"]), font_name="AllerDisplay",
             size=50, position=(165, 125))
        # s300
        Text(self.layer_1, text=f"{self.score['notes_values']['300']}x", font_name="AllerDisplay", size=35,
             position=(200, 250))

        # s100
        Text(self.layer_1, text=f"{self.score['notes_values']['100']}x", font_name="AllerDisplay", size=35,
             position=(200, 350))

        # s50
        Text(self.layer_1, text=f"{self.score['notes_values']['50']}x", font_name="AllerDisplay", size=35,
             position=(200, 450))

        # s300_0
        Text(self.layer_1, text=f"{self.score['notes_values']['300-0']}x", font_name="AllerDisplay", size=35,
             position=(500, 250))

        # s100_0
        Text(self.layer_1, text=f"{self.score['notes_values']['100-0']}x", font_name="AllerDisplay", size=35,
             position=(500, 350))

        # s0
        Text(self.layer_1, text=f"{self.score['notes_values']['0']}x", font_name="AllerDisplay", size=35,
             position=(500, 450))

        # Misc
        Text(self.layer_1, text=f"{self.score['combo']}x", font_name="AllerDisplay", size=40,
             position=(100, self.game.height // 2 + 150))
        Text(self.layer_1, text=f"{self.score['accuracy']:.2f}%", font_name="AllerDisplay", size=40,
             position=(400, self.game.height // 2 + 150))

        logger.info("resultScreen screen Initialized")

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_screen("MainMenu")

    def update(self, events):
        self.layer_1.update()

    def render(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))
        screen.blit(self.bg, (0, 0))
        screen.blit(self.ranking_panel, (0, 105))

        top_panel = pygame.Surface((self.game.width, 100), pygame.SRCALPHA)
        top_panel.fill((0, 0, 0, 200))
        screen.blit(top_panel, (0, 0))

        # render_text(screen, self.args[0][0]["level_name"], size=30, position=(5, 5))
        # render_text(screen, f"Beatmap by {self.args[0][0]['levels'][0]['author']}", size=18, position=(5, 35))
        # render_text(screen, f"Played by Flame on {self.played_time}", size=18,
        #             position=(5, 55))
        #
        # render_text(screen, " ".join([n for n in f"{self.score['score']:010}"]), font_name="AllerDisplay", size=50,
        #             position=(165, 125))

        # Score values
        s_300 = self.game.skin_manager.get_skin("hit300")
        s_300 = pygame.transform.scale(s_300, (50, 50))
        screen.blit(s_300, (100, 250))
        # render_text(screen, f"{self.score['notes_values']['300']}x", font_name="AllerDisplay", size=35,
        #             position=(200, 250))

        s_100 = self.game.skin_manager.get_skin("hit100")
        s_100 = pygame.transform.scale(s_100, (50, 50))
        screen.blit(s_100, (100, 350))
        # render_text(screen, f"{self.score['notes_values']['100']}x", font_name="AllerDisplay", size=35,
        #             position=(200, 350))

        s_50 = self.game.skin_manager.get_skin("hit50")
        s_50 = pygame.transform.scale(s_50, (50, 50))
        screen.blit(s_50, (100, 450))
        # render_text(screen, f"{self.score['notes_values']['50']}x", font_name="AllerDisplay", size=35,
        #             position=(200, 450))

        s_300_0 = self.game.skin_manager.get_skin("hit300k")
        s_300_0 = pygame.transform.scale(s_300_0, (50, 50))
        screen.blit(s_300_0, (400, 250))
        # render_text(screen, f"{self.score['notes_values']['300-0']}x", font_name="AllerDisplay", size=35,
        #             position=(500, 250))

        s_100_0 = self.game.skin_manager.get_skin("hit100k")
        s_100_0 = pygame.transform.scale(s_100_0, (50, 50))
        screen.blit(s_100_0, (400, 350))
        # render_text(screen, f"{self.score['notes_values']['100-0']}x", font_name="AllerDisplay", size=35,
        #             position=(500, 350))

        s_0 = self.game.skin_manager.get_skin("hit0")
        s_0 = pygame.transform.scale(s_0, (50, 50))
        screen.blit(s_0, (400, 450))
        # render_text(screen, f"{self.score['notes_values']['0']}x", font_name="AllerDisplay", size=35,
        #             position=(500, 450))

        # render_text(screen, f"{self.score['combo']}x", font_name="AllerDisplay", size=40,
        #             position=(100, self.game.height // 2 + 150))
        # render_text(screen, f"{self.score['accuracy']:.2f}%", font_name="AllerDisplay", size=40,
        #             position=(400, self.game.height // 2 + 150))

        self.layer_1.draw(screen)


class Rating(pygame.sprite.Sprite):
    def __init__(self, *groups, game, rating):
        super().__init__(*groups)

        self.game = game

        self.image = self.game.skin_manager.get_skin(f"ranking-{rating}")
        self.rect = self.image.get_rect()
        self.rect.centerx = self.game.width - 200
        self.rect.centery = 320

    def update(self):
        pass
