from typing import Union

from classes.board import Board
from classes.piece import PIECES_CLASSES, Piece
from classes.player import Player


class Shogi:
  def __init__(self):
    self.board = Board()
    self.players = [Player("Jogador 1", "WHITE"), Player("Jogador 2", "BLACK")]
    self.whoPlaysNow = self.players[0]
    self.round = 0
    self.winner = None
    self.game_over = False
    self.selected_piece = None
    self.promotion_cadidate = None
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

  def get_piece_moves(self, piece: Piece):
    return piece.possible_moves(self.board.board_str)
  
  def select_piece(self, identifier: Union[str, Piece]):
    if self.game_over: return
    
    if isinstance(identifier, str):
      # TODO: caso seja passado as coordenadas da peça (i.e. '00' ou '11')
      pass
    elif isinstance(identifier, Piece):
      if identifier.color == self.whoPlaysNow.color:
        self.selected_piece = identifier
    else:
      print("Peça inválida")
      
  def deselect_piece(self):
    self.selected_piece = None 
    
  # se for obrigatório a promoção, retorna a peça promovida
  # se não for obrigatório a promoção, retorna None
  def move_piece(self, new_position: int) -> Piece | None:
    promoted_piece = None
    old_position = self.selected_piece.position
    piece_symbol = self.board.board_str[old_position]
    
    self.board.board_str = self.board.board_str[:old_position] + '.' + self.board.board_str[old_position+1:]
    self.board.board_str = self.board.board_str[:new_position] + piece_symbol + self.board.board_str[new_position+1:]
    
    self.selected_piece.move(new_position)

    if self.is_mandatory_promotion(self.selected_piece):
      promoted_piece = self.promote_piece(self.selected_piece)
    elif self.is_promotion_candidate(self.selected_piece):
      self.promotion_cadidate = self.selected_piece
    else: 
      self.promotion_cadidate = None

    self.deselect_piece()
    self.next_turn()
    self.board.print_board()
    return promoted_piece
    
  def is_mandatory_promotion(self, piece: Piece):
    if piece.color == "WHITE":
      return piece.position < 9 and (piece.name == 'pawn' or piece.name == 'lance' or piece.name == 'knight') 
    elif piece.color == "BLACK":
      return piece.position > 71 and (piece.name == 'pawn' or piece.name == 'lance' or piece.name == 'knight')
    return False  
  
  def is_promotion_candidate(self, piece: Piece):
    if piece and not piece.promotable and not piece.promotion_offer:
      if piece.color == "WHITE" and piece.position < 27:
        return True
      elif piece.color == "BLACK" and piece.position > 53:
        return True
    return False
  
  def promote_piece(self, piece: Piece) -> Piece | None:
    promoted_piece = piece.promote()
    if promoted_piece:
      self.board.board_str = self.board.board_str[:piece.position] + promoted_piece.symbol + self.board.board_str[piece.position+1:]
      player = self.players[0] if piece.color == "WHITE" else self.players[1]
      player.remove_piece(piece)
      player.add_piece(promoted_piece)
    return promoted_piece
  
  def next_turn(self):
    self.round += 1
    self.whoPlaysNow = self.players[self.round % 2]
    self.check_winner()
    if self.winner is None:
      self.print_turn()
  
  def check_winner(self):
    black_king_alive = self.board.board_str.find('K')
    white_king_alive = self.board.board_str.find('k')
    if black_king_alive == -1 or white_king_alive == -1:
      self.winner = self.players[0 if black_king_alive == -1 else 1]
      self.game_over = True
      self.print_winner()

  def possible_moves(self):
    
    pass

  def check_game_over(self):
    # verifica se o jogo acabou
    pass
  
  def print_winner(self):
    print(f"O vencedor é: {self.winner.name} ({self.winner.color})")  
  
  def print_game_over(self):
    # imprime o fim do jogo
    pass
  
  def print_turn(self):
    print(self.whoPlaysNow.pieces[0].symbol)
    print(f"Rodada {self.round} - Vez do jogador(a): {self.whoPlaysNow.name} ({self.whoPlaysNow.color})")
    pass
  
  
