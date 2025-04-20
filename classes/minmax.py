import copy
class Minmax:
    def __init__(self,game,max_height):
        self.game = copy.deepcopy(game)
        self.max_height = max_height

    def evaluate_tree(self):
         
         if self.game.check_winner() or self.max_height == 0:
             return
             