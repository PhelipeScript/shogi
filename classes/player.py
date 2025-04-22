from classes.minmax import Minmax
from classes.piece import Piece

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

  def add_piece(self, piece):
    self.pieces.append(piece)
  
  def remove_piece(self, piece):
    if piece in self.pieces:
      self.pieces.remove(piece)
  
  def capture_piece(self, piece):
    if piece.color == "WHITE":
      piece.color = "BLACK"
    else:
      piece.color = "WHITE"
    self.captured_pieces.append(piece)
    
  def copy(self):
    new_player = Player(self.name, self.color)
    new_player.captured_pieces = [piece.copy() for piece in self.captured_pieces]
    return new_player  
  
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
