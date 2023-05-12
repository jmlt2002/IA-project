# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 99986 João Tiago
# 102663 Pedro Ribeiro

import sys
import numpy as np
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

ROWS = 10
COLUMNS = 10

#USEFULL DEFINITIONS
Hint = (str, bool)
Position = (int, int)
Action = (str, Position)

#BOATS
Four_boat = (Position, Position, Position, Position, str)
Three_boat = (Position, Position, Position, str)
Two_boat = (Position, Position, str) #last str indicates direction
One_boat = Position


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
    
    rows = 10
    columns = 10

    def __init__(self):
        self.board = np.full((10, 10), '0')
        self.rows= [0]*ROWS
        self.columns = [0]*COLUMNS
        self.initial_row_value = [0]*ROWS   #listas para guardar os valores iniciais das col e lin
        self.initial_column_value = [0]*COLUMNS  #para passar logo a frente na procura de barcos

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente. (acima, abaixo)"""
        if(row == 0):
            return ('OUT', self.board[row+1][col])
        elif(row == 9):
            return (self.board[row-1][col], 'OUT')
        return (self.board[row-1][col], self.board[row+1][col])

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente. (esquerda, direita)"""
        if(col == 0):
            return ('OUT', self.board[row][col+1])
        elif(col == 9):
            return (self.board[row][col-1], 'OUT')
        else:
            return (self.board[row][col-1], self.board[row][col+1])

    @staticmethod
    def parse_instance(self):
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """

        # to use in rows and columns with no boat
        water_row = ['W','W','W','W','W','W','W','W','W','W']

        #read rows values
        rows = input().split()
        for i in range(len(self.rows)):
            if(rows[i+1] == '0'):
                self.board[i] = water_row
            else:
                self.rows[i] = int(rows[i+1]) #1st element ROWS

        #read columns values
        columns = input().split()
        for i in range(len(self.columns)):
            if(columns[i+1] == '0'):
                for j in range(len(self.rows)):
                    self.board[j][i] = 'W'
            else:
                self.columns[i] = int(columns[i+1]) #1st element COLUMNS

        #read hints
        hint_total = int(input())

        for i in range(hint_total):
            hint = input().split()
            self.board[int(hint[1])][int(hint[2])] = hint[3]
            
            # TODO: decrease row and column values by 1

            if(hint[3] == 'M'):
                self.fill_water_around_middle(int(hint[1]), int(hint[2]), hint[3])
            elif(hint[3] == 'C'):
                self.fill_water_around_circle(int(hint[1]), int(hint[2]), hint[3])
            elif(hint[3] == 'B'):
                self.fill_water_around_bottom(int(hint[1]), int(hint[2]), hint[3])
            elif(hint[3] == 'T'):
                self.fill_water_around_top(int(hint[1]), int(hint[2]), hint[3])
            elif(hint[3] == 'L'):
                self.fill_water_around_left(int(hint[1]), int(hint[2]), hint[3])
            elif(hint[3] == 'R'):
                self.fill_water_around_right(int(hint[1]), int(hint[2]), hint[3])

        pass

    def print_board(self):
        """"Imprime o tabuleiro de jogo."""
        print("board->\n")
        for i in range(10):
            for j in range(10):
                if(self.board[i][j] == 'W'):
                    print('▒', end=' ')
                elif(self.board[i][j] == 'M'):
                    print('■', end=' ')
                elif(self.board[i][j] == 'C'):
                    print('●', end=' ')
                elif(self.board[i][j] == 'B'):
                    print('▼', end=' ')
                elif(self.board[i][j] == 'T'):
                    print('▲', end=' ')
                elif(self.board[i][j] == 'L'):
                    print('◀', end=' ')
                elif(self.board[i][j] == 'R'):
                    print('▶', end=' ')
                else:
                    print('0', end=' ')
            print('  ', end='')
            print(self.rows[i])
        print()
        for i in range(10):
            print(self.columns[i], end=' ')
        pass

    # FILLS WATER TILES ADJACENT TO SHIPS------------------------------
    def fill_water_around_circle(self, row: int, col: int, dir: str):
        if(row + 1 < 10):
            self.board[row+1][col] = 'W'
            if(col + 1 < 10):
                self.board[row+1][col+1] = 'W'
                self.board[row][col+1] = 'W'
            if(col - 1 >= 0):
                self.board[row+1][col-1] = 'W'
                self.board[row][col-1] = 'W'
        if(row - 1 >= 0):
            self.board[row-1][col] = 'W'
            if(col + 1 < 10):
                self.board[row-1][col+1] = 'W'
                self.board[row][col+1] = 'W'
            if(col - 1 >= 0):
                self.board[row-1][col-1] = 'W'
                self.board[row][col-1] = 'W'
    
    def fill_water_around_middle(self, row: int, col: int, dir: str):
        if(row + 1 < 10 and col + 1 < 10):
            self.board[row+1][col+1] = 'W'
        if(row + 1 < 10 and col - 1 >= 0):
            self.board[row+1][col-1] = 'W'
        if(row - 1 >= 0 and col + 1 < 10):
            self.board[row-1][col+1] = 'W'
        if(row - 1 >= 0 and col - 1 >= 0):
            self.board[row-1][col-1] = 'W'

    def fill_water_around_top(self, row: int, col: int, dir: str):
        if(row + 1 < 10 and col + 1 < 10):
                self.board[row+1][col+1] = 'W'
                self.board[row][col+1] = 'W'
                if(col - 1 >= 0):
                    self.board[row+1][col-1] = 'W'
                    self.board[row][col-1] = 'W'
        if(row - 1 >= 0):
            self.board[row-1][col] = 'W'
            if(col + 1 < 10):
                self.board[row-1][col+1] = 'W'
                self.board[row][col+1] = 'W'
            if(col - 1 >= 0):
                self.board[row-1][col-1] = 'W'
                self.board[row][col-1] = 'W'
        pass

    def fill_water_around_bottom(self, row: int, col: int, dir: str):
        if(row + 1 < 10):
            self.board[row+1][col] = 'W'
            if(col + 1 < 10):
                self.board[row+1][col+1] = 'W'
                self.board[row][col+1] = 'W'
            if(col - 1 >= 0):
                self.board[row+1][col-1] = 'W'
                self.board[row][col-1] = 'W'
        if(row - 1 >= 0 and col + 1 < 10):
            self.board[row-1][col+1] = 'W'
            self.board[row][col+1] = 'W'
        if(row - 1 >= 0 and col - 1 >= 0):
            self.board[row-1][col-1] = 'W'
            self.board[row][col-1] = 'W'
        pass
    
    def fill_water_around_right(self, row: int, col: int, dir: str):
        if(col + 1 < 10):
            self.board[row][col+1] = 'W'
            if(row + 1 < 10):
                self.board[row+1][col+1] = 'W'
                self.board[row+1][col] = 'W'
            if(row - 1 >= 0):
                self.board[row-1][col+1] = 'W'
                self.board[row-1][col] = 'W'
        if(col - 1 >= 0 and row + 1 < 10):
            self.board[row+1][col-1] = 'W'
            self.board[row+1][col] = 'W'
        if(col - 1 >= 0 and row - 1 >= 0):
            self.board[row-1][col-1] = 'W'
            self.board[row-1][col] = 'W'
        pass

    def fill_water_around_left(self, row: int, col: int, dir: str):
        if(col - 1 >= 0):
            self.board[row][col-1] = 'W'
            if(row + 1 < 10):
                self.board[row+1][col-1] = 'W'
                self.board[row+1][col] = 'W'
            if(row - 1 >= 0):
                self.board[row-1][col-1] = 'W'
                self.board[row-1][col] = 'W'
        if(col + 1 < 10 and row + 1 < 10):
            self.board[row+1][col+1] = 'W'
            self.board[row+1][col] = 'W'
        if(col + 1 < 10 and row - 1 >= 0):
            self.board[row-1][col+1] = 'W'
            self.board[row-1][col] = 'W'
        pass
    #---------------------------------------------------------------------

    def look_for_four_boat(self) -> tuple(Four_boat):
        "procura no tabuleiro espacos onde colocar barcos de 4"
        pass

    def look_for_three_boat(self) -> tuple(Three_boat):
        "procura no tabuleiro espacos onde colocar barcos de 3"
        pass

    def look_for_two_boat(self) -> tuple(Two_boat):
        "procura no tabuleiro espacos onde colocar barcos de 2"
        pass

    def look_for_one_boat(self) -> tuple(One_boat):
        "procura no tabuleiro espacos onde colocar barcos de 1"
        pass

class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO:
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO:
        pass

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO:
        pass

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO:
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO:
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass

def bimaru_read():
    board = Board()
    board.parse_instance(board)
    board.print_board()

bimaru_read()