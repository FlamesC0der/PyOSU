import pygame
import sys


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
def quit(game):
    game.intro_music.stop()
    sound = pygame.mixer.Sound("game/resources/sounds/see_you_next_time.mp3")
    s = sound.play()
    while s.get_busy():
        pygame.time.wait(10)

    pygame.quit()
    sys.exit()


def time_to_frame(ms):
    return int(ms * 60 / 1000)
