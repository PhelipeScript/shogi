import pygame
import sys
import tkinter as tk
from classes.image_manager import ImageManager
from classes.piece import Piece
from classes.shogi import Shogi


#COLORS
BACKGROUND = (26, 26, 34)
BOARD_COLOR = (44, 72, 117)
CAPTURED_PIECES_COLOR = (209, 179, 196)
GAME_INFO_COLOR = (197, 184, 209)
MOVE_HISTORY_COLOR = (179, 209, 188)
TITLE_COLOR = (148, 148, 162)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HOVER = (240, 227, 204)
SELECTED = (213, 179, 106)
POSSIBLE_MOVE = (77, 123, 196)
POSSIBLE_CAPTURE = (191, 64, 64)
BUTTON_COLOR = (50, 150, 255)
BOARD_COLOR = (224, 165, 49)
BUTTON_HOVER_COLOR = (30, 130, 230)

class GameInterface:
  def __init__(self):
    self.game = Shogi()
    self.image_manager = ImageManager()
    self.board_tile = self.image_manager.load_image('assets/board_tile.png')
    self.captured_tile = self.image_manager.load_image('assets/captured_tile.png')
    self.game_info_tile = self.image_manager.load_image('assets/info_tile.png')
    self.move_history_tile = self.image_manager.load_image('assets/history_tile.png')
    self.fullscreen = False
    self.board = []
    self.capture_display = None
    self.possible_moves = []
    self.GRID_SIZE = 9
    self.promotion_menu_active = False
    
  def configure_screen(self):
    if (self.fullscreen):
      self.screen_width = self.root.winfo_screenwidth()
      self.screen_height = self.root.winfo_screenheight()
      self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
      self.screen_width = max(1200, self.root.winfo_screenwidth() // 2)
      self.screen_height = max(800, self.root.winfo_screenheight() // 2)
      self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
   
    self.FONT_12 = pygame.font.SysFont('Arial', 12)
    self.FONT_16 = pygame.font.SysFont('Arial', 16)
    self.FONT_18 = pygame.font.SysFont('Arial', 18)
    self.FONT_36 = pygame.font.SysFont('Arial', 36)
    pygame.display.set_caption("将棋 (Shogi)")
    self.configure_fullscreen_button()
    self.configure_board()
    self.configure_captured_pieces()
    self.configure_game_info()
    self.configure_move_history()
    
  def configure_board(self):
    self.board_width = 0.50 * self.screen_width
    self.board_height = 0.82 * self.screen_height
    self.board_tile_height = self.board_height // self.GRID_SIZE
    self.board_tile_width = min(self.board_width // self.GRID_SIZE, self.board_tile_height-6)
    
    self.board = []
    board_pieces = self.game.board.string_to_array()
    board_tile_resized = pygame.transform.smoothscale(self.board_tile, (self.board_tile_width, self.board_tile_height))
    for row in range(self.GRID_SIZE):
      for col in range(self.GRID_SIZE):
        x = col * self.board_tile_width + 0.5 * (self.screen_width - self.GRID_SIZE * self.board_tile_width)
        y = row * self.board_tile_height + 0.5 * (self.screen_height - self.GRID_SIZE * self.board_tile_height)
        
        piece = None
        piece_img_resized = None
        if board_pieces[row][col] != '.' and board_pieces[row][col].islower():
          piece = self.game.players[0].get_piece(col + (row * self.GRID_SIZE))
          piece_img_resized = pygame.transform.smoothscale(piece.image, (self.board_tile_width-16, self.board_tile_height-12))
        elif board_pieces[row][col] != '.':
          piece = self.game.players[1].get_piece(col + (row * self.GRID_SIZE))
          piece_img_resized = pygame.transform.smoothscale(piece.image, (self.board_tile_width-16, self.board_tile_height-12))
        
        rect = pygame.Rect(x, y, self.board_tile_width, self.board_tile_height)
        self.board.append({
          "rect": rect, 
          "rect_color": BACKGROUND,
          "piece": piece, 
          "piece_img": piece_img_resized, 
          "tile_img": board_tile_resized,
        })
  
  def draw_board(self):
    for cell in self.board:
      self.screen.blit(cell["tile_img"], cell["rect"].topleft)

      if cell["piece"]:
        piece_rect = cell["piece_img"].get_rect(center=cell["rect"].center)
        self.screen.blit(cell["piece_img"], piece_rect.topleft)

      pygame.draw.rect(self.screen, cell["rect_color"], cell["rect"], 1 if cell["rect_color"] == BLACK else 3)

  def configure_captured_pieces(self):
    self.captured_pieces_title = self.FONT_18.render("PEÇAS CAPTURADAS", True, CAPTURED_PIECES_COLOR)
    captured_grid_size = 5
    self.captured_width = 0.20 * self.screen_width
    self.captured_height = 0.35 * self.screen_height
    self.captured_tile_height = self.captured_height // captured_grid_size
    self.captured_tile_width = min(self.captured_width // captured_grid_size, self.captured_tile_height-6)
    
    self.b_captured_pieces = []
    self.w_captured_pieces = []
    captured_tile_resized = pygame.transform.smoothscale(self.captured_tile, (self.captured_tile_width, self.captured_tile_height))
      
    for i in range(len(self.game.players)):
      for row in range(captured_grid_size):
        for col in range(captured_grid_size):
          if i == 0:
            x = col * self.captured_tile_width + self.screen_width - self.captured_width - captured_grid_size
            y = row * self.captured_tile_height + self.screen_height - self.captured_height - captured_grid_size
            rect = pygame.Rect(x, y, self.captured_tile_width, self.captured_tile_height)
            self.w_captured_pieces.append({
              "rect": rect, 
              "rect_color": BACKGROUND,
              "piece": None, 
              "piece_img": None, 
              "tile_img": captured_tile_resized,
            })
          else:
            x = col * self.captured_tile_width + captured_grid_size
            y = row * self.captured_tile_height + captured_grid_size
            rect = pygame.Rect(x, y, self.captured_tile_width, self.captured_tile_height)
            self.b_captured_pieces.append({
              "rect": rect, 
              "rect_color": BACKGROUND,
              "piece": None, 
              "piece_img": None, 
              "tile_img": captured_tile_resized,
            })
          
        
  def draw_captured_pieces(self):
    for player in self.game.players:
      for i, cell in enumerate(self.w_captured_pieces if player.color == 'WHITE' else self.b_captured_pieces):
        self.screen.blit(cell["tile_img"], cell["rect"].topleft)

        if i > 4 and len(player.captured_pieces) >= i-5+1:
          piece = player.captured_pieces[i-5]
          cell["piece"] = piece
          cell["piece_img"] = pygame.transform.smoothscale(piece.image, (self.captured_tile_width-16, self.captured_tile_height-12))
          piece_rect = cell["piece_img"].get_rect(center=cell["rect"].center)
          self.screen.blit(cell["piece_img"], piece_rect.topleft)

        pygame.draw.rect(self.screen, cell["rect_color"], cell["rect"], 1 if cell["rect_color"] == BACKGROUND else 3)

    # Draw the title for captured black pieces
    title_rect = self.captured_pieces_title.get_rect(center=(self.w_captured_pieces[2]["rect"].centerx, self.w_captured_pieces[2]["rect"].centery))
    self.screen.blit(self.captured_pieces_title, title_rect.topleft)
    
    # Draw the title for captured white pieces
    title_rect = self.captured_pieces_title.get_rect(center=(self.b_captured_pieces[2]["rect"].centerx, self.b_captured_pieces[2]["rect"].centery))
    self.screen.blit(self.captured_pieces_title, title_rect.topleft)
        
  def configure_game_info(self):
    self.game_info_title = self.FONT_18.render("INFORMAÇÕES", True, GAME_INFO_COLOR)
    game_info_grid_size = 5
    self.game_info_width = 0.20 * self.screen_width
    self.game_info_height = 0.35 * self.screen_height
    self.game_info_tile_height = self.game_info_height // game_info_grid_size
    self.game_info_tile_width = min(self.game_info_width // game_info_grid_size, self.game_info_tile_height-6)
    
    self.game_info = []
    game_info_tile_resized = pygame.transform.smoothscale(self.game_info_tile, (self.game_info_tile_width, self.game_info_tile_height))
      
    for row in range(game_info_grid_size):
      for col in range(game_info_grid_size):
        x = col * self.game_info_tile_width + self.screen_width - self.game_info_width - game_info_grid_size
        y = row * self.game_info_tile_height + self.screen_height - 2.2*self.game_info_height - game_info_grid_size
        rect = pygame.Rect(x, y, self.game_info_tile_width, self.game_info_tile_height)
     
        self.game_info.append({
                "rect": rect, 
                "rect_color": BACKGROUND,
                "tile_img": game_info_tile_resized,
              })
        
  def draw_game_info(self):
    for cell in self.game_info:
      self.screen.blit(cell["tile_img"], cell["rect"].topleft)
      pygame.draw.rect(self.screen, cell["rect_color"], cell["rect"], 1)
    
    texts = [
      {"label": "Jogador 1:", "value": self.game.players[0].name},
      {"label": "Jogador 2:", "value": self.game.players[1].name},
      {"label": "Tempo jogador 1:", "value": "5:32"},
      {"label": "Tempo jogador 2:", "value": "10:00"},
      {"label": "Tempo total:", "value": "15:32"},
      {"label": "Rodada atual:", "value": self.game.round+1},
      {"label": "Jogador da vez:", "value": self.game.whoPlaysNow.name},
    ]
    
    for i in range(0, len(texts), 2):
      j = i // 2
      text = self.FONT_16.render(f"{texts[i]['label']} {texts[i]['value']}", True, GAME_INFO_COLOR)
      text_rect = text.get_rect(midleft=(self.game_info[(j+1)*5]["rect"].centerx - self.game_info[(j+1)*5]['rect'].width/3, self.game_info[(j+1)*5]["rect"].top))
      self.screen.blit(text, text_rect.topleft)
      
      if len(texts) > i+1:
        text = self.FONT_16.render(f"{texts[i+1]['label']} {texts[i+1]['value']}", True, GAME_INFO_COLOR)
        text_rect = text.get_rect(midleft=(self.game_info[(j+1)*5]["rect"].centerx - self.game_info[(j+1)*5]['rect'].width/3, self.game_info[(j+1)*5]["rect"].centery))
        self.screen.blit(text, text_rect.topleft)
        
    # Draw the title for game info
    title_rect = self.game_info_title.get_rect(center=(self.game_info[2]["rect"].centerx, self.game_info[2]["rect"].centery))
    self.screen.blit(self.game_info_title, title_rect.topleft)
        
  def configure_move_history(self):
    self.move_history_title = self.FONT_18.render("HISTÓRICO", True, MOVE_HISTORY_COLOR)
    move_history_grid_size = 5
    self.move_history_width = 0.20 * self.screen_width
    self.move_history_height = 0.35 * self.screen_height
    self.move_history_tile_height = self.move_history_height // move_history_grid_size
    self.move_history_tile_width = min(self.move_history_width // move_history_grid_size, self.move_history_tile_height-6)
    
    self.move_history = []
    move_history_tile_resized = pygame.transform.smoothscale(self.move_history_tile, (self.move_history_tile_width, self.move_history_tile_height))
      
    for row in range(move_history_grid_size+3):
      for col in range(move_history_grid_size):
        x = col * self.move_history_tile_width + move_history_grid_size
        y = (row-3) * self.move_history_tile_height + self.screen_height - self.move_history_height - move_history_grid_size
        rect = pygame.Rect(x, y, self.move_history_tile_width, self.move_history_tile_height)
     
        self.move_history.append({
                "rect": rect, 
                "rect_color": BACKGROUND,
                "tile_img": move_history_tile_resized,
              })
  
  def draw_move_history(self):
    for cell in self.move_history:
      self.screen.blit(cell["tile_img"], cell["rect"].topleft)
      pygame.draw.rect(self.screen, cell["rect_color"], cell["rect"], 1)
    
    texts = [
      {"round": 1, "player": self.game.players[0].name, "move": "P de 7g para 7f"},
      {"round": 2, "player": self.game.players[1].name, "move": "N de 2b para 3d promove"},
      {"round": 3, "player": self.game.players[0].name, "move": "B de 8h para 3c captura S"},
      {"round": 4, "player": self.game.players[1].name, "move": "P de 5d para 5c promove e captura G"},
    ]
    
    # TODO: fazer um loop para desenhar os textos e se possível fazer um scroll
    
    # Draw the title for move history
    title_rect = self.move_history_title.get_rect(center=(self.move_history[2]["rect"].centerx, self.move_history[2]["rect"].centery))
    self.screen.blit(self.move_history_title, title_rect.topleft)
    
  
  def handle_possible_moves(self, piece: Piece):
    if not self.game.game_over and piece is not None and piece.color == self.game.whoPlaysNow.color:
      self.possible_moves = self.game.get_piece_moves(piece)
    else:
      self.possible_moves = []
      
  def handle_select_piece(self, piece: Piece):
    if self.game.selected_piece is None:
      self.game.select_piece(piece)
    elif self.game.selected_piece is piece:
      self.game.deselect_piece()
      
  def handle_move_piece(self, new_position: int):
    old_position = self.game.selected_piece.position
    self.game.capture_piece(self.board,new_position)

    old_cell = self.board[old_position]
    new_cell = self.board[new_position]

    if new_cell["piece"] is not None:
      if new_cell["piece"].color != self.game.selected_piece.color:
        self.game.players[0 if self.game.selected_piece.color == 'WHITE' else 1].capture_piece(new_cell["piece"])

    new_cell["piece"] = self.game.selected_piece
    new_cell["piece_img"] = old_cell["piece_img"]
    old_cell["piece"] = None
    old_cell["piece_img"] = None
    
    promoted_piece = self.game.move_piece(new_position)
    if promoted_piece:
      new_cell["piece"] = promoted_piece
      new_cell["piece_img"] = pygame.transform.smoothscale(promoted_piece.image, (self.board_tile_width-16, self.board_tile_height-12))
    else:
      self.promotion_menu_active = self.game.is_promotion_candidate(self.game.promotion_cadidate)
    
  def configure_fullscreen_button(self):
    self.fullscreen_button = pygame.Rect(self.screen_width-166, 16, 150, 16)
    self.fullscreen_button_text = self.FONT_16.render(f"FULLSCREEN: {'ON' if self.fullscreen else 'OFF'}", True, TITLE_COLOR) 
    
  def draw_fullscreen_button(self): 
    pygame.draw.rect(self.screen, BACKGROUND, self.fullscreen_button, border_radius=8)  
    fullscreen_button_center = self.fullscreen_button_text.get_rect(center=self.fullscreen_button.center)
    self.screen.blit(self.fullscreen_button_text, fullscreen_button_center)

  def handle_promotion(self):
    if not self.promotion_menu_active:
        return

    piece = self.game.promotion_cadidate

    index = piece.position
    cell = self.board[index]

    offset_y = -50 if piece.color == "WHITE" else 50
    select_box = pygame.Rect((cell["rect"].x - cell["rect"].width / 2) - 6, cell["rect"].y + offset_y, 100, 50)
    first_option_box = pygame.Rect(select_box.x + 5, select_box.y + 5, 40, 40)
    second_option_box = pygame.Rect(select_box.x + 55, select_box.y + 5, 40, 40)

    pygame.draw.rect(self.screen, BACKGROUND, select_box, border_radius=8)
    pygame.draw.rect(self.screen, WHITE, first_option_box, border_radius=8)
    pygame.draw.rect(self.screen, WHITE, second_option_box, border_radius=8)

    confirm_text = self.FONT_16.render("Yes", True, BLACK)
    cancel_text = self.FONT_16.render("No", True, BLACK)
    self.screen.blit(confirm_text, confirm_text.get_rect(center=first_option_box.center))
    self.screen.blit(cancel_text, cancel_text.get_rect(center=second_option_box.center))

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if first_option_box.collidepoint(self.MOUSE_X, self.MOUSE_Y):
                promoted_piece = self.game.promote_piece(piece)
                self.board[index]["piece"] = promoted_piece
                self.board[index]["piece_img"] = pygame.transform.smoothscale(promoted_piece.image, (self.board_tile_width-16, self.board_tile_height-12))
                self.promotion_menu_active = False
                return
            elif second_option_box.collidepoint(self.MOUSE_X, self.MOUSE_Y):
                self.promotion_menu_active = False
                return

  def draw_winner(self):
    text = self.FONT_36.render(f"{self.game.winner.name} ganhou!", True, TITLE_COLOR)
    text_in_middle_screen = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
    self.screen.blit(text, text_in_middle_screen)
    
  def handle_events(self):
    self.CURRENT_CURSOR = pygame.mouse.get_cursor()
    self.MOUSE_X, self.MOUSE_Y = pygame.mouse.get_pos()

    if self.promotion_menu_active:
      return

    for index, cell in enumerate(self.board):
      if cell["rect"].collidepoint(self.MOUSE_X, self.MOUSE_Y):
        if self.game.selected_piece is None:
          cell["rect_color"] = HOVER
          self.handle_possible_moves(cell["piece"])
      elif cell["piece"] == self.game.selected_piece and cell['piece'] is not None:
        cell["rect_color"] = WHITE
      elif index in self.possible_moves:
        if cell["piece"] is not None:
          cell["rect_color"] = POSSIBLE_CAPTURE
        else:
          cell["rect_color"] = POSSIBLE_MOVE
      else:
        cell["rect_color"] = BLACK
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
      elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if self.fullscreen_button.collidepoint(self.MOUSE_X, self.MOUSE_Y):
          self.fullscreen = not self.fullscreen
          self.configure_screen()
          
        for index, cell in enumerate(self.board):
          if cell["rect"].collidepoint(self.MOUSE_X, self.MOUSE_Y) and cell["piece"]:
            self.handle_select_piece(cell["piece"])

          if cell["rect"].collidepoint(self.MOUSE_X, self.MOUSE_Y) and self.game.selected_piece is not None and index not in self.possible_moves:
            if index is not self.game.selected_piece.position:
              self.game.deselect_piece()
              break

          if cell["rect"].collidepoint(self.MOUSE_X, self.MOUSE_Y) and index in self.possible_moves:
            self.handle_move_piece(index)
            break

    if self.fullscreen_button.collidepoint(self.MOUSE_X, self.MOUSE_Y):
      if self.CURRENT_CURSOR != pygame.SYSTEM_CURSOR_HAND:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
      if self.CURRENT_CURSOR != pygame.SYSTEM_CURSOR_ARROW:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
   

  def run(self):
    self.root = tk.Tk()
    self.root.withdraw()
    pygame.init()
    self.running = True
    self.configure_screen()
    
    while self.running:
      self.screen.fill(BACKGROUND)
      
      self.handle_events()
      self.draw_fullscreen_button()
      self.draw_board()
      self.draw_captured_pieces()
      self.draw_game_info()
      self.draw_move_history()
      self.handle_promotion()
      
      if self.game.game_over:
        self.draw_winner()
      
      pygame.display.flip()
      
    pygame.quit()
    sys.exit()
