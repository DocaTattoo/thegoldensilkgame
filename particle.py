import random
import pygame

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.velocity_x = random.uniform(-3, 3)
        self.velocity_y = random.uniform(-5, -1)
        self.life = random.randint(25, 45)
        self.max_life = self.life
        self.size = random.randint(3, 7)
        self.color = color

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += 0.15
        self.life -= 1

    def draw(self, screen):
        if self.life <= 0:
            return
        ratio = self.life / self.max_life
        size = max(1, int(self.size * ratio))
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)

    def is_alive(self):
        return self.life > 0
