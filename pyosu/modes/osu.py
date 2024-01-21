import pygame

from pyosu.game.core import handle_click
from pyosu.game.beatmapparser.curve import Bezier
from pyosu.log import logger


class Circle(pygame.sprite.Sprite):
    def __init__(self, *groups, game, pos, start_time):
        super().__init__(*groups)

        self.game = game
        self.pos = pos
        self.start_time = start_time
        self.type = "circle"

        self.approach_circle = self.game.skin_manager.get_skin("approachcircle")
        self.hit_circle = self.game.skin_manager.get_skin("hitcircle")

        self.image = self.approach_circle.copy()

        self.rect = self.image.get_rect()
        self.rect.centerx = self.game.padding + 50 + (self.pos[0] / 512) * (self.game.height - 100)
        self.rect.centery = 100 + (self.pos[1] / 512) * (self.game.height - 200)

        self.click_sound = self.game.skin_manager.get_skin("soft-hitnormal")

        self.clicked = False
        self.animation = True

    def update(self, current_time):
        mouse_x, mouse_y = pygame.mouse.get_pos()

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
            self.game.current_notes += 1
            self.kill()
        if current_time > self.start_time + 200:  # hide if not clicked
            self.game.current_notes += 1
            self.game.score["combo"] = 0
            self.kill()
            self.game.score["notes_values"]["0"] += 1
            HitImage(self.game.hit_images, game=self.game, pos=(self.rect.centerx, self.rect.centery),
                     score=0)

        if handle_click(self, mouse_x, mouse_y) and not self.animation and not self.clicked:
            logger.info(f"clicked {self.game.clicked_notes + 1}")

            self.clicked = True
            self.game.clicked_notes += 1
            self.game.score["combo"] += 1
            self.click_sound.play()

            time_diff = current_time - self.start_time
            if 0 <= time_diff <= 50:  # 300
                self.game.score["score"] += 300
                self.game.score["notes_values"]["300"] += 1
                HitImage(self.game.hit_images, game=self.game, pos=(self.rect.centerx, self.rect.centery),
                         score=300)
            elif 51 <= time_diff <= 150:  # 100
                self.game.score["score"] += 100
                self.game.score["notes_values"]["100"] += 1
                HitImage(self.game.hit_images, game=self.game, pos=(self.rect.centerx, self.rect.centery),
                         score=100)
            elif 151 <= time_diff <= 200:  # 50
                self.game.score["score"] += 50
                self.game.score["notes_values"]["50"] += 1
                HitImage(self.game.hit_images, game=self.game, pos=(self.rect.centerx, self.rect.centery),
                         score=50)

        # todo fix this problem
        # self.image.blit(self.hit_circle, (self.image.get_width() // 2 - 62.5, self.image.get_height() // 2 - 62.5))


class Slider(pygame.sprite.Sprite):
    def __init__(self, *groups, game, data):
        super().__init__(*groups)

        self.game = game
        self.data = data
        self.type = "slider"

        self.curve_type = data['curveType']
        self.duration = data['duration']
        self.end_position = data['end_position']
        self.end_time = data['end_time']
        self.new_combo = data['newCombo']
        self.pixel_length = data['pixelLength']
        self.points = data['points']
        self.position = data['position']
        self.repeat_count = data['repeatCount']
        self.sound_types = data['soundTypes']
        self.start_time = data['startTime']

        self.bezier_curve = Bezier(self.points)

        self.image = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.curve_points = []
        for t in range(10):
            self.curve_points.append(self.bezier_curve.at(t / 10))
        self.draw_slider()

        self.duration = self.end_time - self.start_time

        self.follow_circle = SliderFollowCircle(*groups, game=self.game, slider=self)
        self.follow_circle_index = 0

    def draw_slider(self):
        for pos in self.curve_points:
            pygame.draw.circle(self.image, (255, 255, 255), (
                self.game.padding + 50 + (pos[0] / 512) * (self.game.height - 100),
                100 + (pos[1] / 512) * (self.game.height - 200)), 55)

        for pos in self.curve_points:
            pygame.draw.circle(self.image, (0, 0, 0), (
                self.game.padding + 50 + (pos[0] / 512) * (self.game.height - 100),
                100 + (pos[1] / 512) * (self.game.height - 200)), 50)

    def update(self, current_time):
        diff = (current_time - self.start_time) / self.duration
        if 1 >= diff > 0 and (self.follow_circle_index != int(diff * len(self.curve_points))):
            self.follow_circle_index = int(diff * (len(self.curve_points) - 1))
            self.follow_circle.update_pos(self.curve_points[self.follow_circle_index])
        self.follow_circle_index = int(diff * (len(self.curve_points) - 1))

        if current_time > self.end_time:
            self.follow_circle.kill()
            self.kill()
            current_time / self.start_time


class SliderFollowCircle(pygame.sprite.Sprite):
    def __init__(self, *groups, game, slider):
        super().__init__(*groups)

        self.game = game
        self.slider = slider
        self.type = "sliderFollowCircle"

        self.image = self.game.skin_manager.get_skin("sliderfollowcircle")
        self.image = pygame.transform.scale(self.image, (150, 150))

        self.rect = self.image.get_rect()
        self.rect.centerx = self.game.padding + 50 + (slider.curve_points[0][0] / 512) * (self.game.height - 100)
        self.rect.centery = 100 + (slider.curve_points[0][1] / 512) * (self.game.height - 200)

        self.state = 0
        self.hold_start_time = 0

    def update_pos(self, pos):
        self.rect.centerx = self.game.padding + 50 + (pos[0] / 512) * (self.game.height - 100)
        self.rect.centery = 100 + (pos[1] / 512) * (self.game.height - 200)

    def update(self, current_time):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        HitImage(self.game.hit_images, game=self.game, pos=(self.rect.centerx, self.rect.centery),
                 score="100k")


class Spinner(pygame.sprite.Sprite):
    def __init__(self, *groups, game, start_time, end_time):
        super().__init__(*groups)

        self.game = game
        self.start_time = start_time
        self.end_time = end_time
        self.type = "spinner"

        self.approach_circle = self.game.skin_manager.get_skin("spinner-approachcircle")
        self.spinner_circle = self.game.skin_manager.get_skin("spinner-circle")

        self.image = self.approach_circle.copy()

        self.rect = self.image.get_rect()
        self.rect.centerx = self.game.padding + 50 + 0.5 * (self.game.height - 100)
        self.rect.centery = 100 + 0.5 * (self.game.height - 200)

    def update(self, current_time):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if current_time > self.start_time:
            progress = (current_time - self.start_time) / (self.end_time - self.start_time)
            scaled_size = max(1, int(100 + (340 * (1 - progress))))
            self.image = pygame.transform.scale(self.approach_circle, (scaled_size, scaled_size))
            self.rect = self.image.get_rect(center=self.rect.center)
        if current_time > self.end_time:
            self.kill()

        self.image.blit(self.spinner_circle, (self.image.get_width() // 2 - 62.5, self.image.get_height() // 2 - 62.5))


class HitImage(pygame.sprite.Sprite):
    def __init__(self, *groups, game, pos, score):
        super().__init__(*groups)

        self.game = game
        self.pos = pos
        self.score = score

        self.start_time = pygame.time.get_ticks()

        self.image = self.game.skin_manager.get_skin(f"hit{self.score}")
        self.image = pygame.transform.scale(self.image, (100, 100))

        self.rect = self.image.get_rect()
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]

    def update(self):  # hide after 5000ms

        if pygame.time.get_ticks() - self.start_time >= 500:
            self.kill()
