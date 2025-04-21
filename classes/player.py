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
    new_player.captured_pieces = [piece for piece in self.captured_pieces]
    return new_player  
  