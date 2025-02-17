from classes.image_manager import ImageManager


class Piece:
  def __init__(self, name, color, position):
    self.name = name
    self.color = color
    self.position = position
    self.image_manager = ImageManager()
    pass
  
  def move(self, new_position):
    # move a peça para a nova posição
    pass
  
  def possible_moves(self):
    # retorna uma lista de posições possíveis para a peça
    pass
  
class Pawn(Piece):
  def __init__(self, color, position):
    super().__init__('pawn', color, position)
    self.image = self.image_manager.load_image('assets/international_pieces/pawn.png')
    pass
  
  def move(self, new_position):
    # movimento especial para peão
    pass
  
  def possible_moves(self, board):
    moves = []
    if (self.color == 'WHITE'):
      if (self.position >= 9) and board[self.position - 9] == '.':
        moves.append(self.position - 9)
    else:
      if (self.position <= 72) and board[self.position + 9] == '.':
        moves.append(self.position + 9)
    return moves
  
class Rook(Piece): 
  def __init__(self, color, position):
    super().__init__('rook', color, position)
    self.image = self.image_manager.load_image('assets/international_pieces/rook.png')
    pass
  
  def move(self, new_position):
    # movimento especial para torre
    pass
  
class Knight(Piece):
  def __init__(self, color, position):
    super().__init__('knight', color, position)
    self.image = self.image_manager.load_image('assets/international_pieces/knight.png')
    pass
  
  def move(self, new_position):
    # movimento especial para cavalo
    pass
  
class Bishop(Piece):
  def __init__(self, color, position):
    super().__init__('bishop', color, position)
    self.image = self.image_manager.load_image('assets/international_pieces/bishop.png')
    pass
  
  def move(self, new_position):
    # movimento especial para bispo
    pass
  
class Gold_general(Piece): 
  def __init__(self, color, position):
    super().__init__('gold_general', color, position)
    self.image = self.image_manager.load_image('assets/international_pieces/gold_general.png')
    pass
  
  def move(self, new_position):
    # movimento especial para general de ouro
    pass
  
class Silver_general(Piece):
  def __init__(self, color, position):
    super().__init__('silver_general', color, position)
    self.image = self.image_manager.load_image('assets/international_pieces/silver_general.png')
    pass
  
  def move(self, new_position):
    # movimento especial para general de prata
    pass
  
class King(Piece):
  def __init__(self, color, position):
    super().__init__('king', color, position)
    self.image = self.image_manager.load_image('assets/international_pieces/king.png')
    pass
  
  def move(self, new_position):
    # movimento especial para rei
    pass
  
class Lance(Piece):
  def __init__(self, color, position):
    super().__init__('lance', color, position)
    self.image = self.image_manager.load_image('assets/international_pieces/lance.png')
    pass
  
  def move(self, new_position):
    # movimento especial para lança
    pass


PIECES_CLASSES = {
    'k': King, 
    'g': Gold_general, 
    'p': Pawn, 
    'r': Rook, 
    'l': Lance,
    'b': Bishop,
    'n': Knight, 
    's': Silver_general, 
}
