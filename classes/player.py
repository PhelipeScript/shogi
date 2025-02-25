class Player:
  def __init__(self, name, color):
    self.name = name
    self.color = color
    self.pieces = []
    self.captured_pieces = []
    pass
  
  def get_piece(self, index):
    for piece in self.pieces:
      if piece.position == index:
        return piece
    

  def add_piece(self, piece):
    self.pieces.append(piece)
    pass
  
  def remove_piece(self, piece):
    self.pieces.remove(piece)
    pass
  
  def capture_piece(self, piece):
    piece.color = self.color
    self.captured_pieces.append(piece)
    pass  
  