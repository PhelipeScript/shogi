import copy
class Minmax:
    def __init__(self,game,max_height):
        self.game = copy.deepcopy(game)

    def evaluate_tree(self,player,max_height = 5):

        if self.game.check_winner() or max_height == 0:
            return self.game.utility_function()

        if player.color == "BLACK":
            higher_value = ("-inf")
            for next_move in []:
                utility = self.evaluate_tree(self.game.jogar(next_move), False, player, max_height - 1)
                higher_value = max(higher_value, utility)
            return higher_value
        else:
            lowest_value = float("inf")
            for next_move in []:
                utility = self.evaluate_tree(self.game.jogar(next_move), False, player, max_height - 1)
                lowest_value = min(lowest_value, utility)
            return lowest_value
    
    def minimax_alfabeta(self,game,player,max_height = 5,alfa = float("-inf"),beta = float("inf")):
        
        if self.game.check_winner() or max_height == 0:
            return self.game.utility_function()
        
        if player.color == "BLACK":
            for next_move in []:
                utility = self.minimax_alfabeta(game.move_piece,False,player,max_height - 1,alfa,beta)
                alfa = max(utility,alfa)
                if beta <= alfa:
                    continue
                return alfa
        else:
            for next_move in []:
                utility = self.minimax_alfabeta(game.move_piece,False,player,max_height - 1,alfa,beta)
                beta = min(utility,alfa)
                if beta <= alfa:
                    continue
                return beta
            
    def best_agent_move(self,game,player,max_height = 5):
        higher_value = float("-inf")
        best_move = float("-inf")
        for next_move in []:
            actual_player = game.whoPlaysNow;
            utility = 0
            if actual_player == "WHITE":
                utility = self.evaluate_tree(game.move_piece, False,game.players[1], max_height)
            else:
                utility = self.evaluate_tree(game.move_piece, False,game.players[0], max_height)
            if utility > higher_value:
                higher_value = utility
                higher_value = next_move
        return higher_value
