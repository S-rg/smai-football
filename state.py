from player import Player
from ball import Ball
from utils import euclidian_distance
from itertools import combinations
import copy
import matplotlib.pyplot as plt

directions = [i for i in range(0, 360, 90)]

default_posn_map = {
    "home_team": [
        (10, 25),
        (30, 10), (30, 20), (30, 30), (30, 40),
        (50, 5), (50, 15), (50, 25), (50, 35), (50, 45),
        (70, 25)
    ],
    "away_team": [
        (90, 25),
        (70, 10), (70, 20), (70, 30), (70, 40),
        (50, 5), (50, 15), (50, 25), (50, 35), (50, 45),
        (30, 25)
    ]
}

possession_radius = 2.0
min_player_sep = 1.0

class State:
    def __init__(self, home_team, away_team, ball, score_home, score_away, turn, position_map=default_posn_map):
        self.home_team = home_team
        self.away_team = away_team
        self.ball = ball
        self.score_home = score_home
        self.score_away = score_away
        self.max_x = 100
        self.max_y = 50
        self.turn = turn
        self.num_players_per_team = len(home_team)
        self.position_map = position_map

        if position_map is None:
            self.position_map = default_posn_map
        

    def is_legal(self):
        if len(self.home_team) != self.num_players_per_team or len(self.away_team) != self.num_players_per_team:
            return False
        
        if self.score_home < 0 or self.score_away < 0:
            return False

        for player in self.home_team + self.away_team:
            if not (0 <= player.x <= self.max_x) or not (0 <= player.y <= self.max_y):
                return False
            
        if not (0 <= self.ball.x <= self.max_x) or not (0 <= self.ball.y <= self.max_y):
           if (not self.goal_test()):
               return False
           
        for p1, p2 in combinations(self.home_team + self.away_team, 2):
            if euclidian_distance(p1.x, p1.y, p2.x, p2.y) < min_player_sep:
                return False
           
        
        
        return True
    

    def goal_test(self):
        if self.score_home >= 1 or self.score_away >= 1: #in case reset_positions is called after goal, remove after testing
            return True
        if self.ball.x <= 0 or self.ball.x >= self.max_x:
            if (self.max_y / 2 - 7.32 / 2) <= self.ball.y <= (self.max_y / 2 + 7.32 / 2):
                return True
        return False
    

    def update_score(self):
        if self.goal_test():
            if self.ball.x <= 0:
                self.score_away += 1
            elif self.ball.x >= self.max_x:
                self.score_home += 1
            self.reset_positions()


    def reset_positions(self, default_posn_map=None):
        if default_posn_map is None:
            default_posn_map = self.position_map if self.position_map is not None else default_posn_map

        for i, pos in enumerate(default_posn_map["home_team"][:self.num_players_per_team]):
            self.home_team[i].x, self.home_team[i].y = pos
            self.home_team[i].has_possession = False

        for i, pos in enumerate(default_posn_map["away_team"][:self.num_players_per_team]):
            self.away_team[i].x, self.away_team[i].y = pos
            self.away_team[i].has_possession = False

        self.ball.x, self.ball.y = 50, 25
        self.set_possession()

    def show(self):
        fig, ax = plt.subplots(figsize=(10, 5))

        ax.set_xlim(0, self.max_x)
        ax.set_ylim(0, self.max_y)
        ax.set_aspect('equal')
        ax.set_facecolor('mediumseagreen')

        ax.plot([self.max_x/2, self.max_x/2], [0, self.max_y], color='white', linewidth=2)

        goal_width = 7.32
        ax.plot([0, 0], [self.max_y/2 - goal_width/2, self.max_y/2 + goal_width/2], color='yellow', linewidth=5)
        ax.plot([self.max_x, self.max_x], [self.max_y/2 - goal_width/2, self.max_y/2 + goal_width/2], color='yellow', linewidth=5)

        home_x = [p.x for p in self.home_team]
        home_y = [p.y for p in self.home_team]
        ax.scatter(home_x, home_y, c='blue', s=100, label='Home Team')

        away_x = [p.x for p in self.away_team]
        away_y = [p.y for p in self.away_team]
        ax.scatter(away_x, away_y, c='red', s=100, label='Away Team')

        ax.scatter(self.ball.x, self.ball.y, c='black', s=50, marker='o', label='Ball')

        for p in self.home_team + self.away_team:
            if hasattr(p, 'has_possession') and p.has_possession:
                ax.annotate('P', (p.x, p.y), color='gold', fontsize=14, fontweight='bold', ha='center', va='center')

        ax.legend(loc='upper right')
        ax.set_title(f'Score: Home {self.score_home} - Away {self.score_away} | Turn: {self.turn}')
        
        plt.show()

    def set_possession(self):
        active_team = self.home_team if self.turn % 2 == 1 else self.away_team
        other_team = self.away_team if self.turn % 2 == 1 else self.home_team

        closest = None
        min_dist = float('inf')

        for idx in range(len(active_team)):
            dist = euclidian_distance(active_team[idx].x, active_team[idx].y, self.ball.x, self.ball.y)
            if dist < min_dist and dist <= possession_radius:
                min_dist = dist
                closest = idx

        if closest is None:
            min_dist = float('inf')
            for idx in range(len(other_team)):
                dist = euclidian_distance(other_team[idx].x, other_team[idx].y, self.ball.x, self.ball.y)
                if dist < min_dist and dist <= possession_radius:
                    min_dist = dist
                    closest = idx
            if closest is not None:
                active_team = other_team

        for p in self.home_team + self.away_team:
            p.has_possession = False

        if closest is not None:
            active_team[closest].has_possession = True

    def round_state(self, decimals=0):
        for player in self.home_team + self.away_team:
            player.x = round(player.x, decimals)
            player.y = round(player.y, decimals)
        self.ball.x = round(self.ball.x, decimals)
        self.ball.y = round(self.ball.y, decimals)
        
    def copy(self):
        return State(
            copy.deepcopy(self.home_team[:]),
            copy.deepcopy(self.away_team[:]),
            copy.deepcopy(self.ball),
            self.score_home,
            self.score_away,
            self.turn
        )
    
    def get_neighbours(self):
        neighbours = []
        active_team = self.home_team if self.turn % 2 == 1 else self.away_team

        for player_idx in range(len(active_team)):
            player = active_team[player_idx]

            if player.has_possession:
                for shot_direction in directions:
                    shot_state = self.copy()
                    shot_active_team = (
                        shot_state.home_team if shot_state.turn % 2 == 1 else shot_state.away_team
                    )

                    shot_active_team[player_idx].shoot(
                        shot_state.ball,
                        shot_direction,
                        shot_active_team[player_idx].shot_speed
                    )

                    shot_state.update_score()
                    shot_state.set_possession()
                    shot_state.turn += 1

                    if shot_state.is_legal():
                        neighbours.append(shot_state)

            for direction in directions:
                new_state = self.copy()
                new_active_team = (
                    new_state.home_team if self.turn % 2 == 1 else new_state.away_team
                )

                new_active_team[player_idx].move(
                    new_active_team[player_idx].sprint_speed, direction
                )
                new_state.turn += 1

                new_state.update_score()
                new_state.set_possession()

                if new_state.is_legal():
                    neighbours.append(new_state)

        return neighbours


    def heuristic(self):
        if self.goal_test():
            return float('inf')

        active_team = self.home_team if self.turn % 2 == 1 else self.away_team
        other_team = self.away_team if self.turn % 2 == 1 else self.home_team

        possessing_player = None
        for player in active_team:
            if player.has_possession:
                possessing_player = player
                break

        if possessing_player is None:
            return 0

        goal_x = 0 if self.turn % 2 == 1 else self.max_x
        goal_y = self.max_y / 2

        dist_to_goal = euclidian_distance(possessing_player.x, possessing_player.y, goal_x, goal_y)
        dist_to_ball = euclidian_distance(possessing_player.x, possessing_player.y, self.ball.x, self.ball.y)

        min_dist_other = float('inf')
        for opponent in other_team:
            dist = euclidian_distance(possessing_player.x, possessing_player.y, opponent.x, opponent.y)
            if dist < min_dist_other:
                min_dist_other = dist

        heuristic_value = (self.max_x + self.max_y) - dist_to_goal + (possession_radius - dist_to_ball) + min_dist_other
        return heuristic_value