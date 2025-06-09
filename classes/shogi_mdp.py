from classes.shogi import Shogi

class ShogiMDP:
    def __init__(self,shogi):
        self.game_over = False
        self.game = shogi
        self.process_states()

    def process_states(self):
        self.states = []
        self.actions = []
        self.index_state = {}
        self.index_action = {}

        encoded_shogi = self.encoding_shogi(self.game)
        self.states.append(encoded_shogi)
        self.index_state[encoded_shogi] = 0

        moves = self.game.all_possible_moves()
        for _, (piece,possible_move) in enumerate(moves):
            for target in  possible_move:
                action = (piece.position,target)
                self.actions.append(action)
                self.index_action[action] = len(self.actions) - 1
        print(self.actions)


    def encoding_shogi(self, shogi) -> str:
        return ''.join(shogi.board.board_str) + ( "W"if shogi.who_plays_now.color == "WHITE" else "B")

    
    def T(self,state_id: int, action_id: int):
        state_str = self.states[state_id]
        action = self.actions[action_id]
        shogi_copy = self.shogi_from_state(state_str)

        print(f"estado string: {state_str}")
        print(f"action: {action}")
        print(f"shogi copy: {shogi_copy}")

        piece_pos, target = action
        print(f"posição da peça a ser movimentada {piece_pos}, {target}")
        piece = next((p for p in self.game.who_plays_now.pieces if p.position == piece_pos),None)
        print(f"Peça movimentada: {piece}")
        if piece is None:
            return []
    
        self.game.select_piece(piece)
        self.game.move_piece(target)
        self.game.deselect_piece()
        self.game.next_turn()
        self.process_states()

        encoded_copy = self.encoding_shogi(self.game)
        if encoded_copy not in self.index_state:
            self.index_state[encoded_copy] = len(self.states)
            self.states.append(encoded_copy)

        return [(self.index_state[encoded_copy], 0.8)]
    
    def R(self, s, a, s_):
        shogi_copy = self.shogi_from_state(self.states[s_])
        utility = shogi_copy.utility_function()

        if  utility == -float('inf') or utility == float('inf'):
            self.game_over = True

        return shogi_copy.utility_function()
    
    @staticmethod
    def shogi_from_state(state_string: str) -> Shogi:
        board_str = state_string[:-1]
        who_plays_now = state_string[-1]

        new_shogi = Shogi()
        new_shogi.board.board_str = board_str
        
        if who_plays_now == "W":
            new_shogi.who_plays_now = new_shogi.player
        else:
            new_shogi.who_plays_now = new_shogi.agent

        new_shogi.replace_pieces()
        print(f"jogador que joga agora: {who_plays_now}")
        
        return new_shogi




        

