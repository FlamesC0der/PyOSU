import pygame
import os

from pyosu.settings import ROOT_DIR
from pyosu.game.utils.fonts import render_text
from pyosu.game.utils.image_loader import load_image
from pyosu.log import logger
from pprint import pprint


class Level:
    def __init__(self, game, args):
        self.game = game
        self.screen = self.game.screen
        self.args = args

        # pprint(self.args)

        self.data = self.args[1]["data"]

        self.game.current_music.stop()

        logger.info(f"Starting level {self.args[1]['name']}")
        # pprint(self.data)

        self.start_time = pygame.time.get_ticks()

        music = self.game.current_music = pygame.mixer.Sound(
            os.path.join(ROOT_DIR, f"songs/{self.args[1]['name']}/{self.data['AudioFilename']}"))
        music.play()

        # Sprites
        self.game.padding = (self.game.width - self.game.height) // 2

        self.objects = self.data["hitObjects"].copy()
        self.circles_sprites = pygame.sprite.Group()

        self.bg = self.args[0]["bg"]
        self.bg = pygame.transform.scale(self.bg, (self.game.width, self.game.height))
        self.bg.set_alpha(100)

        # test
        # Circle(
        #     self.circles_sprites,
        #     game=self.game,
        #     pos=(0, 0),
        #     start_time=15
        # )
        # Circle(
        #     self.circles_sprites,
        #     game=self.game,
        #     pos=(512, 0),
        #     start_time=15
        # )
        # Circle(
        #     self.circles_sprites,
        #     game=self.game,
        #     pos=(512, 512),
        #     start_time=15
        # )
        # Circle(
        #     self.circles_sprites,
        #     game=self.game,
        #     pos=(0, 512),
        #     start_time=15
        # )

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_screen("MainMenu")

    def update(self):
        current_time = pygame.time.get_ticks() - self.start_time

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
                    pass
                self.objects.remove(object)

        self.circles_sprites.update(current_time)

    def render(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))
        screen.blit(self.bg, (0, 0))

        self.circles_sprites.draw(screen)


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

    def update(self, current_time):
        if current_time > self.start_time - 500:  # show before animation
            progress = min(1, (current_time - self.start_time) / 500)
            scaled_size = int(100 + (150 - 100) * (1 - progress))

            self.image = pygame.transform.scale(self.approach_circle, (scaled_size, scaled_size))
            self.rect = self.image.get_rect(center=self.rect.center)
        if current_time > self.start_time:  # show hit
            self.image = self.hit_circle
            self.rect = self.image.get_rect(center=self.rect.center)
        if current_time > self.start_time + 200:  # hide
            self.kill()
