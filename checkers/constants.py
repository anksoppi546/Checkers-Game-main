import pygame

WIDTH, HEIGHT = 650, 650        #  size of the game window in pixels
ROWS, COLS = 8, 8       #  number of rows and columns in the game board
SQUARE_SIZE = WIDTH//COLS       # size of each square on game board, based on window size and no. of rows and columns

# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))
