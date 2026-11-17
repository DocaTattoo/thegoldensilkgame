import pygame
from settings import SCREEN_WIDTH, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, PLAYER_JUMP_POWER, GRAVITY

class Player:
    def __init__(self):
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = PLAYER_SPEED
        self.jump_power = PLAYER_JUMP_POWER
        self.gravity = GRAVITY
        self.reset(SCREEN_WIDTH // 2, 500)

    def reset(self, x, y):
        self.x, self.y = x, y
        self.velocity_x = 0
        self.velocity_y = 0
        self.left_pressed = False
        self.right_pressed = False
        self.collect_animation = 0

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def update(self, platforms):
        self.velocity_x = 0
        if self.left_pressed:
            self.velocity_x -= self.speed
        if self.right_pressed:
            self.velocity_x += self.speed
        self.x += self.velocity_x
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))

        old_bottom = self.y + self.height
        self.velocity_y += self.gravity
        self.y += self.velocity_y

        if self.velocity_y >= 0:
            new_bottom = self.y + self.height
            for platform in platforms:
                if (old_bottom <= platform.y and new_bottom >= platform.y and
                    self.x + self.width > platform.x and self.x < platform.x + platform.width):
                    self.y = platform.y - self.height
                    self.velocity_y = self.jump_power
                    break

        if self.collect_animation > 0:
            self.collect_animation -= 1

    def collect_item(self):
        self.collect_animation = 20

    def draw(self, screen, camera, character):
        x, y = int(self.x), int(self.y - camera.y)
        scale = 1 + (0.08 * self.collect_animation / 20 if self.collect_animation > 0 else 0)
        center_x = x + self.width // 2
        body_width, body_height = int(self.width * scale), int(self.height * scale)
        body_x = center_x - body_width // 2
        body_y = y + self.height - body_height

        pygame.draw.rect(screen, character.body_color,
                         (body_x, body_y, body_width, body_height), border_radius=10)
        pygame.draw.circle(screen, (255,210,170), (center_x, y+15), 15)
        pygame.draw.circle(screen, (20,20,25), (center_x-5, y+13), 2)
        pygame.draw.circle(screen, (20,20,25), (center_x+5, y+13), 2)
