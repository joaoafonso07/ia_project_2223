# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# ist1102779 João Afonso Mestre
# ist1 Miguel Benjamim 

import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

board_size = 10
board_pieces = ('W', 'C', 'T', 'M', 'B', 'L', 'R')


def valid_coord(row, col):
    return row < board_size and row >= 0 and col < board_size and col >= 0
         

class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""
    
    def __init__(self, row_restritions:tuple, empty_in_row: list, column_restritions: tuple, empty_in_col: list, grid, boats):
        self.row_restritions = row_restritions
        self.empty_in_row = empty_in_row
        self.column_restritions = column_restritions
        self.empty_in_col = empty_in_col
        self.grid = grid
        self.boats = boats

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if not valid_coord(row, col):
            return -1
        return self.grid[row][col]

    def adjacent_vertical_values(self, row: int, col: int):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if not valid_coord(row, col):
            return -1
        elif row == board_size:
            return (self.grid[row-1][col], None)
        elif row == 0:
            return (None, self.grid[row+1][col])
        else:
            return (self.grid[row-1][col], self.grid[row+1][col])

    def adjacent_horizontal_values(self, row: int, col: int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if not valid_coord(row, col):
            return -1
        elif col == board_size:
            return (self.grid[row][col-1], None)
        elif col == 0:
            return (None, self.grid[row+1][col])
        else:
            return (self.grid[row][col-1], self.grid[row][col+1])

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """
        str_row = sys.stdin.readline().split()
        row_restritions = tuple(map(int, str_row[1:]))

        str_col = sys.stdin.readline().split()
        column_restritions = tuple(map(int, str_col[1:]))

        numb_of_hints = int(sys.stdin.readline())

        grid = []

        for e in range(board_size):
            grid.append(['.','.','.','.','.','.','.','.','.','.'])

        empty_in_row = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
        empty_in_col = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

        for e in range(numb_of_hints):
            hint = sys.stdin.readline().split()

            row = int(hint[1])
            empty_in_row[row] -= 1

            col = int(hint[2])
            empty_in_col[col] -= 1

            grid[row][col] = hint[3]

        boats = {"boat1": 4, "boat2": 3, "boat3": 2, "boat4": 1}

        for row in range(board_size):
            for col in range(board_size):
                piece = board.grid[row][col]
                if piece == 'C':
                    boats['boat1'] -= 1
                    if row == 0:
                        if col == 0:
                            board.grid[row+1][col] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                        elif col == 9:
                            board.grid[row+1][col] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                        else:
                            board.grid[row][col-1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                    elif row == 9:
                        if col == 0:
                            board.grid[row-1][col] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row-1][col+1] = 'W'
                        elif col == 9:
                            board.grid[row-1][col] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row-1][col-1] = 'W'
                        else:
                            board.grid[row][col-1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-1][col+1] = 'W'
                    else:
                        if col == 0:
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+1][col] = 'W'
                        elif col == 9:
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col] = 'W'
                        else:
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row-1][col+1] = 'W'

                elif piece == 'T':
                    if row == 0:
                        if col == 0:
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+2][col+1] = 'W'
                        elif col == 9:
                            board.grid[row][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+2][col-1] = 'W'
                        else:
                            board.grid[row][col-1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+2][col-1] = 'W'
                            board.grid[row+2][col+1] = 'W'
                    elif row == 8:
                        if col == 0:
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+1][col] = 'B'
                            boats['boat2'] -= 1
                            
                        elif col == 9:
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col] = 'B'
                            boats['boat2'] -= 1
                        else:
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col] = 'B'
                            boats['boat2'] -= 1
                    elif row == 9:
                        return None
                    else:
                        if col == 0:
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+2][col+1] = 'W'
                        elif col == 9:
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+2][col-1] = 'W'
                        else:
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+2][col-1] = 'W'
                            board.grid[row+2][col+1] = 'W'

                elif piece == 'B':
                    if row == 0:
                        return None
                    elif row == 1:
                        if col == 0:
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row-1][col] = 'T'
                            boats['boat2'] -= 1
                            
                        elif col == 9:
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-1][col] = 'T'
                            boats['boat2'] -= 1
                        else:
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row-1][col] = 'T'
                            boats['boat2'] -= 1

                    elif row == 9:
                        if col == 0:
                            board.grid[row][col+1] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row-2][col+1] = 'W'
                        elif col == 9:
                            board.grid[row][col-1] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-2][col-1] = 'W'
                        else:
                            board.grid[row][col-1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row-2][col-1] = 'W'
                            board.grid[row-2][col+1] = 'W'                       
                    else:
                        if col == 0:
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row-2][col+1] = 'W'
                        elif col == 9:
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-2][col-1] = 'W'
                        else:
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row-2][col-1] = 'W'
                            board.grid[row-2][col+1] = 'W'

                elif piece == 'L':
                    if col == 0:
                        if row == 0:
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+1][col+2] = 'W'
                        elif row == 9:
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row-1][col+2] = 'W'
                        else:
                            board.grid[row-1][col] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row-1][col+2] = 'W'
                            board.grid[row+1][col+2] = 'W'
                    elif col == 8:
                        if row == 0:
                            board.grid[row][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row][col+1] = 'R'
                            boats['boat2'] -= 1
                            
                        elif row == 9:
                            board.grid[row][col-1] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row][col+1] = 'R'
                            boats['boat2'] -= 1
                        else:
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row][col+1] = 'R'
                            boats['boat2'] -= 1
                    elif col == 9:
                        return None
                    else:
                        if row == 0:
                            board.grid[row][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+1[col+2]] = 'W'
                        elif row == 9:
                            board.grid[row][col-1] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row-1][col+2] = 'W'
                        else:
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row-1][col] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row-1][col+2] = 'W'
                            board.grid[row+1][col+2] = 'W'

                elif piece == 'R':
                    if col == 0:
                        return None
                    
                    elif col == 1:
                        if row == 0:
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row][col-1] = 'L'
                            boats['boat2'] -= 1
                            
                        elif row == 9:
                            board.grid[row][col+1] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row][col-1] = 'L'
                            boats['boat2'] -= 1
                        else:
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row][col-1] = 'R'

                    if col == 9:
                        if row == 0:
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col-2] = 'W'
                        elif row == 9:
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-1][col-2] = 'W'
                        else:
                            board.grid[row-1][col] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row-1][col-2] = 'W'
                            board.grid[row+1][col-2] = 'W'  
                            boats['boat2'] -= 1
                    
                    else:
                        if row == 0:
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1[col-2]] = 'W'
                        elif row == 9:
                            board.grid[row][col+1] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-1][col-2] = 'W'
                        else:
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row-1][col] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row-1][col-2] = 'W'
                            board.grid[row+1][col-2] = 'W'    

                elif piece == 'M':
                    if row == 0:
                        if col == 0 or col == 9:
                            return None  
                        elif col == 1:
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row][col-1] = 'L'
                        elif col == 8:
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row][col+1] = 'R'
                        else:
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col-2] = 'W'
                            board.grid[row+1][col+2] = 'W'
                            
                        #NOT FINISHED [DOWN]

                    elif row == 1:
                        if col == 0:
                            return None
                            
                        elif col == 9:
                            return None
                        else:
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row-1][col] = 'T'
                            boats['boat2'] -= 1

                    elif row == 8:
                        if col == 0:
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+1][col] = 'B'
                            boats['boat2'] -= 1
                            
                        elif col == 9:
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col] = 'B'
                            boats['boat2'] -= 1
                        else:
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col] = 'B'
                            boats['boat2'] -= 1
                    elif row == 9:
                        return None
                    else:
                        if col == 0:
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+2][col+1] = 'W'
                        elif col == 9:
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+2][col-1] = 'W'
                        else:
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+2][col-1] = 'W'
                            board.grid[row+2][col+1] = 'W'           
        
        return Board(row_restritions = row_restritions, empty_in_row = empty_in_row, column_restritions = column_restritions, empty_in_col = empty_in_col, grid = grid, boats = boats)
    
    def print(self):
        for row in self.grid:
            for i in row:
                print(i, end='')
            print('\n')
    


    # 1 if cell (row, col) contains symbol piece, 0 otherwise (x), -1 in case of error (x)
    def is_value(self, row, col, piece): 
        if not valid_coord(row, col):
            return -1
        if self.get_value(row, col) == piece:
            return 1
        else:
            return 0
        
    #denotes the number of boats that has to be placed in the grid for each sort (S)
    def available_boats(self, boat): 
        return self.boats[boat]
    
    #1 if a boats of length l starts (i.e., has symbol L, T, or C) in cell (row, col), 0 otherwise, -1 in case of error (s)
    def boat_start(self, row, col, l):
        if not valid_coord(row, col):
            return -1
        start_piece = self.grid[row][col]
        if start_piece == 'L':
            if not valid_coord(row, col + l - 1):
                return -1
            if self.grid[row][col + l - 1] == 'R':    #maybe check the midle of the boat
                return 1
            else:
                return 0
        elif start_piece == 'T':
            if not valid_coord(row + l -1, col):
                return -1
            if self.grid[row + l - 1][col] == 'R':    #maybe check the midle of the boat
                return 1
            else:
                return 0
        elif start_piece == 'C':
            if l == 1:
                return 1
            else:
                return 0
        else:
            return 0
    


    # TODO: outros metodos da classe


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.board = board

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        
        if state.state_id == 1: #if is the first state return 1
            return 1
        
        actions = [] #(boatkind, row, col, start_piece)
        board = state.board
        available_boats = board.boats

        if available_boats['boat4'] != 0:
            for row in range(board_size):
                for col in range(board_size):
                    if board.row_restritions[row] >= 4:
                        pass


    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        board = state.board

                        


    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        board = state.board
        
        col_boat_parts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        count_boats = [0, 0, 0, 0] #[boat1, boat2, boat3, boat4]
        for row in range(board_size):
            count_row_boat_parts = 0
            for col in range(col_boat_parts):
                piece = board.grid[row][col]
                initial_piece = self.is_in_initial_grid(row, col)

                if piece not in board_pieces:    #1
                    return False
                
                if initial_piece in board_pieces:#2
                    if piece == initial_piece:
                        return False 
                
                if piece in board_pieces and piece != 'W':
                    count_row_boat_parts += 1
                    col_boat_parts[col] += 1

                if piece == 'C': 
                    if board.start_boat(row, col, 1) == 1: #5
                        count_boats[0] += 1
                    else:
                        return False
                
                if piece != 'C': #5
                    return board.start_boat(row, col, 1) == 0
                
                if piece == 'T' or piece == 'L': 
                    if board.start_boat(row, col, 2) == 1: #6
                        count_boats[1] += 1
                    if board.start_boat(row, col, 3) == 1: #6
                        count_boats[2] += 1
                    if board.start_boat(row, col, 4) == 1: #6
                        count_boats[3] += 1
                    else:
                        return False
                
            if count_row_boat_parts != board.row_restritions[row]: #3
                return False
            
        if tuple(col_boat_parts) != board.col_restritions: #4
            return False
        if count_boats != [4, 3, 2, 1]: #7
            return False

        

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe
    def initial_grid_piece(self, row, col):
        return self.board.get_value(row, col)


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance()
    board.print()
