from ball import Ball
from player import Player
from state import State
import matplotlib.pyplot as plt

class Game:
    def __init__(self, num_players_per_team=11):
        self.state = self.initialize_game(num_players_per_team)

    def initialize_game(self, num_players_per_team):
        home_team = [Player() for _ in range(num_players_per_team)]
        away_team = [Player() for _ in range(num_players_per_team)]
        ball = Ball()
        score_home = 0
        score_away = 0
        turn = 1

        state = State(home_team, away_team, ball, score_home, score_away, turn)
        state.reset_positions()
        return state
    
    def show(self):
        fig = self.state.show()
        plt.show()    