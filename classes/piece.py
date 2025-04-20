from classes.image_manager import ImageManager
from typing import Union

class Piece:
  def __init__(self, name, color, position):
    self.symbol = ''
    self.name = name
    self.color = color
    self.position = position
    self.promotable = False
    self.promotion_offer = False
    self.image_manager = ImageManager()
    self.weight = 0
    pass
  
  def move(self, new_position):
    self.position = new_position
    pass
  
  def possible_moves(self, board):
    # retorna uma lista de posições possíveis para a peça
    pass

  def promote(self) -> Union['Piece', None]:
    # retorna a nova peça promovida
    pass
  
class Pawn(Piece):
  def __init__(self, color, position):
    super().__init__('pawn', color, position)
    if color == 'WHITE':
      self.image = self.image_manager.load_image('assets/international_pieces/w_pawn.png')
      self.symbol = 'p'
    else:
      self.image = self.image_manager.load_image('assets/international_pieces/b_pawn.png')
      self.symbol = 'P'
    self.weight = 1
  
  def possible_moves(self, board):
    moves = []
    if (self.color == 'WHITE'):
        if (board[self.position - 9] == '.'):
            moves.append(self.position - 9)
        elif board[self.position - 9].isupper():
            moves.append(self.position - 9)
    else:
        if (board[self.position + 9] == '.'):
          moves.append(self.position + 9)
        elif board[self.position + 9].islower():
            moves.append(self.position + 9)
    return moves

  def promote(self):
    return Promoted_pawn(self.color, self.position)
  
class Rook(Piece): 
  def __init__(self, color, position):
    super().__init__('rook', color, position)
    if color == 'WHITE':
      self.image = self.image_manager.load_image('assets/international_pieces/w_rook.png')
      self.symbol = 'r'
    else:
      self.image = self.image_manager.load_image('assets/international_pieces/b_rook.png')
      self.symbol = 'R'
    self.weight = 9

  def possible_moves(self, board):
    moves = []
    row = self.position // 9
    col = self.position % 9

    for i in range(row - 1, -1, -1):
      if board[i * 9 + col] == '.':
        moves.append(i * 9 + col)
      elif (board[i * 9 + col].isupper() and self.color == "WHITE") or (board[i * 9 + col].islower() and self.color == "BLACK"):
          moves.append(i * 9 + col)
          break
      else:
        break

    for i in range(row + 1, 9):
      if board[i * 9 + col] == '.':
        moves.append(i * 9 + col)
      elif (board[i * 9 + col].isupper() and self.color == "WHITE") or (board[i * 9 + col].islower() and self.color == "BLACK"):
          moves.append(i * 9 + col)
          break
      else:
        break

    for i in range(col - 1, -1, -1):
      if board[row * 9 + i] == '.':
        moves.append(row * 9 + i)
      elif (board[row * 9 + i].isupper() and self.color == "WHITE") or (board[row * 9 + i].islower() and self.color == "BLACK"):
          moves.append(row * 9 + i)
          break
      else:
        break

    for i in range(col + 1, 9):
      if board[row * 9 + i] == '.':
        moves.append(row * 9 + i)
      elif (board[row * 9 + i].isupper() and self.color == "WHITE") or (board[row * 9 + i].islower() and self.color == "BLACK"):
          moves.append(row * 9 + i)
          break
      else:
        break

    return moves
  
  def promote(self):
    return Dragon(self.color, self.position)
  
