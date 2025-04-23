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
    self.start()
    
    
  def start(self):
    self.who_plays_now = self.player if self.player.color == "WHITE" and self.round % 2 == 0 else self.agent
    self.winner = None
    self.game_over = False
    self.selected_piece = None
    self.selected_piece_to_drop = None
    self.promotion_cadidate = None
    self.player_times = {"WHITE": 0.0, "BLACK": 0.0}
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
      if identifier.color == self.who_plays_now.color:
        self.selected_piece = identifier
        self.selected_piece_to_drop = None
    else:
      print("Peça inválida")
      
  def deselect_piece(self):
    self.selected_piece = None 

  def capture_piece(self, new_position):
    if self.board.board_str[new_position] != '.':
      piece_symbol = self.board.board_str[new_position]
      if piece_symbol.islower(): # se for WHITE peça
        piece = self.player.get_piece(new_position)
        self.agent.capture_piece(piece.antecessor())
        self.player.remove_piece(piece)
      else:
        piece = self.agent.get_piece(new_position)
        self.player.capture_piece(piece.antecessor())
        self.agent.remove_piece(piece)
    
  def select_piece_to_drop(self, piece: Piece):
    if self.game_over: return
    
    self.selected_piece_to_drop = piece
    self.selected_piece = None
  
  def deselect_piece_to_drop(self):
    self.selected_piece_to_drop = None
    
  def drop_piece(self, new_position: int):
    if self.game_over: return
    
    if self.selected_piece_to_drop:
      piece_symbol = self.selected_piece_to_drop.symbol
      self.board.board_str = self.board.board_str[:new_position] + piece_symbol + self.board.board_str[new_position+1:]
      self.selected_piece_to_drop.position = new_position
      player = self.player if self.selected_piece_to_drop.color == "WHITE" else self.agent
      player.remove_captured_piece(self.selected_piece_to_drop)
      player.add_piece(self.selected_piece_to_drop)
    
  # se for obrigatório a promoção, retorna a peça promovida
  # se não for obrigatório a promoção, retorna None
  def move_piece(self, new_position: int) -> Piece | None:
    # verifica se tem alguma peça para ser capturada no proximo movimento
    self.capture_piece(new_position)
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

    if self.autostart:
      self.board.print_board()
    return promoted_piece
  
  def get_possible_drops(self, piece: Piece) -> list[int]:
    return piece.possible_drops(self.board.board_str)
    
  def is_mandatory_promotion(self, piece: Piece):
    if piece.color == "WHITE":
      return piece.position < 9 and (piece.name == 'pawn' or piece.name == 'lance') or piece.position < 18 and piece.name == 'knight' 
    elif piece.color == "BLACK":
      return piece.position > 71 and (piece.name == 'pawn' or piece.name == 'lance') or piece.position > 62 and piece.name == 'knight'
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
  
  def get_time_info(self):
    total = self.player_times["WHITE"] + self.player_times["BLACK"]
    return {
        "Tempo jogador 1": self.format_time(self.player_times["WHITE"]),
        "Tempo jogador 2": self.format_time(self.player_times["BLACK"]),
        "Tempo total": self.format_time(total)
    }

  def format_time(self, seconds):
    m, s = divmod(int(seconds), 60)
    return f"{m}:{s:02d}"

  def next_turn(self):
    self.round += 1
    self.who_plays_now = self.player if self.player.color == "WHITE" and self.round % 2 == 0 else self.agent
      
    self.check_winner()
    if self.winner is None:
      self.print_turn()
    
    if self.who_plays_now == self.agent and not hasattr(self,'ai_move_pending'):
      self.ai_movement()
  
  def check_winner(self):
    black_king_alive = self.board.board_str.find('K')
    white_king_alive = self.board.board_str.find('k')
    if black_king_alive == -1 or white_king_alive == -1:
      self.winner = self.player if self.player.color == "WHITE" and black_king_alive == -1 else self.agent
      self.game_over = True
      self.print_winner()
      return True

  def all_possible_moves(self: "Shogi", player = None) -> list[tuple[Piece, list[int]]]:
    moves = []
    player_pieces = self.who_plays_now.pieces if player is None else player.pieces
    for piece in player_pieces:
      possible_moves = piece.possible_moves(self.board.board_str)
      if possible_moves != [] and piece.position not in possible_moves:
        moves.append((piece, possible_moves))
    return moves
  
  def utility_function(self) -> int:
    white_player_pieces = self.player.pieces
    black_player_pieces = self.agent.pieces

    is_agent_on_check = self.is_on_check(self.agent, self.player)
    is_player_on_check = self.is_on_check(self.player, self.agent)

    black_total_weight = sum(piece.weight for piece in black_player_pieces)
    white_total_weight = sum(piece.weight for piece in white_player_pieces)

    if is_player_on_check:
      # print((black_total_weight - white_total_weight) + 1000)
      return (black_total_weight - white_total_weight) + 1000
    elif is_agent_on_check:
      # print((black_total_weight - white_total_weight) - 1000)
      return (black_total_weight - white_total_weight) - 1000
    else:
      # print(black_total_weight - white_total_weight)
      return black_total_weight - white_total_weight

  def possible_states(self: "Shogi") -> list[tuple[Piece, Piece, "Shogi"]]:
    all_possible_states = []
    for piece, positions in self.all_possible_moves():
      piece_pos = piece.position
      for position in positions:
        shogi_copy = self.copy()
        piece_copy = None

        for p in shogi_copy.who_plays_now.pieces:
          if p.position == piece_pos and p.symbol == piece.symbol:
            piece_copy = p
            break

        if piece_copy:
          shogi_copy.select_piece(piece_copy)
          shogi_copy.move_piece(position)
          if shogi_copy.is_promotion_candidate(piece_copy):
            promote_shogi_copy = shogi_copy.copy()

            for p in promote_shogi_copy.who_plays_now.pieces:
              if p.position == piece_copy.position and p.symbol == piece_copy.symbol:
                promoted_candidate = p
                break

            promote_shogi_copy.promote_piece(promoted_candidate)
            all_possible_states.append((piece, promoted_candidate, shogi_copy))

          all_possible_states.append((piece, piece_copy, shogi_copy))
        
      for idx, cap_piece in enumerate(self.who_plays_now.captured_pieces):
        for drop_position in self.get_possible_drops(piece):
          shogi_copy = self.copy()
          cap_piece_copy = None

          for i, p in enumerate(shogi_copy.who_plays_now.captured_pieces):
            if p.symbol == piece.symbol and i == idx:
              cap_piece_copy = p
              break

          if cap_piece_copy:
            shogi_copy.select_piece_to_drop(cap_piece_copy)
            shogi_copy.drop_piece(drop_position)
            all_possible_states.append((cap_piece, cap_piece_copy, shogi_copy))

    return all_possible_states  

  def ai_movement(self):
    if self.autostart:
      piece, move,is_promoted = self.agent.best_move(self)
      print(f"\nPeça movimentada: {piece.symbol}")
      print(f"movimento realizado: {move}\n")

      if piece in self.agent.captured_pieces:
        self.selected_piece_to_drop = piece

      if is_promoted:
        promoted_piece = self.promote_piece(piece)

      if not self.selected_piece_to_drop:
        self.ai_selected_piece = promoted_piece if is_promoted else piece
      self.ai_target_position = move
      self.ai_move_pending = True


  def is_on_check(self,player,oponent):
    # verifica se o jogador está em xeque
    # se sim, retorna True
    # se não, retorna False
    king_pos = self.board.board_str.find('K') if player.color == "BLACK" else self.board.board_str.find('k')
    if king_pos == -1:
      return False
    
    moves = self.all_possible_moves(oponent)

    for _, positions in moves:
      for position in positions:
        if position == king_pos:
          return True
    return False
    

  def check_game_over(self):
    # verifica se o jogo acabou
    pass
  
  def print_winner(self):
    # print(f"O vencedor é: {self.winner.name} ({self.winner.color})")
    pass
  
  def print_game_over(self):
    # imprime o fim do jogo
    pass
  
  def print_turn(self):
    #print(f"Rodada {self.round} - Vez do jogador(a): {self.who_plays_now.name} ({self.who_plays_now.color})")
    pass
  
  def copy(self):
    return Shogi(self.board.copy(), self.player.copy(), self.agent.copy(), self.round, False)
