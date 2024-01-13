import pygame


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
