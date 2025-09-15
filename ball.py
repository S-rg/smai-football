import math

class Ball:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def move(self, distance: int, direction: int):
        rad = math.radians(direction)
        self.x += distance * math.cos(rad)
        self.y += distance * math.sin(rad)

    