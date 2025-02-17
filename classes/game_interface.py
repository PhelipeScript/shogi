import pygame
import sys
import tkinter as tk
from classes.image_manager import ImageManager
from classes.piece import Piece
from classes.shogi import Shogi

GRID_SIZE = 9

#COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BUTTON_COLOR = (50, 150, 255)
BUTTON_HOVER_COLOR = (30, 130, 230)

class GameInterface:
  def __init__(self):
    self.game = Shogi()
    self.fullscreen = False
    self.possible_moves = []
    self.image_manager = ImageManager()
    self.board_square_image = self.image_manager.load_image('assets/board_square.png')
    
  def configure_screen(self):
    if (self.fullscreen):
      self.screen_width = self.root.winfo_screenwidth()
      self.screen_height = self.root.winfo_screenheight()
      self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
      self.screen_width = self.root.winfo_screenwidth() // 2
      self.screen_height = self.root.winfo_screenheight() // 2
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
  
  def draw_board(self):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    board_pieces = self.game.board.string_to_array()
    for row in range(self.grid_size):
      for col in range(self.grid_size):
        piece = None  
        board_square_image_resized = None
        if board_pieces[row][col] == '.':
          board_square_image_resized = pygame.transform.scale(self.board_square_image, (self.board_square_size, self.board_square_size))
        elif board_pieces[row][col].islower():
          piece = self.game.players[0].get_piece(col + (row * self.grid_size))
          board_square_image_resized = pygame.transform.scale(piece.image, (self.board_square_size, self.board_square_size))
        else:
          piece = self.game.players[1].get_piece(col + (row * self.grid_size))
          board_square_image_resized = pygame.transform.scale(piece.image, (self.board_square_size, self.board_square_size))
          board_square_image_resized = pygame.transform.rotate(board_square_image_resized, 180)

        x = col * self.board_square_size + 0.5 * (self.screen_width - self.grid_size * self.board_square_size)
        y = row * self.board_square_size + 0.5 * (self.screen_height - self.grid_size * self.board_square_size)
        self.screen.blit(board_square_image_resized, (x, y))
        piece_rect = pygame.Rect(x, y, self.board_square_size, self.board_square_size)
        if piece_rect.collidepoint(mouse_x, mouse_y):
          self.handle_piece_click(piece, board_pieces[row][col])
        
        if (col + (row * self.grid_size) in self.possible_moves):
          pygame.draw.rect(self.screen, (255, 0, 0), piece_rect, 3)
        else:
          pygame.draw.rect(self.screen, BLACK, piece_rect, 2)
        
  def handle_piece_click(self, piece: Piece, board_piece: str):
    print(board_piece)
    print(self.possible_moves)
    if piece is not None and piece.name == 'king':
      self.possible_moves = self.game.get_piece_moves(piece)
    else:
      self.possible_moves = []
    
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
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
      elif event.type == pygame.VIDEORESIZE:
        self.configure_screen()
      elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if self.fullscreen_button.collidepoint(mouse_x, mouse_y):
          self.fullscreen = not self.fullscreen
          self.configure_screen()

    if self.fullscreen_button.collidepoint(mouse_x, mouse_y):
        self.fullscreen_button_color = BUTTON_HOVER_COLOR
    else:
        self.fullscreen_button_color = BUTTON_COLOR

  def run(self):
    self.root = tk.Tk()
    self.root.withdraw()
    pygame.init()
    self.running = True
    self.configure_screen()
    self.game.distribute_pieces()
    
    while self.running:
      self.screen.fill((255, 203, 93))
      
      self.handle_events()
      self.draw_fullscreen_button()
      self.draw_board()
      
      pygame.display.flip()
      
    pygame.quit()
    sys.exit()
