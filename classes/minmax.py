import copy
class Minmax:

    def evaluate_tree(self,game,player,max_height = 8):

        if game.check_winner() or max_height == 0:
            return game.utility_function()
        
        next_moves = game.possible_states()

        if not next_moves:
            return game.utility_function()

        if game.whoPlaysNow.color == "BLACK":
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
    
    def evaluate_tree_alfabeta(self,game,max_round,max_height,alfa=float("-inf"),beta=float("inf")):

        if game.check_winner() or max_height == 0:
            return game.utility_function()
        
        next_moves = game.possible_states()

        if not next_moves:
            return game.utility_function()

        if max_round: #O jogador preto neste caso é o maximizador
            for  _, _, next_game in next_moves:
                utility = self.evaluate_tree_alfabeta(next_game,False,(max_height - 1),alfa,beta)
                alfa = max(alfa,utility)
                if beta <= alfa:
                    continue
                return alfa
        else:
            for _, _, next_game in next_moves:
                utility = self.evaluate_tree_alfabeta(next_game,True,(max_height - 1),alfa,beta)
                beta = min(beta,utility)
                if beta <= alfa:
                    continue
                return beta
            
    def best_move(self, game, max_height=8):
        best_value = float("-inf")
        best_move = None
        copy_game = game.copy()
        next_moves = copy_game.possible_states()
        
        for piece, piece_copy, next_game in next_moves:
            utility = self.evaluate_tree_alfabeta(next_game,True,max_height)
            
            if copy_game.agent.color == "BLACK":
                if utility >= best_value:
                    best_value = utility
                    best_move = (piece, piece_copy.position)

        if best_move is None:
            print("Não foi possivel determinar o melhor movimento")

        return best_move