class Knight(Piece):
  def __init__(self, color, position):
    super().__init__('knight', color, position)
    if color == 'WHITE':
      self.image = self.image_manager.load_image('assets/international_pieces/w_knight.png')
      self.symbol = 'n'
    else:
      self.image = self.image_manager.load_image('assets/international_pieces/b_knight.png')
      self.symbol = 'N'
    self.weight = 3
  
  def possible_moves(self, board):
        moves = []
        row = self.position // 9
        col = self.position % 9

        if self.color == 'WHITE':
            if row >= 2 and col >= 1 and board[(row - 2) * 9 + (col - 1)] == '.':
                moves.append((row - 2) * 9 + (col - 1))
            elif row >= 2 and col >= 1 and board[(row - 2) * 9 + (col - 1)].isupper():
                moves.append((row - 2) * 9 + (col - 1))
            if row >= 2 and col <= 7 and board[(row - 2) * 9 + (col + 1)] == '.':
                moves.append((row - 2) * 9 + (col + 1))
            elif row >= 2 and col <= 7 and board[(row - 2) * 9 + (col + 1)].isupper():
                moves.append((row - 2) * 9 + (col + 1))
        else:
            if row <= 6 and col >= 1 and board[(row + 2) * 9 + (col - 1)] == '.':
                moves.append((row + 2) * 9 + (col - 1))
            elif row <= 6 and col >= 1 and board[(row + 2) * 9 + (col - 1)].islower():
                moves.append((row + 2) * 9 + (col - 1))
            if row <= 6 and col <= 7 and board[(row + 2) * 9 + (col + 1)] == '.':
                moves.append((row + 2) * 9 + (col + 1))
            elif row <= 6 and col <= 7 and board[(row + 2) * 9 + (col + 1)].islower():
                moves.append((row + 2) * 9 + (col + 1))
        return moves
  
  def promote(self):
    return Promoted_knight(self.color, self.position)
  
class Bishop(Piece):
  def __init__(self, color, position):
    super().__init__('bishop', color, position)
    if color == 'WHITE':
      self.image = self.image_manager.load_image('assets/international_pieces/w_bishop.png')
      self.symbol = 'b'
    else:
      self.image = self.image_manager.load_image('assets/international_pieces/b_bishop.png')
      self.symbol = 'B'
    self.weight = 7
  
  def possible_moves(self, board):
    moves = []
    row = self.position // 9
    col = self.position % 9

    for i in range(1, 9):
      if row - i >= 0 and col - i >= 0:
        if board[(row - i) * 9 + (col - i)] == '.':
          moves.append((row - i) * 9 + (col - i))
        elif (board[(row - i) * 9 + (col - i)].isupper() and self.color == "WHITE") or (board[(row - i) * 9 + (col - i)].islower() and self.color == "BLACK"):
          moves.append((row - i) * 9 + (col - i))
          break
        else:
          break

    for i in range(1, 9):
      if row - i >= 0 and col + i < 9:
        if board[(row - i) * 9 + (col + i)] == '.':
          moves.append((row - i) * 9 + (col + i))
        elif (board[(row - i) * 9 + (col + i)].isupper() and self.color == "WHITE") or (board[(row - i) * 9 + (col + i)].islower() and self.color == "BLACK"):
          moves.append((row - i) * 9 + (col + i))
          break
        else:
          break

    for i in range(1, 9):
      if row + i < 9 and col - i >= 0:
        if board[(row + i) * 9 + (col - i)] == '.':
          moves.append((row + i) * 9 + (col - i))
        elif (board[(row + i) * 9 + (col - i)].isupper() and self.color == "WHITE") or (board[(row + i) * 9 + (col - i)].islower() and self.color == "BLACK"):
          moves.append((row + i) * 9 + (col - i))
          break
        else:
          break

    for i in range(1, 9):
      if row + i < 9 and col + i < 9:
        if board[(row + i) * 9 + (col + i)] == '.':
          moves.append((row + i) * 9 + (col + i))
        elif (board[(row + i) * 9 + (col + i)].isupper() and self.color == "WHITE") or (board[(row + i) * 9 + (col + i)].islower() and self.color == "BLACK"):
          moves.append((row + i) * 9 + (col + i))
          break
        else:
          break

    return moves
  
  def promote(self):
    return Dragon_knight(self.color, self.position)
  
