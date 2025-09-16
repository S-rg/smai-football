from ball import Ball
from player import Player
from state import State
import matplotlib.pyplot as plt

class Game:
    def __init__(self, num_players_per_team=11, position_map=None):
        self.position_map = position_map
        self.state = self.initialize_game(num_players_per_team)

    def initialize_game(self, num_players_per_team):
        home_team = [Player() for _ in range(num_players_per_team)]
        away_team = [Player() for _ in range(num_players_per_team)]
        ball = Ball()
        score_home = 0
        score_away = 0
        turn = 1

        state = State(home_team, away_team, ball, score_home, score_away, turn, self.position_map)
        state.reset_positions(self.position_map)
        return state
    
    def show(self):
        self.state.show()
