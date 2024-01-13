# import pygame
# import random
#
#
# def fade_out(screen, bg, speed=5):
#     clock = pygame.time.Clock()
#     width, height = screen.get_size()
#     overlay = pygame.Surface((width, height), pygame.SRCALPHA)
#     alpha = 0
#
#     while alpha < 255:
#         alpha += speed
#
#         if alpha > 255:
#             alpha = 255
#
#         screen.blit(bg, (0, 0))
#
#         overlay.fill((0, 0, 0, alpha))
#         screen.blit(overlay, (0, 0))
#
#         pygame.display.flip()
#
#         clock.tick(60)
#
#
# def fade_in(screen, bg, speed):
#     clock = pygame.time.Clock()
#     width, height = screen.get_size()
#     overlay = pygame.Surface((width, height), pygame.SRCALPHA)
#     alpha = 255
#
#     while alpha > 0:
#         alpha -= speed
#
#         if alpha < 0:
#             alpha = 0
#
#         screen.blit(bg, (0, 0))
#
#         overlay.fill((0, 0, 0, alpha))
#         screen.blit(overlay, (0, 0))
#
#         pygame.display.flip()
#
#         clock.tick(60)