class Gold_general(Piece): 
  def __init__(self, color, position):
    super().__init__('gold_general', color, position)
    self.promotion_offer = True
    if color == 'WHITE':
      self.image = self.image_manager.load_image('assets/international_pieces/w_gold_general.png')
      self.symbol = 'g'
    else:
      self.image = self.image_manager.load_image('assets/international_pieces/b_gold_general.png')
      self.symbol = 'G'
    self.weight = 10
  
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
          elif (board[(row + i) * 9 + (col + j)].isupper() and self.color == "WHITE") or (board[(row + i) * 9 + (col + j)].islower() and self.color == "BLACK"):
            moves.append((row + i) * 9 + (col + j))
    return moves
  
  def promote(self):
    return None
  
class Silver_general(Piece):
  def __init__(self, color, position):
    super().__init__('silver_general', color, position)
    if color == 'WHITE':
      self.image = self.image_manager.load_image('assets/international_pieces/w_silver_general.png')
      self.symbol = 's'
    else: 
      self.image = self.image_manager.load_image('assets/international_pieces/b_silver_general.png')
      self.symbol = 'S'
    self.weight = 5
  
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
          elif (board[(row + i) * 9 + (col + j)].isupper() and self.color == "WHITE") or (board[(row + i) * 9 + (col + j)].islower() and self.color == "BLACK"): 
            moves.append((row + i) * 9 + (col + j))
    return moves
  
  def promote(self):
    return Promoted_silver(self.color, self.position)
  
class King(Piece):
  def __init__(self, color, position):
    super().__init__('king', color, position)
    if color == 'WHITE':
      self.image = self.image_manager.load_image('assets/international_pieces/w_king.png')
      self.symbol = 'k'
    else:
      self.image = self.image_manager.load_image('assets/international_pieces/b_king.png')
      self.symbol = 'K'
    self.weight = float("-inf")
  
  def possible_moves(self, board):
    moves = []
    row = self.position // 9
    col = self.position % 9
    for i in range(-1, 2):
      for j in range(-1, 2):
        if row + i >= 0 and row + i < 9 and col + j >= 0 and col + j < 9:
          if board[(row + i) * 9 + (col + j)] == '.':
            moves.append((row + i) * 9 + (col + j))
          elif (board[(row + i) * 9 + (col + j)].isupper() and self.color == "WHITE") or (board[(row + i) * 9 + (col + j)].islower() and self.color == "BLACK"):
            moves.append((row + i) * 9 + (col + j))
    return moves

  def promote(self):
    return None
  
class Lance(Piece):
  def __init__(self, color, position):
    super().__init__('lance', color, position)
    if color == 'WHITE':
      self.image = self.image_manager.load_image('assets/international_pieces/w_lance.png')
      self.symbol = 'l'
    else:
      self.image = self.image_manager.load_image('assets/international_pieces/b_lance.png')
      self.symbol = 'L'
    self.weight = 2
  
  def possible_moves(self, board):
    moves = []
    row = self.position // 9
    col = self.position % 9
    if (self.color == 'WHITE'):
      for i in range(row - 1, -1, -1):
        if board[i * 9 + col] == '.':
          moves.append(i * 9 + col)
        elif (board[i * 9 + col].isupper() and self.color == "WHITE") or (board[i * 9 + col].islower() and self.color == "BLACK"):
          moves.append(i * 9 + col)
          break
        else:
          break
    else:
      for i in range(row + 1, 9):
        if board[i * 9 + col] == '.':
          moves.append(i * 9 + col)
        elif (board[i * 9 + col].isupper() and self.color == "WHITE") or (board[i * 9 + col].islower() and self.color == "BLACK"):
          moves.append(i * 9 + col)
          break
        else:
          break
    return moves
  
  def promote(self):
    return Promoted_lance(self.color, self.position)
  
  
