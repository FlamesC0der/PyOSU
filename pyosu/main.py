import pygame
import sys
import os

from pyosu.settings import ROOT_DIR
from pyosu.log import logger
from pyosu.game.core import Cursor
from pyosu.game.skin_manager import SkinManager

# Screens
from pyosu.game.screens.introScreen import IntroScreen


class Game():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        logger.info("Initialized pygame")

        screen_info = pygame.display.Info()
        self.width, self.height = screen_info.current_w, screen_info.current_h

        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        # self.screen = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME)
        self.clock = pygame.time.Clock()
        self.skin_manager = SkinManager("boop")

        self.cursor = Cursor(self.screen, self.skin_manager)
        self.is_Running = True

        self.screens = {"IntroScreen": IntroScreen(self), "MainMenu": 1}
        self.current_screen = "IntroScreen"

        self.intro_showed = False

        pygame.display.set_caption("PyOSU")
        pygame.mouse.set_visible(False)

        logger.info("Game Initialized")

        # Welcome to osu sound
        sound = pygame.mixer.Sound(os.path.join(ROOT_DIR, "game/resources/sounds/welcome.mp3"))
        sound.play()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_Running = False

                pygame.quit()
                sys.exit()

            self.screens[self.current_screen].handle_events(event)

    def change_screen(self, new_screen):
        if new_screen in self.screens:
            self.current_screen = new_screen

    def update(self):
        self.screens[self.current_screen].update()

    def render(self):
        self.screens[self.current_screen].render(self.screen)
        self.cursor.update()
        pygame.display.flip()

    def run(self):
        while self.is_Running:
            self.handle_events()
            self.update()
            self.render()

            self.clock.tick(60)


if __name__ == "__main__":
    logger.info("PyOSU By FlamesCoder")
    game = Game()
    game.run()
