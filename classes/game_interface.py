import pygame
import sys
from classes.shogi import Shogi


class Game_interface:
  def __init__(self, screen_width, screen_height, grid_size):
    self.game = Shogi()
    self.running = True
    self.screen_width = screen_width
    self.screen_height = screen_height
    self.grid_size = grid_size
    self.board_square_size = screen_width // grid_size
    
  def configure_screen(self):
    pygame.init()
    self.board_square_image = pygame.image.load('assets/board_square.png')
    self.font = pygame.font.SysFont('Arial', 25)
    self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
    pygame.display.set_caption("Shogi")
    
  def draw_board(self):
    for row in range(self.grid_size):
      for col in range(self.grid_size):
        board_square_image_resized = pygame.transform.scale(self.board_square_image, (self.board_square_size, self.board_square_size))
        self.screen.blit(board_square_image_resized, (col * self.board_square_size + 4, row * self.board_square_size + 4))
        pygame.draw.rect(self.screen, (0, 0, 0), (col * self.board_square_size + 4, row * self.board_square_size + 4, self.board_square_size, self.board_square_size), 2)
    
  def handle_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          x, y = pygame.mouse.get_pos()
          print(x, y)
  
  def run(self):
    self.configure_screen()
    
    while self.running:
      self.screen.fill((255, 203, 93))
      
      self.handle_events()
      self.draw_board()
      
      pygame.display.flip()
      
    pygame.quit()
    sys.exit()
