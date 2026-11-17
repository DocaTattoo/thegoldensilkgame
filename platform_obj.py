import pygame

class Platform:
    def __init__(self, x, y, width, height=18):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def draw(self, screen, camera, scenario):
        screen_y = self.y - camera.y
        pygame.draw.rect(screen, scenario.platform_color,
                         (int(self.x), int(screen_y), self.width, self.height),
                         border_radius=6)
        pygame.draw.rect(screen, scenario.decoration_color,
                         (int(self.x), int(screen_y), self.width, 5),
                         border_radius=4)
