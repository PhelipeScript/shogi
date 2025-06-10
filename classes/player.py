from classes.minmax import Minmax
from classes.piece import Piece
import os
import pickle
import random

class Player:
  def __init__(self, name, color):
    self.name = name
    self.color = color
    self.pieces = []
    self.captured_pieces = []
  
  def get_piece(self, index):
    for piece in self.pieces:
      if piece.position == index:
        return piece

  def add_piece(self, piece: Piece):
    self.pieces.append(piece)
  
  def remove_piece(self, piece: Piece):
    if piece in self.pieces:
      self.pieces.remove(piece)
  
  def capture_piece(self, piece: Piece):
    piece.symbol = piece.symbol.lower() if piece.symbol.isupper() else piece.symbol.upper()
    piece.color = self.color
    piece.toggle_image(self.color)
    self.captured_pieces.append(piece)
    
  def remove_captured_piece(self, piece: Piece):
    if piece in self.captured_pieces:
      self.captured_pieces.remove(piece)
    
  def copy(self):
    new_player = Player(self.name, self.color)
    new_player.captured_pieces = [piece.copy() for piece in self.captured_pieces]
    return new_player  
  
  def captured_pieces_str(self):
    return "".join(sorted(piece.symbol for piece in self.captured_pieces))
  
class Agent(Player):
  def __init__(self, name, color, strategy = Minmax()):
    super().__init__(name, color)
    self.strategy = strategy
  
  def best_move(self, game) -> tuple[Piece, int]:
    return self.strategy.best_move(game)
  
  def copy(self):
    new_agent = Agent(self.name, self.color, self.strategy)
    new_agent.captured_pieces = [piece.copy() for piece in self.captured_pieces]
    return new_agent

class QLearningAgent(Player):
  def __init__(self, name, color, must_load_policy = True):
    super().__init__(name, color)
    if must_load_policy:
      self.load_policy()
  
  def load_policy(self):
    if os.path.exists("data/policy.pkl"):
      with open("data/policy.pkl", "rb") as f:
        self.PI = pickle.load(f)
    else:
      self.PI = {}  

  def best_move(self, game) -> tuple[Piece, int, bool]:
    key = ''.join(game.board.board_str) + f"+{self.captured_pieces_str()}" +("W" if self.color == "WHITE" else "B")
    if key in self.PI:
      piece_identifier, target, is_drop = self.PI[key]  
      piece = None
      if is_drop:
        piece = next((p for p in self.captured_pieces if p.symbol == piece_identifier), None)
      else:
        piece = self.get_piece(piece_identifier)

      if piece:
        return (piece, target, is_drop)
      else:
        return self.choose_random_move(game)
    else:
      return self.choose_random_move(game)
      
  def random_drop_move(self, game) -> tuple[Piece, int, bool] | None: 
    if len(self.captured_pieces) > 0:
      random_piece = random.choice(self.captured_pieces)
      all_drops = game.get_possible_drops(random_piece)
      if len(all_drops) == 0: return None
      random_drop = random.choice(all_drops)
      return (random_piece, random_drop, True)

  def choose_random_move(self, game) -> tuple[Piece, int, bool]:
    random_move = self.random_drop_move(game)
    if random_move:
      return random_move  

    random_piece = random.choice(self.pieces)
    all_moves = random_piece.possible_moves(game.board.board_str)
    while len(all_moves) == 0:
      random_piece = random.choice(self.pieces)
      all_moves = random_piece.possible_moves(game.board.board_str)

    random_target = random.choice(all_moves)
    return (random_piece, random_target, False)
  
  def copy(self, must_load_policy):
    new_qlearning_agent = QLearningAgent(self.name, self.color, must_load_policy)
    new_qlearning_agent.captured_pieces = [piece.copy() for piece in self.captured_pieces]
    return new_qlearning_agent
