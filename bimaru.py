# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

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
boar_pieces = ('W', 'C', 'T', 'M', 'B', 'L', 'R')


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

    def __init__(self, row_restritions:tuple, column_restritions: tuple, grid: list[list[str]]):
        self.row_restritions = row_restritions
        self.column_restritions = column_restritions
        self.grid = grid

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if row > board_size or row < 0 or col > board_size or col < 0:
            return -1
        return self.grid[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if row > board_size or row < 0 or col > board_size or col < 0:
            return -1
        elif row == board_size:
            return (self.grid[row-1][col], None)
        elif row == 0:
            return (None, self.grid[row+1][col])
        else:
            return (self.grid[row-1][col], self.grid[row+1][col])

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if row > board_size or row < 0 or col > board_size or col < 0:
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
        # TODO
        str_row = sys.stdin.readline().split()
        row_restritions = tuple(str_row[1:])

        str_col = sys.stdin.readline().split()
        column_restritions = tuple(str_col[1:])

        numb_of_hints = int(sys.stdin.readline())

        grid = []

        for e in range(board_size):
            grid.append(['.','.','.','.','.','.','.','.','.','.'])

        for e in range(numb_of_hints):
            hint = sys.stdin.readline().split
            grid[hint[1]][hint[2]] = hint[3]
        
        return Board(row_restritions=row_restritions, column_restritions= column_restritions, grid=grid)

    # TODO: outros metodos da classe


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.board = board

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        board = state.board
        boat_pieces = [] #stores all the baot pices so we can then confirm if other gola restritions

        for row in range(board_size):
            for col in range(board_size):
                target = board.grid[row][col]

                if target == '.':
                    return False
                
                if  target in boar_pieces and target != 'W':
                    boat_pieces.append((target, row, col))                

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
