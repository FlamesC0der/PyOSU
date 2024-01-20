import pygame
import sys

from pyosu.log import logger


class Cursor(pygame.sprite.Sprite):
    def __init__(self, screen, skin_manager):
        super().__init__()
        self.image = skin_manager.get_skin("cursor")
        self.rect = self.image.get_rect()

        self.screen = screen

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.screen.blit(self.image, self.rect)

    def hide(self):
        self.image.set_alpha(0)

    def show(self):
        self.image.set_alpha(255)


# temp
def quit(game) -> None:
    logger.warning("Exiting game")
    game.current_music.stop()
    pygame.mixer.stop()
    sound = pygame.mixer.Sound("game/resources/sounds/see_you_next_time.mp3")
    s = sound.play()
    while s.get_busy():
        pygame.time.wait(10)

    pygame.quit()
    sys.exit()


def time_to_frame(ms: int) -> int:
    return int(ms * 60 / 1000)


def handle_click(object, mouse_x: int, mouse_y: int):
    keys = pygame.key.get_pressed()
    if pygame.mouse.get_pressed()[0] or keys[pygame.K_z] or keys[pygame.K_x]:
        if object.rect.collidepoint(mouse_x, mouse_y):
            return True
    return False
