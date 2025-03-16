import pygame
import sys
import tkinter as tk
from classes.image_manager import ImageManager
from classes.piece import Piece
from classes.shogi import Shogi

GRID_SIZE = 9
ASIDE_GRID  = 3

#COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (235,27,27)
BUTTON_COLOR = (50, 150, 255)
BUTTON_HOVER_COLOR = (30, 130, 230)

class GameInterface:
  def __init__(self):
    self.game = Shogi()
    self.fullscreen = False
    self.board = []
    self.capture_display = None
    self.possible_moves = []
    self.image_manager = ImageManager()
    self.board_square_image = self.image_manager.load_image('assets/board_square.png')
    
  def configure_screen(self):
    if (self.fullscreen):
      self.screen_width = self.root.winfo_screenwidth()
      self.screen_height = self.root.winfo_screenheight()
      self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
      self.screen_width = self.root.winfo_screenwidth() // 1.5
      self.screen_height = self.root.winfo_screenheight() // 1.5
      self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
   
    self.font = pygame.font.SysFont('Arial', 16)
    pygame.display.set_caption("Shogi")
    self.configure_fullscreen_button()
    self.configure_board()
    
  def configure_board(self):
    self.board_width = 0.95 * self.screen_width
    self.board_height = 0.75 * self.screen_height
    self.grid_size = GRID_SIZE
    self.board_square_size = self.board_height // self.grid_size
    self.board = []
    board_pieces = self.game.board.string_to_array()
    board_square_image_resized = pygame.transform.scale(self.board_square_image, (self.board_square_size, self.board_square_size))
    for row in range(self.grid_size):
      for col in range(self.grid_size):
        x = col * self.board_square_size + 0.5 * (self.screen_width - self.grid_size * self.board_square_size)
        y = row * self.board_square_size + 0.5 * (self.screen_height - self.grid_size * self.board_square_size)
        
        piece = None
        piece_img_resized = None
        if board_pieces[row][col] != '.' and board_pieces[row][col].islower():
          piece = self.game.players[0].get_piece(col + (row * self.grid_size))
          piece_img_resized = pygame.transform.scale(piece.image, (self.board_square_size, self.board_square_size))
        elif board_pieces[row][col] != '.':
          piece = self.game.players[1].get_piece(col + (row * self.grid_size))
          piece_img_resized = pygame.transform.scale(piece.image, (self.board_square_size, self.board_square_size))
          piece_img_resized = pygame.transform.rotate(piece_img_resized, 180)
        
        rect = pygame.Rect(x, y, self.board_square_size, self.board_square_size)
        self.board.append({
          "rect": rect, 
          "rect_color": BLACK,
          "piece": piece, 
          "piece_img": piece_img_resized, 
          "tile_img": board_square_image_resized,
        })
  
  def draw_board(self):
    for cell in self.board:
      self.screen.blit(cell["tile_img"], cell["rect"].topleft)

      if cell["piece"]:
        piece_rect = cell["piece_img"].get_rect(center=cell["rect"].center)
        self.screen.blit(cell["piece_img"], piece_rect.topleft)

      pygame.draw.rect(self.screen, cell["rect_color"], cell["rect"], 1 if cell["rect_color"] == BLACK else 3)
        
  def handle_possible_moves(self, piece: Piece):
    if piece is not None:
      self.possible_moves = self.game.get_piece_moves(piece)
    else:
      self.possible_moves = []
      
  def handle_select_piece(self, piece: Piece):
    if self.game.selected_piece is None:
      self.game.select_piece(piece)
    elif self.game.selected_piece is piece:
      print("teste")
      self.game.deselect_piece()
      
  def handle_move_piece(self, new_position: int):
    old_position = self.game.selected_piece.position

    if self.board[new_position]["piece"] is not None:
      if self.board[new_position]["piece"].color == "BLACK":
        self.game.players[0].capture_piece(self.board[new_position]["piece"])
      else:
        self.game.players[1].capture_piece(self.board[new_position]["piece"])

    old_cell = self.board[old_position]
    new_cell = self.board[new_position]

    new_cell["piece"] = self.game.selected_piece
    new_cell["piece_img"] = old_cell["piece_img"]
    old_cell["piece"] = None
    old_cell["piece_img"] = None
    
    self.game.move_piece(new_position)
    
    
  def configure_fullscreen_button(self):
    self.fullscreen_button = pygame.Rect(10, self.screen_height-60, 100, 50)
    self.fullscreen_button_color = BUTTON_COLOR
    self.fullscreen_button_text = self.font.render('Fullscreen', True, WHITE) 
    
  def draw_fullscreen_button(self): 
    pygame.draw.rect(self.screen, self.fullscreen_button_color, self.fullscreen_button, border_radius=8)  
    fullscreen_button_center = self.fullscreen_button_text.get_rect(center=self.fullscreen_button.center)
    self.screen.blit(self.fullscreen_button_text, fullscreen_button_center)
    
  def handle_events(self):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    for index, cell in enumerate(self.board):
      if cell["rect"].collidepoint(mouse_x, mouse_y):
        if self.game.selected_piece is None:
          cell["rect_color"] = WHITE
          self.handle_possible_moves(cell["piece"])
      elif cell["piece"] == self.game.selected_piece and cell['piece'] is not None:
        cell["rect_color"] = WHITE
      elif index in self.possible_moves:
        cell["rect_color"] = RED
      else:
        cell["rect_color"] = BLACK
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
      elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if self.fullscreen_button.collidepoint(mouse_x, mouse_y):
          self.fullscreen = not self.fullscreen
          self.configure_screen()
          
        for index, cell in enumerate(self.board):
          if cell["rect"].collidepoint(mouse_x, mouse_y) and cell["piece"]:
            self.handle_select_piece(cell["piece"])

          if cell["rect"].collidepoint(mouse_x, mouse_y) and self.game.selected_piece is not None and index not in self.possible_moves:
            if index is not self.game.selected_piece.position:
              self.game.deselect_piece()
              break

          if cell["rect"].collidepoint(mouse_x, mouse_y) and index in self.possible_moves:
            self.handle_move_piece(index)
            break

    if self.fullscreen_button.collidepoint(mouse_x, mouse_y):
        self.fullscreen_button_color = BUTTON_HOVER_COLOR
    else:
        self.fullscreen_button_color = BUTTON_COLOR

  def run(self):
    self.root = tk.Tk()
    self.root.withdraw()
    pygame.init()
    self.running = True
    self.game.distribute_pieces()
    self.configure_screen()
    
    while self.running:
      self.screen.fill((255, 203, 93))
      
      self.handle_events()
      self.draw_fullscreen_button()
      self.draw_board()
      self.configure_board()
      #self.draw_aside_board()
      
      pygame.display.flip()
      
    pygame.quit()
    sys.exit()
