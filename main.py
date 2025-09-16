from ball import Ball
from game import Game
from player import Player
from state import State

import time
from collections import deque

def serialize_state(state):
    player_positions = tuple(
        (round(p.x), round(p.y))
        for p in state.home_team + state.away_team
    )
    ball_pos = (round(state.ball.x), round(state.ball.y))

    return (player_positions, ball_pos, state.score_home, state.score_away)


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
        if n % 1000 == 0:
            print(f"Explored {n} states, queue size: {len(queue)}, visited size: {len(visited)}")

def dfs(initial_state):
    n = 0
    visited = set()
    stack = [initial_state]

    while stack:
        current_state = stack.pop()

        if current_state.goal_test():
            return current_state
        
        state_key = serialize_state(current_state)
        if state_key in visited:
            continue
        visited.add(state_key)

        neighbours = current_state.get_neighbours()
        for neighbor in neighbours:
            stack.append(neighbor)

        n += 1
        if n % 1000 == 0:
            print(f"Explored {n} states, stack size: {len(stack)}, visited size: {len(visited)}")

def best_first_search(initial_state):
    n = 0
    visited = set()
    queue = [(initial_state, initial_state.heuristic())]

    while queue:
        queue.sort(key=lambda x: x[1])
        current_state, _ = queue.pop(0)

        if current_state.goal_test():
            return current_state
        
        state_key = serialize_state(current_state)
        if state_key in visited:
            continue
        visited.add(state_key)

        neighbours = current_state.get_neighbours()
        for neighbor in neighbours:
            queue.append((neighbor, neighbor.heuristic()))

        n += 1
        if n % 1000 == 0:
            print(f"Explored {n} states, queue size: {len(queue)}, visited size: {len(visited)}")


def print_all_neighbours(state):
    neighbours = state.get_neighbours()
    for i, neighbor in enumerate(neighbours):
        print(f"Neighbour {i+1}:")
        print(f"  Turn: {neighbor.turn}")
        print(f"  Score: Home {neighbor.score_home} - Away {neighbor.score_away}")
        print(f"  Player positions: {[ (p.x, p.y) for p in neighbor.home_team + neighbor.away_team ]}")
        print(f"  Ball position: ({neighbor.ball.x}, {neighbor.ball.y})")
        print(f"  Player with ball: {[ (p.x, p.y) for p in neighbor.home_team + neighbor.away_team if p.has_possession ]}")
        print()

        if neighbor.ball.x != 50 or neighbor.ball.y != 25:
            print("Ball has moved from the center!")

            break

    

if __name__ == "__main__":
    position_map = {
        'home_team': [(50, 25), (50, 20), (50, 10), (50, 30), (50, 40)],
        'away_team': [(40, 10), (40, 20), (40, 25), (40, 30), (40, 40)]
    }
    game = Game(num_players_per_team=1, position_map=position_map)

    initial_state = game.state
    result_state = best_first_search(initial_state)

    if result_state:
        print("GOAL STATE REACHED!")
    else:
        print("No goal state found.")

    result_state.show()