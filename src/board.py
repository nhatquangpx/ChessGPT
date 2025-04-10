from const import *
from square import Square
from piece import *
from move import Move
class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]

        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def calc_moves(self, piece, row, col):
        '''
        Calculate all possible moves for a piece at a given position.'
        '''

        def pawn_moves():
            #steps
            steps = 1 if piece.moved else 2

            #vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].is_empty():
                        #create initial and final squares of the new move
                        initial = Square(row,col)
                        final = Square(possible_move_row, col)
                        #create new move
                        move = Move(initial, final)
                        piece.add_move(move)
                    #blocked
                    else: break
                #not in range
                else: break

            #diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col - 1, col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        #create square of the new move
                        initial = Square(row,col)
                        final = Square(possible_move_row, possible_move_col)
                        #Create a new move
                        move = Move(initial, final)
                        #append new valid move
                        piece.add_move(move)

        def knight_moves():
            #8 possible moves for knight
            possible_moves = [
                (row + 2, col + 1), (row + 2, col - 1),
                (row - 2, col + 1), (row - 2, col - 1),
                (row + 1, col + 2), (row + 1, col - 2),
                (row - 1, col + 2), (row - 1, col - 2)
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        #create square of the new move
                        initial = Square(row,col)
                        final = Square(possible_move_row, possible_move_col) #piece = piece
                        #create new move
                        move = Move(initial, final)

                        #check potential checks
                        # if bool:
                        #     if not self.in_check(piece, move):
                        #         # append new move
                        #         piece.add_move(move)
                        #     else: break
                        # else:
                        #     # append new move
                        piece.add_move(move)             

        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr
                
                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        #create square of the new move
                        initial = Square(row,col)
                        final = Square(possible_move_row, possible_move_col)
                        #create new move
                        move = Move(initial, final)

                        #empty
                        if self.squares[possible_move_row][possible_move_col].is_empty():
                            piece.add_move(move)

                        #has enemy piece = add move + break
                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            piece.add_move(move)
                            break

                        #has team piece = break
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break

                    #not in range
                    else: break

                    #incrementing incrs
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            pass

        if isinstance(piece, Pawn):
            pawn_moves()
        elif isinstance(piece, Knight):
            knight_moves()
        elif isinstance(piece, Bishop):
            straightline_moves([
                (-1, -1), #up-left
                (-1, 1), #up-right
                (1, -1), #down-left
                (1, 1) #down-right
            ])

        elif isinstance(piece, Rook):
            straightline_moves([
                (-1, 0), #up
                (1, 0), #down
                (0, -1), #left
                (0, 1) #right
            ])
        elif isinstance(piece, Queen):
            straightline_moves([
                (-1, -1), #up-left
                (-1, 1), #up-right
                (1, -1), #down-left
                (1, 1), #down-right
                (-1, 0), #up
                (1, 0), #down
                (0, -1), #left
                (0, 1) #right
            ])
        elif isinstance(piece, King):
            pass

    def _create(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)
    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        #knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))    
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))
        
        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        
        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))