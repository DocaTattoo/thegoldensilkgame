import pygame

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, screen, font, selected=False):
        color = (80,170,100) if selected else (50,50,60)
        pygame.draw.rect(screen, color, self.rect, border_radius=15)
        pygame.draw.rect(screen, (255,255,255), self.rect, 2, border_radius=15)
        surface = font.render(self.text, True, (255,255,255))
        screen.blit(surface, surface.get_rect(center=self.rect.center))

    def contains(self, position):
        return self.rect.collidepoint(position)
