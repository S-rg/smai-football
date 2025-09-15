from ball import Ball
from game import Game
from player import Player
from state import State

import time
from collections import deque

def quantize(value, precision=1):
    return round(value / precision) * precision


def serialize_state(state):

    player_positions = tuple(
        (quantize(p.x, 0.1), quantize(p.y, 0.1), p.has_possession)
        for p in state.home_team + state.away_team
    )
    ball_pos = (quantize(state.ball.x, 0.1), quantize(state.ball.y, 0.1))

    return (player_positions, ball_pos, state.turn, state.score_home, state.score_away)

def bfs(initial_state):
    n = 0
    visited = set()
    queue = deque([initial_state])

    while queue:
        current_state = queue.popleft()

        if current_state.goal_test():
            return current_state
        
        state_key = serialize_state(current_state)
        if state_key in visited:
            continue
        visited.add(state_key)

        neighbours = current_state.get_neighbours()
        for neighbor in neighbours:
            queue.append(neighbor)

        n += 1
        if n % 100 == 0:
            print(f"Explored {n} states, queue size: {len(queue)}, visited size: {len(visited)}")

    

if __name__ == "__main__":
    game = Game(num_players_per_team=5)
    # game.show()

    initial_state = game.state
    result_state = bfs(initial_state)

    if result_state:
        print("Goal state found!")
        print(f"Score: Home {result_state.score_home} - Away {result_state.score_away}")
        result_state.show()
    else:
        print("No goal state found.")