class Dragon(Piece):
  def __init__(self,color,position):
    super().__init__('dragon',color,position)
    self.promotion_offer = True
    if color == 'WHITE':
      self.image = self.image_manager.load_image('assets/international_pieces/w_promoted_rook.png')
      self.symbol = 'd'
    else:
      self.image = self.image_manager.load_image('assets/international_pieces/b_promoted_rook.png')
      self.symbol = 'D'
    self.weight = 15

  def possible_moves(self, board):
    moves = []
    row = self.position // 9
    col = self.position % 9

    if (board[self.position - 8].isupper() and self.color == "WHITE") or (board[self.position - 8].islower() and self.color == "BLACK") or (board[self.position - 8] == '.'):
      if col != 8 :
        moves.append(self.position - 8)
    if (board[self.position - 10].isupper() and self.color == "WHITE") or (board[self.position - 10].islower() and self.color == "BLACK") or (board[self.position - 10] == '.'):
      if col != 0 :
        moves.append(self.position - 10)
    if (board[self.position + 8].isupper() and self.color == "WHITE") or (board[self.position + 8].islower() and self.color == "BLACK") or (board[self.position + 8] == '.'):
      if col != 0 :
        moves.append(self.position + 8)
    if (board[self.position + 10].isupper() and self.color == "WHITE") or (board[self.position + 10].islower() and self.color == "BLACK") or (board[self.position + 10] == '.'):
      if col != 8 :
        moves.append(self.position + 10)

    for i in range(row - 1, -1, -1):
      if board[i * 9 + col] == '.':
        moves.append(i * 9 + col)
      elif (board[i * 9 + col].isupper() and self.color == "WHITE") or (board[i * 9 + col].islower() and self.color == "BLACK"):
          moves.append(i * 9 + col)
          break
      else:
        break

    for i in range(row + 1, 9):
      if board[i * 9 + col] == '.':
        moves.append(i * 9 + col)
      elif (board[i * 9 + col].isupper() and self.color == "WHITE") or (board[i * 9 + col].islower() and self.color == "BLACK"):
          moves.append(i * 9 + col)
          break
      else:
        break

    for i in range(col - 1, -1, -1):
      if board[row * 9 + i] == '.':
        moves.append(row * 9 + i)
      elif (board[row * 9 + i].isupper() and self.color == "WHITE") or (board[row * 9 + i].islower() and self.color == "BLACK"):
          moves.append(row * 9 + i)
          break
      else:
        break

    for i in range(col + 1, 9):
      if board[row * 9 + i] == '.':
        moves.append(row * 9 + i)
      elif (board[row * 9 + i].isupper() and self.color == "WHITE") or (board[row * 9 + i].islower() and self.color == "BLACK"):
          moves.append(row * 9 + i)
          break
      else:
        break
    return moves
  
  def promote(self):
    return None

class Dragon_knight(Piece):
  def __init__(self,color,position):
    super().__init__('Dragao Cavaleiro',color,position)
    self.promotion_offer = True
    if color == 'WHITE':
      self.image = self.image_manager.load_image('assets/international_pieces/w_promoted_bishop.png')
      self.symbol = 't'
    else: 
      self.image = self.image_manager.load_image('assets/international_pieces/b_promoted_bishop.png')
      self.symbol = 'T'
    self.weight = 15

  def possible_moves(self, board):
    moves = []
    row = self.position // 9
    col = self.position % 9

    for i in range(-1, 2):
      for j in range(-1, 2):
        if row + i >= 0 and row + i < 9 and col + j >= 0 and col + j < 9:
          if board[(row + i) * 9 + (col + j)] == '.':
            moves.append((row + i) * 9 + (col + j))
          elif (board[(row + i) * 9 + (col + j)].isupper() and self.color == "WHITE") or (board[(row + i) * 9 + (col + j)].islower() and self.color == "BLACK"):
            moves.append((row + i) * 9 + (col + j))

    for i in range(1, 9):
      if row - i >= 0 and col - i >= 0:
        if board[(row - i) * 9 + (col - i)] == '.':
          moves.append((row - i) * 9 + (col - i))
        elif (board[(row - i) * 9 + (col - i)].isupper() and self.color == "WHITE") or (board[(row - i) * 9 + (col - i)].islower() and self.color == "BLACK"):
          moves.append((row - i) * 9 + (col - i))
          break
        else:
          break

    for i in range(1, 9):
      if row - i >= 0 and col + i < 9:
        if board[(row - i) * 9 + (col + i)] == '.':
          moves.append((row - i) * 9 + (col + i))
        elif (board[(row - i) * 9 + (col + i)].isupper() and self.color == "WHITE") or (board[(row - i) * 9 + (col + i)].islower() and self.color == "BLACK"):
          moves.append((row - i) * 9 + (col + i))
          break
        else:
          break

    return moves
  
  def promote(self):
    return None

