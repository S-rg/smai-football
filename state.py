class state:
    def __init__(self, team_1, team_2, ball, score_1, score_2):
        self.team_1 = team_1
        self.team_2 = team_2
        self.ball = ball
        self.score_1 = score_1
        self.score_2 = score_2
        self.max_x = 100
        self.max_y = 50
        

    def is_legal(self):
        if len(self.team_1) != 11 or len(self.team_2) != 11:
            return False
        
        if not (0 <= self.score) or not (0 <= self.score_2):
            return False
        
        for player in self.team_1 + self.team_2:
            if not (0 <= player.x <= self.max_x) or not (0 <= player.y <= self.max_y):
                return False
            
        if not (0 <= self.ball.x <= self.max_x) or not (0 <= self.ball.y <= self.max_y):
           if (not self.goal_test()):
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
        pass

    def visualise(self):
        pass

    