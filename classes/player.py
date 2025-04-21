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
    piece.symbol = piece.symbol.lower() if piece.symbol.isupper() else piece.symbol.upper()
    piece.color = self.color
    self.captured_pieces.append(piece)
    
  def copy(self):
    new_player = Player(self.name, self.color)
    new_player.captured_pieces = [piece for piece in self.captured_pieces]
    return new_player  
  