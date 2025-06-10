from classes.shogi import Shogi


class ShogiMDP_v2:
    def __init__(self, shogi):
        self.game_over = False
        self.game = shogi
        self.states = []
        self.actions = []
        self.index_state = {}
        self.index_action = {}
        self.process_states()

    def reset_states(self):
        self.states = []
        self.actions = []
        self.index_state = {}
        self.index_action = {}

    def process_states(self):
        self.reset_states()
        encoded_shogi = self.encoding_shogi(self.game)
        self.states.append(encoded_shogi)

        for piece, possible_moves in self.game.all_possible_moves():
            for target in possible_moves:
                action = (piece.position, target)
                self.actions.append(action)
                

    def encoding_shogi(self, shogi) -> str:
        return ''.join(shogi.board.board_str) + ("W" if shogi.who_plays_now.color == "WHITE" else "B")
    
    def T(self, state, action):
        # self.process_states()
        # piece_pos, target = action
        # piece = next((p for p in self.game.who_plays_now.pieces if p.position == piece_pos), None)
        # if piece is None: 
        #     return []

        # current_utility = self.game.utility_function()

        # self.game.select_piece(piece)
        # self.game.move_piece(target)
        # self.game.deselect_piece()
        # self.game.next_turn()

        # next_utility = self.game.utility_function()
        
        # encoded_shogi = self.encoding_shogi(self.game)
        # return [(encoded_shogi, next_utility / current_utility / 100)]
        states = self.all_possible_states()
        current_utility = self.game.utility_function()
        states_and_probs = []

        for encoded_shogy, utility in states:
            if utility == 0: utility = 1
            if current_utility == 0: current_utility = 1

            if utility == -float('inf') or utility == float('inf'):
                continue
            numerator = utility
            denominator = (utility + current_utility) if (utility + current_utility) != 0 else 1
            prob = numerator / denominator / 100
            states_and_probs.append((encoded_shogy, prob))

        if len(states_and_probs) == 0:
            self.game_over = True
        # print("------------------------------")
        # print(states_and_probs)
        return states_and_probs

    def all_possible_states(self): 
        states = []
        for piece, possible_moves in self.game.all_possible_moves():
            for target in possible_moves:
                shogi_copy = self.game.copy()
                piece_copy = next((p for p in shogi_copy.who_plays_now.pieces if p.position == piece.position), None)
                if piece_copy:
                    shogi_copy.select_piece(piece_copy)
                    shogi_copy.move_piece(target)
                    shogi_copy.deselect_piece()
                    shogi_copy.next_turn()
                    states.append((self.encoding_shogi(shogi_copy), shogi_copy.utility_function()))
        # print("------------------------------")
        # print(f"Estados possiveis: {states}")
        # print("------------------------------")
        return states
        
    def R(self, s, a, s_):
        shogi_copy = self.shogi_from_state(s_)
        utility = shogi_copy.utility_function()

        if utility == -float('inf') or utility == float('inf'):
            self.game_over = True

        return shogi_copy.utility_function()
    
    # @staticmethod
    def shogi_from_state(self, state_string: str):
        board_str = state_string[:-1]
        who_plays_now = state_string[-1]

        new_shogi = Shogi()
        new_shogi.board.board_str = board_str
        
        if who_plays_now == "W":
            new_shogi.who_plays_now = new_shogi.player
        else:
            new_shogi.who_plays_now = new_shogi.agent

        new_shogi.replace_pieces()
        # print(f"jogador que joga agora: {who_plays_now}")
        
        return new_shogi

    def next_state(self, action):
        piece_pos, target = action
        piece = next((p for p in self.game.who_plays_now.pieces if p.position == piece_pos), None)
        if piece: 
            self.game.select_piece(piece)
            self.game.move_piece(target)
            self.game.deselect_piece()
        # else: 
            # print(f"Error: {action=}")
        self.game.next_turn()

        if self.game.game_over:
            self.game_over = True

    def restart(self):
        self.game_over = False
        self.game = Shogi()
        self.reset_states()
