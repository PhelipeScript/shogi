class Board:
  def __init__(self, board_str: str = None):
    # l = Lance
    # n = Cavalo 
    # s = Prata General
    # g = Ouro General
    # k = Rei 
    # b = Bispo 
    # r = Torre 
    # p = Peão 
    # . = Casa vazia
    # w = peao
    # d = dragao
    # t = dragao cavaleiro
    # c = lança promovida
    # h = cavaleiro promovido
    # i = general de prata
    self.board_str = (
      "LNSGKGSNL"  # Linha 1
      ".B.....R."  # Linha 2
      "PPPPPPPPP"  # Linha 3
      "........."  # Linha 4
      "........."  # Linha 5 (Centro do tabuleiro)
      "........."  # Linha 6
      "ppppppppp"  # Linha 7
      ".r.....b."  # Linha 8
      "lnsgkgsnl"  # Linha 9
    ) if board_str is None else board_str
  
  def string_to_array(self):
    return [list(self.board_str[i * 9:(i + 1) * 9]) for i in range(9)]
  
  def print_board(self):
    board_array = self.string_to_array()
    for row in board_array:
      print(" ".join(row))
    pass

  def copy(self):
    return Board(self.board_str)
