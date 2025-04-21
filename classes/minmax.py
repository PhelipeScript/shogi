import copy
class Minmax:

    def evaluate_tree(self,game,player,max_height = 8):

        if game.check_winner() or max_height == 0:
            return game.utility_function()
        
        all_moves = game.all_possible_moves()
        next_moves = game.possible_states(all_moves)

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
    
    def evaluate_tree_alfabeta(self,game,player,max_height=8,alfa=float("-inf"),beta=float("inf")):
        
        if game.check_winner() or max_height == 0:
            return game.utility_function()
        
        all_moves = game.all_possible_moves()
        next_moves = game.possible_states(all_moves)

        if not next_moves:
            return game.utility_function()

        if game.whoPlaysNow.color == "BLACK": #O jogador preto neste caso é o maximizador
            value = float("-inf")
            for _ , _,next_move in next_moves:
                utility = self.evaluate_tree_alfabeta(next_move,player,max_height - 1,alfa,beta)
                value = max(value,utility)
                alfa = max(alfa,value)
                if beta <= alfa:
                    break
            return value
        else:
            value = float("inf")
            for next_move in next_moves:
                utility = self.evaluate_tree_alfabeta(next_move,player,max_height - 1,alfa,beta)
                value = min(value,utility)
                beta = min(beta,value)
                if alfa >= beta:
                    break
            return value
            
    def best_agent_move(self, game, player, max_height=3):
        best_value = float("-inf")
        best_move = None
        copy_game = game.copy()
        all_moves = copy_game.all_possible_moves()
        next_moves = copy_game.possible_states(all_moves)

        if not next_moves:
            return None
        
        piece_map = {id(copy_piece): original_piece for copy_piece, original_piece in zip(copy_game.players[1].pieces, game.players[1].pieces)}
        for piece,position,next_game in next_moves:
            utility = self.evaluate_tree_alfabeta(next_game, player, max_height)

            original_piece = piece_map.get(id(piece))
            if player.color == "BLACK":
                if utility > best_value:
                    best_value = utility
                    best_move = (original_piece,position)
            else:
                if utility < best_value:
                    best_value = utility
                    best_move = (original_piece,position)

        if best_move is None:
            print("Não foi possivel determinar o melhor movimento")

        return best_move