from typing import Union
from classes.board import Board
from classes.piece import PIECES_CLASSES, Piece
from classes.player import Agent, Player


class Shogi:

  def __init__(
      self, board: Board = None, player: Player = None, agent: Agent = None,
      round: int = 0, autostart: bool = True
    ):
    self.player = player if player else Player("Jogador", "WHITE")
    self.agent = agent if agent else Agent("Agente", "BLACK") if self.player.color == "WHITE" else Agent("Agente", "WHITE")
    self.board = Board() if board is None else board
    self.round = round
    self.autostart = autostart

    if autostart:
      self.start()
    
    
  def start(self):
    self.whoPlaysNow = self.player if self.player.color == "WHITE" and self.round % 2 == 0 else self.agent
    self.winner = None
    self.game_over = False
    self.selected_piece = None
    self.promotion_cadidate = None
    self.distribute_pieces()

  def end(self):
    # finaliza o jogo
    pass
  
  def distribute_pieces(self):
    for i, board_piece in enumerate(self.board.board_str):
      if board_piece != '.':
        player = None
        if board_piece.islower():
          player = self.player
        else:
          player = self.agent

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
      player = self.player if piece.color == "WHITE" else self.agent
      player.remove_piece(piece)
      player.add_piece(promoted_piece)
    return promoted_piece
  
  def next_turn(self):
    self.round += 1
    self.whoPlaysNow = self.player if self.player.color == "WHITE" and self.round % 2 == 0 else self.agent
      
    self.check_winner()
    if self.winner is None:
      self.print_turn()
    
    if self.whoPlaysNow == self.agent and not hasattr(self,'ai_move_pending'):
      self.ai_movement()
  
  def check_winner(self):
    black_king_alive = self.board.board_str.find('K')
    white_king_alive = self.board.board_str.find('k')
    if black_king_alive == -1 or white_king_alive == -1:
      self.winner = self.player if self.player.color == "WHITE" and black_king_alive == -1 else self.agent
      self.game_over = True
      self.print_winner()
      return True

  def all_possible_moves(self):
    moves = []
    player_pieces = self.whoPlaysNow.pieces
    for i in range(len(player_pieces)):
      player_moves = player_pieces[i].possible_moves(self.board.board_str)
      if player_moves != []:
        if player_pieces[i].position not in player_moves:
          piece_copy = player_pieces[i].copy()
          moves.append((piece_copy , player_moves))
    return moves
  
  def utility_function(self):
    white_player_pieces = self.player.pieces
    black_player_pieces = self.agent.pieces
    white_total_weight = sum(piece.weight for piece in white_player_pieces)
    black_total_weight = sum(piece.weight for piece in black_player_pieces)
    if self.whoPlaysNow.color == "WHITE":
      return white_total_weight - black_total_weight
    else:
      return black_total_weight - white_total_weight
    
  def possible_states(self,moves):
    all_possible_states = []
    for piece, positions in moves:
      valid_moves = piece.possible_moves(self.board.board_str)
      for position in positions:

        if position not in valid_moves:
          continue

        new_board = self.board.copy()
        new_players = [self.player.copy(),self.agent.copy()]
        new_shogi = Shogi(new_board,new_players[0],new_players[1],self.round, False)
        new_shogi.whoPlaysNow = self.player if self.player.color == "WHITE" and self.round % 2 == 0 else self.agent
        new_shogi.winner = None
        new_shogi.game_over = False
        new_shogi.selected_piece = None
        new_shogi.promotion_cadidate = None

        copied_piece = None
        for p in new_shogi.whoPlaysNow.pieces:
          if p.position == piece.position and p.symbol == piece.symbol:
            copied_piece = p
            break

        if copied_piece is None:
          continue

        new_shogi.select_piece(copied_piece)
        new_shogi.move_piece(position)  
        all_possible_states.append( (copied_piece, position, new_shogi) )

    return all_possible_states

    
  def capture_piece(self,board,new_position):
    if board[new_position]["piece"] is not None:
      if board[new_position]["piece"].color == "BLACK":
        self.agent.remove_piece(board[new_position]["piece"])
        self.player.capture_piece(board[new_position]["piece"])
      else:
        self.player.remove_piece(board[new_position]["piece"])
        self.agent.capture_piece(board[new_position]["piece"])

  def ai_movement(self):
    if self.autostart:
      piece, move = self.agent.best_move(self)
      print(f"Peça movimentada: {piece}")
      print(f"Peça movimento realizado: {move}")

      self.ai_selected_piece = piece
      self.ai_target_position = move
      self.ai_move_pending = True


  def check_game_over(self):
    # verifica se o jogo acabou
    pass
  
  def print_winner(self):
    print(f"O vencedor é: {self.winner.name} ({self.winner.color})")
  
  def print_game_over(self):
    # imprime o fim do jogo
    pass
  
  def print_turn(self):
    #print(f"Rodada {self.round} - Vez do jogador(a): {self.whoPlaysNow.name} ({self.whoPlaysNow.color})")
    pass
  
  def copy(self):
    return Shogi(self.board.copy(), self.player.copy(), self.agent.copy(), self.round)
