from classes.game_interface import Game_interface


# CONTANTES
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GRID_SIZE = 9

game_interface = Game_interface(SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE)

game_interface.run()
