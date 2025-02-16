from classes.board import Board
from classes.piece import PIECES_CLASSES, Piece
from classes.player import Player


class Shogi:
  def __init__(self):
    self.board = Board()
    self.players = [Player("Jogador 1", "branco"), Player("Jogador 2", "preto")]
    self.turn = 0
    self.winner = None
    self.game_over = False
    print("iniciando o jogo")
    self.board.print_board()
    
  def start(self):
    # inicia o loop do jogo
    pass

  def end(self):
    # finaliza o jogo
    pass
  
  def distribute_pieces(self):
    for i, board_piece in enumerate(self.board.board_str):
      if board_piece != '.':
        player = None
        if board_piece.islower():
          player = self.players[0]
        else:
          player = self.players[1]

        new_piece = PIECES_CLASSES[board_piece.lower()](player.color, i)
        player.add_piece(new_piece)

  
  def next_turn(self):
    # passa a vez
    pass
  
  def check_winner(self):
    # verifica se há um vencedor
    pass
  
  def check_game_over(self):
    # verifica se o jogo acabou
    pass
  
  def print_winner(self):
    # imprime o vencedor
    pass
  
  def print_game_over(self):
    # imprime o fim do jogo
    pass
  
  def print_turn(self):
    # imprime a vez do jogador
    pass
  
  
