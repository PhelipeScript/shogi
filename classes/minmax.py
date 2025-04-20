import copy
class Minmax:

    def evaluate_tree(self,game,player,max_height = 8):

        if game.check_winner() or max_height == 0:
            return game.utility_function()
        
        all_moves = game.all_possible_moves()
        next_moves = game.possible_states(all_moves)

        if player.color == "BLACK":
            higher_value = float("-inf")
            for next_move in next_moves:
                utility = self.evaluate_tree(next_move, player, max_height - 1)
                higher_value = max(higher_value, utility)
            return higher_value
        else:
            lowest_value = float("inf")
            for next_move in next_moves:
                utility = self.evaluate_tree(next_move, player, max_height - 1)
                lowest_value = min(lowest_value, utility)
            return lowest_value
    
    def minimax_alfabeta(self,game,player,max_height=8,alfa=float("-inf"),beta=float("inf")):
        
        if game.check_winner() or max_height == 0:
            return game.utility_function()
        
        all_moves = game.all_possible_moves()
        next_moves = game.possible_states(all_moves)

        if player.color == "BLACK":
            value = float("-inf")
            for next_move in next_moves:
                utility = self.minimax_alfabeta(next_move,player,max_height - 1,alfa,beta)
                value = max(value,utility)
                alfa = max(utility,alfa)
                if beta <= alfa:
                    break
                return value
        else:
            value = float("inf")
            for next_move in next_moves:
                utility = self.minimax_alfabeta(next_move,False,player,max_height - 1,alfa,beta)
                value = max(value,utility)
                beta = min(utility,alfa)
                if beta <= alfa:
                    continue
                return value
            
    def best_agent_move(self, game, player, max_height=3):
        higher_value = float("-inf") if player.color == "BLACK" else float("inf")
        best_move = None

        all_moves = game.all_possible_moves()
        next_moves = game.possible_states(all_moves)

        for next_game in next_moves:
            utility = self.evaluate_tree(next_game, player, max_height)
            if player.color == "BLACK":
                if utility > best_value:
                    best_value = utility
                    best_move = next_game
            else:
                if utility < best_value:
                    best_value = utility
                    best_move = next_game
        return best_move