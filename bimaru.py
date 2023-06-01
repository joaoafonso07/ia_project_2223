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
import copy
import time

board_size = 10
board_pieces = ('W', 'C', 'T', 'M', 'B', 'L', 'R')


def valid_coord(row, col):
    return row < board_size and row >= 0 and col < board_size and col >= 0

def around_coord(row, col, P):
    if P == 'C':
        return [(row-1, col-1), (row-1, col), (row-1, col+1),
                (row, col-1)                ,   (row, col+1),
                (row+1, col-1), (row+1, col), (row+1, col+1)]
    
    elif P == 'T':
        return [(row-1, col-1), (row-1, col), (row-1, col+1),
                (row, col-1)                ,   (row, col+1),
                (row+1, col-1)              , (row+1, col+1),
                (row+2, col-1)              , (row+2, col+1)]
    
    elif P == 'B':
        return [(row-2, col-1)              , (row-2, col+1),
                (row-1, col-1)              , (row-1, col+1),
                (row, col-1)                ,   (row, col+1),
                (row+1, col-1), (row+1, col), (row+1, col+1)]
    
    elif P == 'L':
        return [(row-1, col-1), (row-1, col), (row-1, col+1), (row-1, col+2),
                (row, col-1)                ,   
                (row+1, col-1), (row+1, col), (row+1, col+1), (row+1, col+2)]
    
    elif P == 'R':
        return [(row-1, col-2), (row-1, col-1), (row-1, col), (row-1, col+1),
                                                                (row, col+1),   
                (row+1, col-2), (row+1, col-1), (row+1, col), (row+1, col+1)]
    
    elif P == 'M':
        return [(row-1, col-1)             , (row-1, col+1),
                
                (row+1, col-1)             , (row+1, col+1)]
    elif P == 'W':
        return []
    else:
        return -1
    

         

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
    
    def __init__(self, row_info: list, col_info: list, grid, boats):
        self.row_info = row_info # row_info = [[row_restriction, empty_in_row, pieces_not_boat_in_row, boat_pieces_in_row], ...]
        self.col_info = col_info # col_info = [[col_restriction, empty_in_col, pieces_not_boat_in_col, boat_pieces_in_col], ...]
        self.grid = grid
        self.boats = boats


    def get_value(self, row: int, col: int):
        """Devolve o valor na respetiva posição do tabuleiro."""
        if not valid_coord(row, col):
            return -1
        return self.grid[row][col]
    

    def adjacent_values(self, row: int, col: int):
        """Devolve um tuplo com os valores que rodeiam a celula."""
        if not valid_coord(row, col):
            return -1
        P = self.grid[row, col]
        adjacent_values = around_coord(row, col, P)
        for coord in adjacent_values:
            coord_row = coord[0]
            coord_col = coord[1]
            if not valid_coord[coord_row, coord_col]:
                adjacent_values.remove[(coord_row, coord_col)]
        return adjacent_values
    
    def water_lines(self):
        """Preenche com 'W' (água) todas as linhas em que o 
        número de peças for igual à restrição dessa linha aka
        não caberem mais peças"""
        for row in range(board_size):
            for col in range(board_size):
                if self.grid[row][col] == '.':
                    if self.row_info[row][0] == self.row_info[row][2] + self.row_info[row][3] or self.col_info[col][0] == self.col_info[col][2] + self.col_info[col][3]:
                        self.grid[row][col] = 'W'
                        self.row_info[row][1] -= 1 #row empty -= 1
                        self.col_info[col][1] -= 1 #col empty -= 1
    

    def boat4_row(self, row):
        """Para uma determinada linha retorna os indices 
        de onde um barco 4 pode começar"""
        if row <= 9 and row >= 0:
            starting_points = []
            if self.row_info[row][0] >= 4: #row restriction >= 4
                if self.row_info[row][0] - self.row_info[row][3] >=4 :
                    if self.row_info[row][1] + self.row_info[row][2] >= 4:                    
                        possible_sublists =(['.', '.', '.', '.'], ['L', '.', '.', '.'],
                                            ['.', 'M', '.', '.'], ['L', 'M', '.', '.'],  
                                            ['.', 'M', 'M', '.'], ['L', 'M', 'M', '.'], 
                                            ['.', 'M', 'M', 'R'], ['L', '.', '.', 'R'],  
                                            ['.', 'M', '.', 'R'], ['L', 'M', '.', 'R'], 
                                            ['.', '.', 'M', 'R'], ['L', '.', 'M', 'R'],  
                                            ['.', '.', '.', 'R'], ['L', '.', 'M', '.'], 
                                            ['.', '.', 'M', '.'])
                        target = self.get_row(row)
                        for n in range(7):
                            if target[n: n+4] in possible_sublists:
                                starting_points.append(n)
            return starting_points

    def boat4_col(self, col):
        """Para uma determinada coluna retorna os indices 
        de onde um barco 4 pode começar"""
        if col <= 9 and col >= 0:
            starting_points = []
            if self.col_info[col][0] >= 4:
                if self.col_info[col][0] - self.col_info[col][3] >= 4:
                    if self.col_info[col][1] + self.col_info[col][2] >= 4:                    
                        possible_sublists =(['.', '.', '.', '.'], ['T', '.', '.', '.'], 
                                            ['.', 'M', '.', '.'], ['T', 'M', '.', '.'],
                                            ['.', 'M', 'M', '.'], ['T', 'M', 'M', '.'],   
                                            ['.', '.', 'M', '.'], ['T', '.', 'M', '.'], 
                                            ['.', 'M', '.', 'B'], ['T', 'M', '.', 'B'],
                                            ['.', '.', 'M', 'B'], ['T', '.', 'M', 'B'],
                                            ['.', 'M', 'M', 'B'])
                        target = self.get_col(col)
                        for n in range(7):
                            if target[n: n+4] in possible_sublists:
                                starting_points.append(n)
            return starting_points             


    def boat3_row(self, row):
        """Para uma determinada linha retorna os indices 
        de onde um barco 3 pode começar"""
        if row <= 9 and row >= 0:
            starting_points = []
            if self.row_info[row][0] >= 3:
                if self.row_info[row][0] - self.row_info[row][3] >= 3:
                    if self.row_info[row][1] + self.row_info[row][2] >= 3:
                        possible_sublists =(['.', 'M', '.'], ['L', 'M', '.'],   
                                            ['.', '.', '.'], ['L', '.', '.'],  
                                            ['.', '.', 'R'], ['L', '.', 'R'],
                                            ['.', 'M', 'R'])                       
                        target = self.get_row(row)
                        for n in range(8):
                            if target[n: n+3] in possible_sublists:
                                starting_points.append(n)
            return starting_points

    def boat3_col(self, col):
        """Para uma determinada coluna retorna os indices 
        de onde um barco 3 pode começar"""
        if col <= 9 and col >= 0:
            starting_points = []
            if self.col_info[col][0] >= 3:
                if self.col_info[col][0] - self.col_info[col][3] >= 3:
                    if self.col_info[col][1] + self.col_info[col][2] >= 3:                    
                        possible_sublists =(['.', 'M', '.'], ['T', 'M', '.'],   
                                            ['.', '.', '.'], ['T', '.', '.'],  
                                            ['.', '.', 'B'], ['T', '.', 'B'],
                                            ['.', 'M', 'B'])                       
                        target = self.get_col(col)
                        for n in range(8):
                            if target[n: n+3] in possible_sublists:
                                starting_points.append(n)
            return starting_points


    def boat2_row(self, row):
        """Para uma determinada linha retorna os indices 
        de onde um barco 2 pode começar"""
        if row <= 9 and row >= 0:
            starting_points = []
            if self.row_info[row][0] >= 2:
                if self.row_info[row][0] - self.row_info[row][3] >= 2:
                    if self.row_info[row][1] + self.row_info[row][2] >= 2:
                        possible_sublists =(['.', '.'], ['L', '.'],   
                                            ['.', 'R'])                       
                        target = self.get_row(row)
                        for n in range(9):
                            if target[n: n+2] in possible_sublists:
                                starting_points.append(n)
            return starting_points

    def boat2_col(self, col):
        """Para uma determinada linha retorna os indices 
        de onde um barco 2 pode começar"""
        if col <= 9 and col >= 0:
            starting_points = []
            if self.col_info[col][0] >= 2:
                if self.col_info[col][0] - self.col_info[col][3] >= 2:
                    if self.col_info[col][1] + self.col_info[col][2] >= 2:
                        possible_sublists =(['.', '.'], ['T', '.'],   
                                            ['.', 'B'])                       
                        target = self.get_col(col)
                        for n in range(9):
                            if target[n: n+2] in possible_sublists:
                                starting_points.append(n)
            return starting_points
    

    def boat1_row(self, row):
        """Para uma determinada linha retorna os indices 
        de onde um barco 2 pode começar"""
        if row <= 9 and row >= 0:
            starting_points = []
            if self.row_info[row][0] >= 1:
                if self.row_info[row][1] + self.row_info[row][2] >= 1:
                    possible_sublists =(['.'])                       
                    target = self.get_row(row)
                    for n in range(10):
                        if target[n] in possible_sublists:
                            starting_points.append(n)
            return starting_points

    def boat1_col(self, col):
        """Para uma determinada linha retorna os indices 
        de onde um barco 2 pode começar"""
        if col <= 9 and col >= 0:
            starting_points = []
            if self.col_info[col][0] >= 1:
                if self.col_info[col][1] + self.col_info[col][2] >= 1:
                    possible_sublists =(['.'], ['C'])                       
                    target = self.get_col(col)
                    for n in range(10):
                        if target[n] in possible_sublists:
                            starting_points.append(n)
            return starting_points
    

    def get_row(self, row):
        if row <= 9 and row >= 0:
            return self.grid[row]

    
    def get_col(self, col):
        if col <= 9 and col >= 0:
            column = []
            for n in range(board_size):
                column.append(self.grid[n][col])
            return column


    def row_retrictions(self, row):
        if row <= 9 and row >= 0:
            return self.row_info[0]
    
    def col_restrictions(self, col):
        if col <= 9 and col >= 0:
            return self.col_info[0]
        
    def row_numb_pieces(self, row):
        if row <= 9 and row >= 0:
            return self.row_info[2]
    
    def col_numb_pieces(self, col):
        if col <= 9 and col >= 0:
            return self.col_info[2]
        
    def row_numb_empty(self, row):
        if row <= 9 and row >= 0:
            return self.row_info[1]
    
    def col_numb_empty(self, col):
        if col <= 9 and col >= 0:
            return self.col_info[1]


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

        boats = {"boat1": 4, "boat2": 3, "boat3": 2, "boat4": 1}

        row_info = []
        col_info = []

        grid = []

        for e in range(board_size):
            grid.append(['.','.','.','.','.','.','.','.','.','.'])
            row_info.append([row_restritions[e], 10, 0, 0])
            col_info.append([column_restritions[e], 10, 0, 0])


        for e in range(numb_of_hints):
            hint = sys.stdin.readline().split()

            row = int(hint[1])
            col = int(hint[2])
            
            grid[row][col] = hint[3]

            if hint[3] != 'W':
                row_info[row][2] += 1 # row pieces not boat += 1
                col_info[col][2] += 1 # col pieces not boat += 1

            if hint[3] == 'C':
                boats['boat1'] -= 1
                row_info[row][2] -= 1 #row pieces not boat -= 1
                row_info[row][3] += 1 #row boat pieces += 1
                col_info[col][2] -= 1 #col pieces not boat -= 1
                col_info[col][3] += 1 #col boat pieces += 1

            row_info[row][1] -= 1 #row empty -= 1
            col_info[col][1] -= 1 #col empty -= 1

            

            coord_to_water = around_coord(row, col, hint[3])

            for coord in coord_to_water:
                if valid_coord(coord[0], coord[1]):
                    if grid[coord[0]][coord[1]] == '.':
                        grid[coord[0]][coord[1]] = 'W'
                        row_info[coord[0]][1] -= 1 #row empty -= 1
                        col_info[coord[1]][1] -= 1 #col empty -= 1
                    
        

        for row in range(board_size):
            for col in range(board_size):
                if grid[row][col] == 'T':
                    if row+1 and grid[row+1][col] == 'B':
                        boats['boat2'] -= 1
                        col_info[col][2] -= 2 #col pieces not boat -= 2
                        col_info[col][3] += 2 #col boat pieces += 2
                    elif grid[row+1][col] == 'M':
                        if row+2 <= 9:
                            if grid[row+2][col] == 'B':
                                boats['boat3'] -= 1
                                col_info[2] -= 3 #col pieces not boat -= 3
                                col_info[3] += 3 #col boat pieces += 3
                            elif grid[row+2][col] == 'M':
                                if row+3 <= 9 and grid[row+3][col] == 'B':
                                    boats['boat4'] -= 1  
                                    col_info[2] -= 4 #col pieces not boat -= 4
                                    col_info[3] += 4 #col boat pieces += 4
                elif grid[row][col] == 'L':
                    if grid[row][col+1] == 'R':
                        boats['boat2'] -= 1
                        row_info[2] -= 2 #row pieces not boat -= 2
                        row_info[3] += 2 #row boat pieces += 2
                    elif grid[row][col+1] == 'M':
                        if col+2 <= 9:
                            if grid[row][col+2] == 'R':
                                boats['boat3'] -= 1
                                row_info[2] -= 3 #row pieces not boat -= 3
                                row_info[3] += 3 #row boat pieces += 3
                            elif grid[row][col+2] == 'M':
                                if col+3 <= 9 and grid[row][col]+3 == 'R':
                                    boats['boat4'] -= 1
                                    row_info[2] -= 4 #row pieces not boat -= 4
                                    row_info[3] += 4 #row boat pieces += 4
                elif grid[row][col] == '.':
                    if row_info[row][0] == row_info[row][2] + row_info[row][3] or col_info[col][0] == col_info[col][2] + col_info[col][3]:
                        grid[row][col] = 'W'
                        row_info[row][1] -= 1 #row empty -= 1
                        col_info[col][1] -= 1 #col empty -= 1
                    

        return Board(row_info = row_info, col_info = col_info, grid = grid, boats = boats)
    
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
        self.initial = BimaruState(board)

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        
        actions = [] #(boat_lenght, row, col, 0 or 1 ->(vertical or horizontal))
        if state == None:
            return actions
        board = state.board
        available_boats = board.boats

        if available_boats['boat4'] != 0:
            for n in range(board_size):
                row_starting_coord = board.boat4_row(n)
                col_starting_coord = board.boat4_col(n)
                for col in row_starting_coord:
                    actions.append((4, n, col, 1))
                for row in col_starting_coord:
                    actions.append((4, row, n, 0))
        elif available_boats['boat3'] != 0:
            for n in range(board_size):
                row_starting_coord = board.boat3_row(n)
                col_starting_coord = board.boat3_col(n)
                for col in row_starting_coord:
                    actions.append((3, n, col, 1))
                for row in col_starting_coord:
                    actions.append((3, row, n, 0))
        elif available_boats['boat2'] != 0:
            for n in range(board_size):
                row_starting_coord = board.boat2_row(n)
                col_starting_coord = board.boat2_col(n)
                for col in row_starting_coord:
                    actions.append((2, n, col, 1))
                for row in col_starting_coord:
                    actions.append((2, row, n, 0))
        elif available_boats['boat1'] != 0:
            for n in range(board_size):
                row_starting_coord = board.boat1_row(n)
                col_starting_coord = board.boat1_col(n)
                for col in row_starting_coord:
                    actions.append((1, n, col, 1))
                for row in col_starting_coord:
                    actions.append((1, row, n, 0))

        print('returned actions =', actions)
        return actions
                

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        print("started result")
        board = copy.deepcopy(state.board)
        boat_lenght = action[0]
        row = action[1]
        col = action[2]
        direction = action[3]

        
        if boat_lenght == 4:
            board.boats['boat4'] -= 1
            if direction:
                board.row_info[row][3] += 4
            else:
                board.col_info[col][3] += 4
        elif boat_lenght == 3:
            board.boats['boat3'] -= 1
            if direction:
                board.row_info[row][3] += 3
            else:
                board.col_info[col][3] += 3
        elif boat_lenght == 2:
            board.boats['boat2'] -= 1
            if direction:
                board.row_info[row][3] += 2
            else:
                board.col_info[col][3] += 2
        elif boat_lenght == 1:
            board.boats['boat1'] -= 1
            board.row_info[row][3] += 1
            board.col_info[col][3] += 1

        print("boat 4", board.boats['boat4'] )
        print("boat 3", board.boats['boat3'] )
        print("boat 2", board.boats['boat2'] )
        print("boat 1", board.boats['boat1'] )


        print("boat_lenght=", boat_lenght)
        print("direction=", direction)
        print("row, col = ", row, col)

        if boat_lenght == 1:
            if board.grid[row][col] == '.':
                board.grid[row][col] = 'C'

                board.row_info[row][1] -= 1 #row empty -= 1
                board.col_info[col][1] -= 1 #col empty -= 1

                if board.row_info[row][0] > board.row_info[row][2] + board.row_info[row][3] or board.col_info[col][0] > board.col_info[col][2] + board.col_info[col][3]:
                    return None
                
                coord_to_water = around_coord(row, col, 'C')

                for coord in coord_to_water:
                    if valid_coord(coord[0], coord[1]):
                        if board.grid[coord[0]][coord[1]] == '.':
                            board.grid[coord[0]][coord[1]] = 'W'
                            board.row_info[coord[0]][1] -= 1
                            board.col_info[coord[1]][1] -= 1
                        elif board.grid[coord[0]][coord[1]] != 'W':
                            print("result returned null")
                            return None
        else:
            if direction: #if horizontal
                for n in range(boat_lenght):
                    if n == 0:
                        if board.grid[row][col+n] == '.':
                            board.grid[row][col+n] = 'L'
                            print("printed L")
                            
                            board.row_info[row][1] -= 1 #row empty -= 1
                            board.col_info[col+n][1] -= 1 #col empty -= 1
                            
                            board.col_info[col+n][2] += 1 #col pieces not boat += 1

                            if board.col_info[col+n][0] < board.col_info[col+n][2] + board.col_info[col+n][3]:
                                return None

                            coord_to_water = around_coord(row, col + n, 'L')

                            for coord in coord_to_water:
                                if valid_coord(coord[0], coord[1]):
                                    if board.grid[coord[0]][coord[1]] == '.':
                                        board.grid[coord[0]][coord[1]] = 'W'
                                        board.row_info[coord[0]][1] -= 1
                                        board.col_info[coord[1]][1] -= 1
                                    elif board.grid[coord[0]][coord[1]] != 'W':
                                        print("result returned null")
                                        return None
                        else:
                            board.row_info[row][2] -= 1 #col pieces not boat -= 1
                            
                    elif n == boat_lenght - 1:
                        if board.grid[row][col+n] == '.':
                            board.grid[row][col+n] = 'R' 
                            print("printed R")

                            board.row_info[row][1] -= 1 #row empty -= 1
                            board.col_info[col+n][1] -= 1 #col empty -= 1
                            
                            board.col_info[col+n][2] += 1 #col pieces not boat += 1

                            if board.col_info[col+n][0] < board.col_info[col+n][2] + board.col_info[col+n][3]:
                                return None

                            coord_to_water = around_coord(row, col + n, 'R')

                            for coord in coord_to_water:
                                if valid_coord(coord[0], coord[1]):
                                    if board.grid[coord[0]][coord[1]] == '.':
                                        board.grid[coord[0]][coord[1]] = 'W'
                                        board.row_info[coord[0]][1] -= 1 #row empty -= 1
                                        board.col_info[coord[1]][1] -= 1 #col empty -= 1
                                    elif board.grid[coord[0]][coord[1]] != 'W':
                                        print("result returned null")
                                        return None
                        else:
                            board.row_info[row][2] -= 1 #col pieces not boat -= 1
                    else:
                        if board.grid[row][col+n] == '.':
                            board.grid[row][col+n] = 'M'
                            print("printed M")
                            board.row_info[row][1] -= 1 #row empty -= 1
                            board.col_info[col+n][1] -= 1 #col empty -= 1
                            
                            board.col_info[col+n][2] += 1 #col pieces not boat += 1

                            if board.col_info[col+n][0] < board.col_info[col+n][2] + board.col_info[col+n][3]:
                                return None

                            coord_to_water = around_coord(row, col + n, 'M')

                            for coord in coord_to_water:
                                if valid_coord(coord[0], coord[1]):
                                    if board.grid[coord[0]][coord[1]] == '.':
                                        board.grid[coord[0]][coord[1]] = 'W'
                                        board.row_info[coord[0]][1] -= 1
                                        board.col_info[coord[1]][1] -= 1
                                    elif board.grid[coord[0]][coord[1]] != 'W':
                                        print("result returned null")
                                        return None
                        else:
                            board.row_info[row][2] -= 1 #col pieces not boat -= 1
            else: #vertical
                for n in range(boat_lenght):
                    if n == 0:
                        print("n =", n)
                        if board.grid[row+n][col] == '.':
                            board.grid[row+n][col] = 'T'
                            print("printed T")

                            board.row_info[row+n][1] -= 1 #row empty -= 1
                            board.col_info[col][1] -= 1 #col empty -= 1
                            
                            board.row_info[row+n][2] += 1 #row pieces not boat += 1

                            if board.row_info[row+n][0] < board.row_info[row+n][2] + board.row_info[row+n][3]:
                                return None

                            coord_to_water = around_coord(row+n, col, 'T')

                            for coord in coord_to_water:
                                if valid_coord(coord[0], coord[1]):
                                    if board.grid[coord[0]][coord[1]] == '.':
                                        board.grid[coord[0]][coord[1]] = 'W'
                                        board.row_info[coord[0]][1] -= 1 #row empty -= 1
                                        board.col_info[coord[1]][1] -= 1 #col empty -= 1
                                    elif board.grid[coord[0]][coord[1]] != 'W':
                                        print("result returned null T")
                                        return None
                        else:
                            board.col_info[col][2] -= 1 #col pieces not boat -= 1

                    elif n == boat_lenght - 1:
                        print("n =", n)
                        if board.grid[row+n][col] == '.':
                            board.grid[row+n][col] = 'B' 
                            print("printed B")
                            board.row_info[row+n][1] -= 1 #row empty -= 1
                            board.col_info[col][1] -= 1 #col empty -= 1
                            
                            board.row_info[row+n][2] += 1 #row pieces not boat += 1

                            if board.row_info[row+n][0] < board.row_info[row+n][2] + board.row_info[row+n][3]:
                                return None

                            coord_to_water = around_coord(row+n, col, 'B')

                            for coord in coord_to_water:
                                if valid_coord(coord[0], coord[1]):
                                    print(board.grid[coord[0]][coord[1]])
                                    if board.grid[coord[0]][coord[1]] == '.':
                                        board.grid[coord[0]][coord[1]] = 'W'
                                        board.row_info[coord[0]][1] -= 1 #row empty -= 1
                                        board.col_info[coord[1]][1] -= 1 #col empty -= 1
                                    elif board.grid[coord[0]][coord[1]] != 'W':
                                        print("result returned null B")
                                        return None
                        else:
                            board.col_info[col][2] -= 1 #col pieces not boat -= 1
                    else:
                        print("n =", n)
                        if board.grid[row+n][col] == '.':
                            print("got here")
                            board.grid[row+n][col] = 'M'
                            print("printed M")
                            board.row_info[row+n][1] -= 1 #row empty -= 1
                            board.col_info[col][1] -= 1 #col empty -= 1
                            
                            board.row_info[row+n][2] += 1 #row pieces not boat += 1

                            if board.row_info[row+n][0] < board.row_info[row+n][2] + board.row_info[row+n][3]:
                                return None

                            coord_to_water = around_coord(row+n, col, 'M')

                            for coord in coord_to_water:
                                if valid_coord(coord[0], coord[1]):
                                    print(board.grid[coord[0]][coord[1]])
                                    if board.grid[coord[0]][coord[1]] == '.':
                                        board.grid[coord[0]][coord[1]] = 'W'
                                        board.row_info[coord[0]][1] -= 1 #row empty -= 1
                                        board.col_info[coord[1]][1] -= 1 #col empty -= 1
                                    elif board.grid[coord[0]][coord[1]] != 'W':
                                        print("result returned null M")
                                        return None
                        else:
                            board.col_info[col][2] -= 1 #col pieces not boat -= 1
        

        print("Board before water_lines")
        board.print()
        print("row_info", board.row_info)
        print("col_info", board.col_info)
        board.water_lines()
        print("Board after water_lines")
        board.print()
        print("row_info", board.row_info)
        print("col_info", board.col_info)
        print("result finished")
        return BimaruState(board)    


                        


    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        if state == None:
            return False
        
        board = state.board
        
        for row in range(board_size):
            for col in range(board_size):
                if board.grid[row][col] == '.':
                    return False
                if board.row_info[row][0] !=  board.row_info[row][2] + board.row_info[row][3]:
                    return False
                if board.col_info[col][0] !=  board.col_info[col][2] + board.col_info[col][3]:
                    return False
        return True
    
        """
        col_boat_parts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        count_boats = [0, 0, 0, 0] #[boat1, boat2, boat3, boat4]
        for row in range(board_size):
            count_row_boat_parts = 0
            for col in range(board_size):
                piece = board.grid[row][col]
                initial_piece = self.initial_grid_piece(row, col)

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
        """        

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe
    def initial_grid_piece(self, row, col):
        return self.initial.board.get_value(row, col)


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    start = time.perf_counter()
    board = Board.parse_instance()
    board.print()
    problem = Bimaru(board)
    goal_node = depth_first_tree_search(problem)
    goal_node.state.board.print()
