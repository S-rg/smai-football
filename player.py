import math
from ball import Ball

class Player:
    def __init__(
        self,
        sprint_speed: int = 10,
        shot_speed: int = 20,
        is_keeper: bool = False,
        has_possession: bool = False,
        x: int = 0,
        y: int = 0
    ):
        self.sprint_speed = sprint_speed
        self.shot_speed = shot_speed
        self.is_keeper = is_keeper
        self.has_possession = has_possession
        self.x = x
        self.y = y

    def move(self, distance: int, direction: int):
        rad = math.radians(direction)
        self.x += distance * math.cos(rad)
        self.y += distance * math.sin(rad)

    def shoot(self, ball: Ball, direction: int, power: int):
        if self.has_possession:
            ball.x = self.x
            ball.y = self.y
            ball.move(power, direction)
            self.has_possession = False