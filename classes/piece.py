from classes.image_manager import ImageManager


class Piece:
  def __init__(self, name, color, position):
    self.name = name
    self.color = color
    self.position = position
    self.image_manager = ImageManager()
    pass
  
  def move(self, new_position):
    self.position = new_position
    pass
  
  def possible_moves(self, board):
    # retorna uma lista de posições possíveis para a peça
    pass
  
class Pawn(Piece):
  def __init__(self, color, position):
    super().__init__('pawn', color, position)
    self.image = self.image_manager.load_image('assets/international_pieces/pawn.png')
    pass
  
  def possible_moves(self, board):
    moves = []
    if (self.color == 'WHITE'):
        moves.append(self.position - 9)
    else:
        moves.append(self.position + 9)
    return moves
  
class Rook(Piece): 
  def __init__(self, color, position):
    super().__init__('rook', color, position)
    self.image = self.image_manager.load_image('assets/international_pieces/rook.png')
    pass

  def possible_moves(self, board):
    moves = []
    row = self.position // 9
    col = self.position % 9

    print(self.color)

    for i in range(row - 1, -1, -1):
      if board[i * 9 + col] == '.':
        moves.append(i * 9 + col)
      else:
        if (board[i * 9 + col].isupper() and self.color == "WHITE") or (board[i * 9 + col].islower() and self.color == "BLACK"):
          moves.append(i * 9 + col)
        break
    for i in range(row + 1, 9):
      if board[i * 9 + col] == '.':
        moves.append(i * 9 + col)
      else:
        if (board[i * 9 + col].isupper() and self.color == "WHITE") or (board[i * 9 + col].islower() and self.color == "BLACK"):
          moves.append(i * 9 + col)
        break
    for i in range(col - 1, -1, -1):
      if board[row * 9 + i] == '.':
        moves.append(row * 9 + i)
      else:
        if (board[row * 9 + i].isupper() and self.color == "WHITE") or (board[row * 9 + i].islower() and self.color == "BLACK"):
          moves.append(row * 9 + i)
        break
    for i in range(col + 1, 9):
      if board[row * 9 + i] == '.':
        moves.append(row * 9 + i)
      else:
        if (board[row * 9 + i].isupper() and self.color == "WHITE") or (board[row * 9 + i].islower() and self.color == "BLACK"):
          moves.append(row * 9 + i)
        break
    return moves
  
class Knight(Piece):
  def __init__(self, color, position):
    super().__init__('knight', color, position)
    self.image = self.image_manager.load_image('assets/international_pieces/knight.png')
    pass
  
  def possible_moves(self, board):
    moves = []  # pos = 65
    row = self.position // 9 # 7
    col = self.position % 9 # 2
    if (self.color == 'WHITE'):
      if (row >= 2 and col >= 1) and board[(row - 2) * 9 + (col - 1)] == '.':
        moves.append((row - 2) * 9 + (col - 1))
      if (row >= 2 and col <= 7) and board[(row - 2) * 9 + (col + 1)] == '.':
        moves.append((row - 2) * 9 + (col + 1))
    else:
      if (row <= 6 and col >= 1) and board[(row + 2) * 9 + (col - 1)] == '.':
        moves.append((row + 2) * 9 + (col - 1))
      if (row <= 6 and col <= 7) and board[(row + 2) * 9 + (col + 1)] == '.':
        moves.append((row + 2) * 9 + (col + 1))
    return moves
  
  
class Bishop(Piece):
  def __init__(self, color, position):
    super().__init__('bishop', color, position)
    self.image = self.image_manager.load_image('assets/international_pieces/bishop.png')
    pass
  
  def possible_moves(self, board):
    moves = []
    row = self.position // 9
    col = self.position % 9
    for i in range(1, 9):
      if row - i >= 0 and col - i >= 0:
        if board[(row - i) * 9 + (col - i)] == '.':
          moves.append((row - i) * 9 + (col - i))
        else:
          break
      else:
        break
    for i in range(1, 9):
      if row - i >= 0 and col + i < 9:
        if board[(row - i) * 9 + (col + i)] == '.':
          moves.append((row - i) * 9 + (col + i))
        else:
          break
      else:
        break
    for i in range(1, 9):
      if row + i < 9 and col - i >= 0:
        if board[(row + i) * 9 + (col - i)] == '.':
          moves.append((row + i) * 9 + (col - i))
        else:
          break
      else:
        break
    for i in range(1, 9):
      if row + i < 9 and col + i < 9:
        if board[(row + i) * 9 + (col + i)] == '.':
          moves.append((row + i) * 9 + (col + i))
        else:
          break
      else:
        break
    return moves
  
class Gold_general(Piece): 
  def __init__(self, color, position):
    super().__init__('gold_general', color, position)
    self.image = self.image_manager.load_image('assets/international_pieces/gold_general.png')
    pass
  
  def possible_moves(self, board):
    moves = []
    row = self.position // 9
    col = self.position % 9
    for i in range(-1, 2):
      for j in range(-1, 2):
        evitar_index = 1 if self.color == 'WHITE' else -1
        if i == evitar_index and (j == -1 or j == 1):
          continue
        if row + i >= 0 and row + i < 9 and col + j >= 0 and col + j < 9:
          if board[(row + i) * 9 + (col + j)] == '.':
            moves.append((row + i) * 9 + (col + j)) 
    return moves
  
class Silver_general(Piece):
  def __init__(self, color, position):
    super().__init__('silver_general', color, position)
    self.image = self.image_manager.load_image('assets/international_pieces/silver_general.png')
    pass
  
  def possible_moves(self, board):
    moves = []
    row = self.position // 9
    col = self.position % 9
    for i in range(-1, 2):
      for j in range(-1, 2):
        evitar_index = 1 if self.color == 'WHITE' else -1
        if i == 0 and (j == -1 or j == 1) or i == evitar_index and j == 0:
          continue
        if row + i >= 0 and row + i < 9 and col + j >= 0 and col + j < 9:
          if board[(row + i) * 9 + (col + j)] == '.':
            moves.append((row + i) * 9 + (col + j)) 
    return moves
  
class King(Piece):
  def __init__(self, color, position):
    super().__init__('king', color, position)
    self.image = self.image_manager.load_image('assets/international_pieces/king.png')
    pass
  
  def possible_moves(self, board):
    moves = []
    row = self.position // 9
    col = self.position % 9
    for i in range(-1, 2):
      for j in range(-1, 2):
        if row + i >= 0 and row + i < 9 and col + j >= 0 and col + j < 9:
          if board[(row + i) * 9 + (col + j)] == '.':
            moves.append((row + i) * 9 + (col + j))
    return moves
  
class Lance(Piece):
  def __init__(self, color, position):
    super().__init__('lance', color, position)
    self.image = self.image_manager.load_image('assets/international_pieces/lance.png')
    pass
  
  def possible_moves(self, board):
    moves = []
    row = self.position // 9
    col = self.position % 9
    if (self.color == 'WHITE'):
      for i in range(row - 1, -1, -1):
        if board[i * 9 + col] == '.':
          moves.append(i * 9 + col)
        else:
          break
    else:
      for i in range(row + 1, 9):
        if board[i * 9 + col] == '.':
          moves.append(i * 9 + col)
        else:
          break
    return moves


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
