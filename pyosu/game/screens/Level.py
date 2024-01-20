import pygame
import os

from pyosu.settings import ROOT_DIR
from pyosu.game.utils.fonts import render_text
from pyosu.game.utils.image_loader import load_image
from pyosu.game.core import handle_click
from pyosu.log import logger
from pprint import pprint


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

        self.music_playing = False
        self.music = self.game.current_music = pygame.mixer.Sound(
            os.path.join(ROOT_DIR, f"songs/{self.args[1]['name']}/{self.data['AudioFilename']}"))

        # Sprites
        self.game.padding = (self.game.width - self.game.height) // 2

        self.objects = self.data["hitObjects"].copy()
        self.circles_sprites = pygame.sprite.Group()

        self.bg = self.args[0]["bg"]
        self.bg = pygame.transform.scale(self.bg, (self.game.width, self.game.height))
        self.bg.set_alpha(120)

        # Stats
        self.nbCircles = self.data["nbCircles"]
        self.nbSliders = self.data["nbSliders"]
        self.nbSpinners = self.data["nbSpinners"]

        self.current_notes = 0
        self.clicked_notes = 0
        self.score = 0

        self.game.combo = 0
        self.accuracy = 100
        self.score = 0

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_screen("MainMenu")

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
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
                    pass
                elif object["object_name"] == "spinner":
                    Spinner(
                        self.circles_sprites,
                        game=self.game,
                        start_time=object["startTime"],
                        end_time=object["end_time"]
                    )
                self.objects.remove(object)
                self.current_notes += 1

        self.circles_sprites.update(current_time)

        for i, object in enumerate(self.circles_sprites.sprites()):
            if handle_click(object, mouse_x, mouse_y) and not object.animation and not object.clicked:
                logger.info(f"clicked {self.clicked_notes + 1}/{self.nbCircles}")
                object.clicked = True
                self.clicked_notes += 1
                self.score += 300
                self.game.combo += 1

        if not self.objects:
            self.game.change_screen("MainMenu")

        if self.current_notes > 0:
            self.accuracy = (self.score / (self.current_notes * 300)) * 100

    def render(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))
        screen.blit(self.bg, (0, 0))

        self.circles_sprites.draw(screen)

        render_text(self.screen, f"{self.score:010}", font_name="AllerDisplay", size=40,
                    position=(self.game.width - 250, 15))
        render_text(self.screen, f"{self.accuracy:.2f}%", font_name="Aller_It", size=30,
                    position=(self.game.width - 150, 60))
        render_text(self.screen, f"{self.game.combo}x", font_name="AllerDisplay", size=40,
                    position=(20, self.game.height - 100))


class Circle(pygame.sprite.Sprite):
    def __init__(self, *groups, game, pos, start_time):
        super().__init__(*groups)

        self.game = game
        self.pos = pos
        self.start_time = start_time

        self.approach_circle = self.game.skin_manager.get_skin("approachcircle")
        self.hit_circle = self.game.skin_manager.get_skin("hitcircle")

        self.image = self.approach_circle.copy()

        self.rect = self.image.get_rect()
        self.rect.centerx = self.game.padding + 50 + (self.pos[0] / 512) * (self.game.height - 100)
        self.rect.centery = 100 + (self.pos[1] / 512) * (self.game.height - 200)

        self.clicked = False
        self.animation = True

    def update(self, current_time):
        if current_time > self.start_time - 500:  # show before animation
            progress = (self.start_time - current_time) / 500
            scaled_size = int(128 + (175 * progress))

            self.image = pygame.transform.scale(self.approach_circle, (scaled_size, scaled_size))
            self.rect = self.image.get_rect(center=self.rect.center)
        if current_time > self.start_time:  # show hit
            self.animation = False
            self.image = self.hit_circle
            self.rect = self.image.get_rect(center=self.rect.center)
        if self.clicked:
            self.kill()
        if current_time > self.start_time + 200:  # hide
            self.game.combo = 0
            self.kill()

        # todo fix this problem
        # self.image.blit(self.hit_circle, (self.image.get_width() // 2 - 62.5, self.image.get_height() // 2 - 62.5))


class Spinner(pygame.sprite.Sprite):
    def __init__(self, *groups, game, start_time, end_time):
        super().__init__(*groups)

        self.game = game
        self.start_time = start_time
        self.end_time = end_time

        self.approach_circle = self.game.skin_manager.get_skin("spinner-approachcircle")
        self.spinner_circle = self.game.skin_manager.get_skin("spinner-circle")

        self.image = self.approach_circle.copy()

        self.rect = self.image.get_rect()
        self.rect.centerx = self.game.padding + 50 + 0.5 * (self.game.height - 100)
        self.rect.centery = 100 + 0.5 * (self.game.height - 200)

        self.clicked = False
        self.animation = True

    def update(self, current_time):
        if current_time > self.start_time:
            progress = (current_time - self.start_time) / (self.end_time - self.start_time)
            scaled_size = max(1, int(100 + (340 * (1 - progress))))
            self.image = pygame.transform.scale(self.approach_circle, (scaled_size, scaled_size))
            self.rect = self.image.get_rect(center=self.rect.center)
        if current_time > self.end_time:
            self.kill()

        self.image.blit(self.spinner_circle, (self.image.get_width() // 2 - 62.5, self.image.get_height() // 2 - 62.5))
