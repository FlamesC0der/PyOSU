import pygame
import os

from pyosu.settings import ROOT_DIR
from pyosu.game.utils.fonts import render_text
from pyosu.game.utils.image_loader import load_image
from pyosu.game.core import handle_click
from pyosu.log import logger
from pprint import pprint

from pyosu.modes.osu import Circle, Slider, Spinner


class Level:
    def __init__(self, game, args):
        self.game = game
        self.screen = self.game.screen
        self.args = args

        self.data = self.args[1]["data"]

        self.game.current_music.stop()

        logger.info(f"Starting level {self.args[1]['name']}")
        # pprint(self.data)

        self.start_time = pygame.time.get_ticks()
        self.end_time = 0

        self.music_playing = False
        self.music = self.game.current_music = pygame.mixer.Sound(
            os.path.join(ROOT_DIR, f"songs/{self.args[1]['name']}/{self.data['AudioFilename']}"))

        # Sprites
        self.game.padding = (self.game.width - self.game.height) // 2

        self.objects = self.data["hitObjects"].copy()
        self.circles_sprites = pygame.sprite.Group()
        self.game.hit_images = pygame.sprite.Group()

        self.bg = self.args[0]["bg"]
        self.bg = pygame.transform.scale(self.bg, (self.game.width, self.game.height))
        self.bg.set_alpha(120)

        # Sounds
        self.click_sound = self.game.skin_manager.get_skin("soft-hitnormal")

        # Stats
        self.nbCircles = self.data["nbCircles"]
        self.nbSliders = self.data["nbSliders"]
        self.nbSpinners = self.data["nbSpinners"]

        self.game.score = {
            "score": 0,
            "accuracy": 100,
            "combo": 0,
            "notes_values": {
                "300": 0,
                "100": 0,
                "50": 0,
                "0": 0,
                "300-0": 0,
                "100-0": 0
            }
        }

        self.game.current_notes = 0
        self.game.clicked_notes = 0

        logger.info("Level screen Initialized")

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_screen("MainMenu")

    def result(self):
        logger.info(f"Level ended. Result: {self.game.score}")
        self.game.change_screen("ResultScreen", self.args, self.game.score)

    def update(self):
        # mouse_x, mouse_y = pygame.mouse.get_pos()
        current_time = pygame.time.get_ticks() - self.start_time - 5000

        if current_time > 0 and not self.music_playing:
            self.music.play()
            self.music_playing = True

        for object in self.objects:
            if current_time > object["startTime"] - 500:
                if object["object_name"] == "circle":
                    Circle(
                        self.circles_sprites,
                        game=self.game,
                        pos=tuple(object["position"]),
                        start_time=object["startTime"]
                    )
                elif object["object_name"] == "slider":
                    Slider(
                        self.circles_sprites,
                        game=self.game,
                        data=object
                    )
                elif object["object_name"] == "spinner":
                    Spinner(
                        self.circles_sprites,
                        game=self.game,
                        start_time=object["startTime"],
                        end_time=object["end_time"]
                    )
                self.objects.remove(object)

        self.circles_sprites.update(current_time)
        self.game.hit_images.update()

        if len(self.circles_sprites.sprites()) == 0 and not self.objects:  # quit from level
            self.end_time += 100
            if self.end_time >= 10000:
                self.result()

        if self.game.current_notes > 0:
            self.game.score["accuracy"] = (self.game.score["score"] / (self.game.current_notes * 300)) * 100

    def render(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))
        screen.blit(self.bg, (0, 0))

        self.circles_sprites.draw(screen)
        self.game.hit_images.draw(screen)

        render_text(self.screen, f"{self.game.score['score']:010}", font_name="AllerDisplay", size=40,
                    position=(self.game.width - 250, 15))
        render_text(self.screen, f"{self.game.score['accuracy']:.2f}%", font_name="Aller_It", size=30,
                    position=(self.game.width - 150, 60))
        render_text(self.screen, f"{self.game.score['combo']}x", font_name="AllerDisplay", size=50,
                    position=(20, self.game.height - 20))