class Promoted_lance(Piece):
  def __init__(self,color,position):
    super().__init__('Lança Promovida',color,position)
    self.promotion_offer = True
    if color == 'WHITE':
      self.image = self.image_manager.load_image('assets/international_pieces/w_promoted_lance.png')
      self.symbol = 'c'
    else:
      self.image = self.image_manager.load_image('assets/international_pieces/b_promoted_lance.png')
      self.symbol = 'C'
    self.weight = 10

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
          elif (board[(row + i) * 9 + (col + j)].isupper() and self.color == "WHITE") or (board[(row + i) * 9 + (col + j)].islower() and self.color == "BLACK"):
            moves.append((row + i) * 9 + (col + j))
    return moves

  def promote(self):
    return None

class Promoted_knight(Piece):
  def __init__(self,color,position):
    super().__init__('Cavaleiro Promovido',color,position)
    self.promotion_offer = True
    if color == 'WHITE':
      self.image = self.image_manager.load_image('assets/international_pieces/w_promoted_knight.png')
      self.symbol = 'h'
    else:
      self.image = self.image_manager.load_image('assets/international_pieces/b_promoted_knight.png')
      self.symbol = 'H'
    self.weight = 10

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
          elif (board[(row + i) * 9 + (col + j)].isupper() and self.color == "WHITE") or (board[(row + i) * 9 + (col + j)].islower() and self.color == "BLACK"):
            moves.append((row + i) * 9 + (col + j))
    return moves
  
  def promote(self):
    return None

class Promoted_silver(Piece):
  def __init__(self,color,position):
    super().__init__('',color,position)
    self.promotion_offer = True
    if color == 'WHITE':
      self.image = self.image_manager.load_image('assets/international_pieces/w_promoted_silver_general.png')
      self.symbol = 'i'
    else:
      self.image = self.image_manager.load_image('assets/international_pieces/b_promoted_silver_general.png')
      self.symbol = 'I'
    self.weight = 10

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
          elif (board[(row + i) * 9 + (col + j)].isupper() and self.color == "WHITE") or (board[(row + i) * 9 + (col + j)].islower() and self.color == "BLACK"):
            moves.append((row + i) * 9 + (col + j))
    return moves
  
  def promote(self):
    return None

class Promoted_pawn(Piece):
  def __init__(self,color,position):
    super().__init__('promoted_pawn',color,position)
    self.promotion_offer = True
    if color == 'WHITE':
      self.image = self.image_manager.load_image('assets/international_pieces/w_promoted_pawn.png')
      self.symbol = 'w'
    else:
      self.image = self.image_manager.load_image('assets/international_pieces/b_promoted_pawn.png')
      self.symbol = 'W'
    self.weight = 10

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
          elif (board[(row + i) * 9 + (col + j)].isupper() and self.color == "WHITE") or (board[(row + i) * 9 + (col + j)].islower() and self.color == "BLACK"):
            moves.append((row + i) * 9 + (col + j))
    return moves
  
  def promote(self):
    return None
  

PIECES_CLASSES = {
    'k': King, 
    'g': Gold_general,
    'p': Pawn, 
    'r': Rook, 
    'l': Lance,
    'b': Bishop,
    'n': Knight, 
    's': Silver_general,
    'd': Dragon,
    't': Dragon_knight,
    'c': Promoted_lance,
    'h': Promoted_knight,
    'i': Promoted_silver,
    'w': Promoted_pawn
}
