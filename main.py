import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED , WHITE
from checkers.game import Game
from minimax.algorithm import minimax

FPS = 90

WIN = pygame.display.set_mode((WIDTH, HEIGHT))      # initializes game window with specified width and height.
pygame.display.set_caption('Checkers')      #  set the title of the game window

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE      # give us the row index of the square in a grid of squares
    col = x // SQUARE_SIZE      # give us the col index of the square in a grid of squares
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()     # control the framerate of the game.
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.turn == WHITE :
            # game.get_board(): the current state of the game board
            # 5: the maximum depth to search in the game tree (i.e., the number of moves ahead to consider)
            # True: indicating whether this is the maximizing player (i.e., the AI player)
            # game: make recursive calls to itself
            value , new_board = minimax(game.get_board() ,3,float('-inf') , float('inf') ,True ,game)
            game.ai_move(new_board)

        if game.winner() != None:
            print(game.winner())
            run = False

        for event in pygame.event.get():        # get a list of all events that have occurred since last time it was called
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()        # detect position by clicking mouse
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)       
        game.update()       # updates the game state based on the user's input


    pygame.quit()

main()