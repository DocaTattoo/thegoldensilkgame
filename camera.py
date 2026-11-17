from settings import SCREEN_HEIGHT, CAMERA_FOLLOW_HEIGHT

class Camera:
    def __init__(self):
        self.y = 0

    def update(self, player):
        target_y = player.y - SCREEN_HEIGHT * CAMERA_FOLLOW_HEIGHT
        if target_y < self.y:
            self.y += (target_y - self.y) * 0.08

    def reset(self):
        self.y = 0
