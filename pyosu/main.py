import pygame
import sys
import os
import math

from pyosu.settings import ROOT_DIR
from pyosu.log import logger
from pyosu.game.core import Cursor, quit
from pyosu.game.skin_manager import SkinManager
from pyosu.game.utils.fonts import render_text

# Screens
from pyosu.game.screens.Intro import Intro
from pyosu.game.screens.IntroScreen import IntroScreen
from pyosu.game.screens.MainMenu import MainMenu
from pyosu.game.screens.Level import Level
from pyosu.game.screens.resultScreen import ResultScreen


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

        self.screens = {"Intro": Intro(self), "IntroScreen": IntroScreen(self), "MainMenu": MainMenu(self)}
        self.current_screen = self.screens["Intro"]
        # self.current_screen = self.screens["MainMenu"]

        pygame.display.set_caption("PyOSU")
        pygame.mouse.set_visible(False)

        logger.info("Game Initialized")

        # Welcome to osu sound
        sound = pygame.mixer.Sound(os.path.join(ROOT_DIR, "game/resources/sounds/welcome.mp3"))
        sound.play()

        self.current_music = pygame.mixer.Sound(os.path.join(ROOT_DIR, "game/resources/sounds/circles.mp3"))
        self.current_music.play(-1)

        logger.info("Starting game...")
        logger.info("==========================")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_Running = False

                pygame.quit()
                sys.exit()

            self.current_screen.handle_events(event)

    def change_screen(self, new_screen, *args):
        # Static screens
        if new_screen in ["IntroScreen", "MainMenu"]:
            self.current_screen = self.screens[new_screen]
        elif new_screen == "Level":
            self.current_screen = Level(self, args[0])
        elif new_screen == "ResultScreen":
            self.current_screen = ResultScreen(self, args)
        logger.info(f"changed screen to {new_screen}")

    def update(self):
        self.current_screen.update()

    def render(self):
        self.current_screen.render(self.screen)
        self.cursor.update()
        render_text(self.screen, f"fps: {math.ceil(self.clock.get_fps())}", size=20,
                    position=(self.width - 80, 10))  # fps
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
    try:
        game.run()
    except KeyboardInterrupt:
        quit(game)
