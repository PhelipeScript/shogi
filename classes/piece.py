class Piece:
  def __init__(self, name, color, position):
    self.name = name
    self.color = color
    self.position = position
    pass
  
  def move(self, new_position):
    # move a peça para a nova posição
    pass
  
class Pawn(Piece):
  def __init__(self, color, position):
    super().__init__('pawn', color, position)
    pass
  
  def move(self, new_position):
    # movimento especial para peão
    pass
  
class Rook(Piece): 
  def __init__(self, color, position):
    super().__init__('rook', color, position)
    pass
  
  def move(self, new_position):
    # movimento especial para torre
    pass
  
class Knight(Piece):
  def __init__(self, color, position):
    super().__init__('knight', color, position)
    pass
  
  def move(self, new_position):
    # movimento especial para cavalo
    pass
  
class Bishop(Piece):
  def __init__(self, color, position):
    super().__init__('bishop', color, position)
    pass
  
  def move(self, new_position):
    # movimento especial para bispo
    pass
  
class Gold_general(Piece): 
  def __init__(self, color, position):
    super().__init__('gold_general', color, position)
    pass
  
  def move(self, new_position):
    # movimento especial para general de ouro
    pass
  
class Silver_general(Piece):
  def __init__(self, color, position):
    super().__init__('silver_general', color, position)
    pass
  
  def move(self, new_position):
    # movimento especial para general de prata
    pass
  
class King(Piece):
  def __init__(self, color, position):
    super().__init__('king', color, position)
    pass
  
  def move(self, new_position):
    # movimento especial para rei
    pass
  
class Lance(Piece):
  def __init__(self, color, position):
    super().__init__('lance', color, position)
    pass
  
  def move(self, new_position):
    # movimento especial para lança
    pass
