from player import Player
from ball import Ball
from utils import euclidian_distance
from itertools import combinations

directions = [i for i in range(0, 360, 45)]

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

class state:
    def __init__(self, home_team, away_team, ball, score_1, score_2, turn):
        self.home_team = home_team
        self.away_team = away_team
        self.ball = ball
        self.score_1 = score_1
        self.score_2 = score_2
        self.max_x = 100
        self.max_y = 50
        self.turn = 1
        

    def is_legal(self):
        if len(self.home_team) != 11 or len(self.away_team) != 11:
            return False
        
        if not (0 <= self.score) or not (0 <= self.score_2):
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
        if self.ball.x <= 0 or self.ball.x >= self.max_x:
            if (self.max_y / 2 - 7.32 / 2) <= self.ball.y <= (self.max_y / 2 + 7.32 / 2):
                return True
        return False
    

    def update_score(self):
        if self.goal_test():
            if self.ball.x <= 0:
                self.score_2 += 1
            elif self.ball.x >= self.max_x:
                self.score_1 += 1
            self.reset_positions()


    def reset_positions(self):
        for i, pos in enumerate(default_posn_map["home_team"]):
            self.home_team[i].x, self.home_team[i].y = pos
            self.home_team[i].has_possession = False

        for i, pos in enumerate(default_posn_map["away_team"]):
            self.away_team[i].x, self.away_team[i].y = pos
            self.away_team[i].has_possession = False

        self.ball.x, self.ball.y = 50, 25
        self.ball.vx, self.ball.vy = 0, 0
        self.set_possession()

    def visualise(self):
        pass

    def set_possession(self):
        team = self.home_team if self.turn % 2 == 1 else self.away_team
        closest = None
        min_dist = float('inf')

        for player in range(len(team)):
            dist = euclidian_distance(team[player].x, team[player].y, self.ball.x, self.ball.y)
            if dist < min_dist and dist <= possession_radius:
                min_dist = dist
                closest = player

        for p in self.home_team + self.away_team:
            p.has_possession = False

        if closest is not None:
            team[closest].has_possession = True


        
    def copy(self):
        return state(
            self.home_team[:],
            self.away_team[:],
            self.ball,
            self.score_1,
            self.score_2,
            self.turn
        )
    
    def get_neighbours(self):
        neighbours = []

        team = self.home_team if self.turn % 2 == 1 else self.away_team
        for player in range(len(team)):
            for direction in directions:
                new_state = self.copy()
                new_state.home_team[player].move(new_state.home_team[player].sprint_speed, direction)
                new_state.turn += 1
                new_state.update_score()
                if new_state.is_legal():
                    neighbours.append(new_state)

                if new_state.home_team[player].has_possession:
                    for shot_direction in directions:
                        shot_state = new_state.copy()
                        shot_state.home_team[player].shoot(shot_state.ball, shot_direction, shot_state.home_team[player].shot_speed)
                        shot_state.update_score()
                        if shot_state.is_legal():
                            neighbours.append(shot_state)