import math
import pygame

class Collectible:
    def __init__(self, x, y, item_name, color):
        self.x = x
        self.base_y = y
        self.item_name = item_name
        self.color = color
        self.animation_time = 0
        self.collected = False

    def update(self):
        self.animation_time += 0.08

    def get_y(self):
        return self.base_y + math.sin(self.animation_time) * 10

    @property
    def rect(self):
        y = self.get_y()
        return pygame.Rect(int(self.x - 17), int(y - 17), 34, 34)

    def draw(self, screen, camera):
        if self.collected:
            return
        x, y = self.x, self.get_y() - camera.y

        if self.item_name == "Stella":
            points = []
            for i in range(10):
                angle = -math.pi / 2 + i * math.pi / 5
                radius = 17 if i % 2 == 0 else 7
                points.append((x + math.cos(angle) * radius,
                               y + math.sin(angle) * radius))
            pygame.draw.polygon(screen, self.color, points)

        elif self.item_name == "Hamburger":
            pygame.draw.ellipse(screen, (220, 160, 80), (x-18, y-15, 36, 16))
            pygame.draw.rect(screen, (80,160,70), (x-18,y-1,36,5))
            pygame.draw.rect(screen, (170,70,40), (x-18,y+5,36,7))
            pygame.draw.rect(screen, (240,190,60), (x-18,y+12,36,5))

        elif self.item_name == "Cartuccia":
            pygame.draw.rect(screen, (70,70,80), (x-13,y-16,26,32), border_radius=4)
            pygame.draw.rect(screen, (180,180,190), (x-9,y-20,18,6))
            pygame.draw.rect(screen, (40,40,45), (x-7,y+3,14,10))
