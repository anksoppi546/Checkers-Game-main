import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from .piece import Piece

# Initialise the board condition
class Board:        
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12    # no. of red and white is 12
        self.red_kings = self.white_kings = 0       #no. of kings of red and white
        self.create_board()

    def draw_squares(self, win):
        win.fill(BLACK)     # fills the entire window (represented by the "win" parameter) with a black color
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):     # points to red and white
        return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)

    def get_all_pieces(self,color):
        pieces = []         # store all of the pieces of the specified color
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces


    def move(self, piece, row, col):
        # swap the positions of the current piece with the new position on the game board
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:     # checks if the moved piece has reached the opposite end of the board
            piece.make_king()       # If the piece has reached the opposite end of the board, it is promoted to a king
            # If piece is a white piece, "white_kings" variable is incremented. Otherwise, "red_kings" variable is incremented'''
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):     # checks if col is an odd or even col based on row number
                # The first three rows get pieces of WHITE color, while the last three rows get pieces of RED color'''
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):        # self parameter refers to an instance of the class that this method belongs to
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:      # If there is no piece in cell(i.e., if value of piece is zero), it moves on to next cell
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED

        return None

    def get_valid_moves(self, piece):
        moves = {}
        # represent col indices that are one position to left and one position to right of piece object's current column index, respectively'''
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
        # If piece is either red or a king, then it will update "moves" by traversing left and right 
        # diagonally from current position of piece on board
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))

        return moves
# color : stores information about the player whose turn it is to move
# left : represents no. of squares, player is allowed to move leftwards 
# skipped : optional parameter that defaults to an empty list, store info about any pieces, player has skipped during their move
    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
# checks if there is a piece that was previously skipped in prev. iteration of loop, and whether this is last possible move for that piece
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    # it checks if the rightmost column specified by the 'right' parameter is within the bounds of the game board.
    # If it is outside the bounds, the loop is broken and no further moves are generated'''
    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
            # If there are skipped pieces and last cell checked was not a skipped piece, loop is broken to prevent generating invalid moves'''
                if skipped and not last:
                    break
                    # If there are skipped pieces and last cell checked was a skipped piece, method generates a possible move by 
                    # combining current cell with last cell and skipped pieces. If there are no skipped pieces, method generates a 
                    # possible move by only considering last cell checked'''
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:      #  suggests that the traversal is happening in an upward direction
                # sets value of variable row to max value between r-3 and 0, i.e, traversal process will stop when it 
                # reaches top of board or has reached a distance of three rows from current position, whichever is closer
                        row = max(r-3, 0)       
                    else:
                # sets value of variable row to the min value between r+3 and ROWS, i.e, total no. of rows on board. 
                # means that traversal will stop when it reaches bottom of board or has reached a distance of three rows 
                # from current position, whichever is closer
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]        # keep track of any previously skipped pieces in the traversal process

            right += 1      # keep track of the current column being traversed in the diagonal direction

        return moves