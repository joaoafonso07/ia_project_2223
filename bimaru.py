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
        self.row_info = row_info # row_info = [[row_restrition, empty_in_row, pieces_in_row], ...]
        self.col_info = col_info # col_info = [[col_restrition, empty_in_col, pieces_in_col], ...]
        self.grid = grid
        self.boats = boats


    def get_value(self, row: int, col: int) -> str:
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
                    if self.row_info[row][0] == self.row_info[row][2] or self.col_info[col][0] == self.col_info[col][2]:
                        self.grid[row][col] = 'W'
                        self.row_info[row][1] -= 1
                        self.col_info[col][1] -= 1


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

        row_info = []
        col_info = []

        grid = []

        for e in range(board_size):
            grid.append(['.','.','.','.','.','.','.','.','.','.'])
            row_info.append([row_restritions[e], 10, 0])
            col_info.append([column_restritions[e], 10, 0])


        for e in range(numb_of_hints):
            hint = sys.stdin.readline().split()

            row = int(hint[1])
            col = int(hint[2])
            
            grid[row][col] = hint[3]

            row_info[row][1] -= 1
            col_info[col][1] -= 1

            if hint[3] != 'W':
                row_info[row][2] += 1
                col_info[col][2] += 1

            coord_to_water = around_coord(row, col, hint[3])

            for coord in coord_to_water:
                if valid_coord(coord[0], coord[1]):
                    if grid[coord[0]][coord[1]] == '.':
                        grid[coord[0]][coord[1]] = 'W'
                        row_info[coord[0]][1] -= 1
                        col_info[coord[1]][1] -= 1
                    
        boats = {"boat1": 4, "boat2": 3, "boat3": 2, "boat4": 1}

        for row in range(board_size):
            for col in range(board_size):
                if grid[row][col] == '.':
                    if row_info[row][0] == row_info[row][2] or col_info[col][0] == col_info[col][2]:
                        grid[row][col] = 'W'
                        row_info[row][1] -= 1
                        col_info[col][1] -= 1
                    

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
