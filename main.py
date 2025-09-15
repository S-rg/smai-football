from ball import Ball
from game import Game
from player import Player
from state import State

import time

if __name__ == "__main__":
    game = Game(num_players_per_team=5)
    game.show()

    game.state.home_team[0].move(10, 0)

    neighbors = game.state.get_neighbours()
    print(f"Number of neighbors: {len(neighbors)}")

    game.show_neighbours()