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

    def __init__(self):
        self.board = np.full((10, 10), '0')
        self.row_values = [0]*Board.rows
        self.column_values = [0]*Board.columns

    @staticmethod
    def parse_instance(self):
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """

        water_row = ['▒','▒','▒','▒','▒','▒','▒','▒','▒','▒']

        row_inputs = input().split()
        for i in range(self.rows):
            if(row_inputs[i+1] == '0'):
                self.board[i] = water_row
            else:
                self.row_values[i] = int(row_inputs[i+1]) #1st element ROWS

        column_inputs = input().split()
        for i in range(self.columns):
            if(column_inputs[i+1] == '0'):
                for j in range(self.rows):
                    self.board[j][i] = '▒'
            else:
                self.column_values[i] = int(column_inputs[i+1]) #1st element COLUMNS

        hint_total = int(input())

        for i in range(hint_total):
            hint = input().split()
            #HINT row[1] column[2] value[3]
            if(hint[3] == 'W'):
                self.board[int(hint[1])][int(hint[2])] = '▒'
            elif(hint[3] == 'T'):
                self.board[int(hint[1])][int(hint[2])] = '▲'
                self.fill_water_around_top(int(hint[1]), int(hint[2]), 'T')
            elif(hint[3] == 'B'):
                self.board[int(hint[1])][int(hint[2])] = '▼'
                self.fill_water_around_bottom(int(hint[1]), int(hint[2]), 'B')
            elif(hint[3] == 'R'):
                self.board[int(hint[1])][int(hint[2])] = '▶'
                self.fill_water_around__right(int(hint[1]), int(hint[2]), 'R')
            elif(hint[3] == 'L'):
                self.board[int(hint[1])][int(hint[2])] = '◀'
                self.fill_water_around_left(int(hint[1]), int(hint[2]), 'L')
            elif(hint[3] == 'M'):
                self.board[int(hint[1])][int(hint[2])] = '■'
                self.fill_water_around_middle(int(hint[1]), int(hint[2]), 'M')
            elif(hint[3] == 'C'):
                self.board[int(hint[1])][int(hint[2])] = '●'
                self.fill_water_around_circle(int(hint[1]), int(hint[2]), 'C')
        
        print("board->\n")
        for i in range(10):
            for j in range(10):
                print(self.board[i][j], end=' ')
            print('  ', end='')
            print(self.row_values[i])
        print()
        for i in range(10):
            print(self.column_values[i], end=' ')
        pass

    def fill_water_around_circle(self, row: int, col: int, dir: str):
        if(row + 1 < 10):
            self.board[row+1][col] = '▒'
            if(col + 1 < 10):
                self.board[row+1][col+1] = '▒'
                self.board[row][col+1] = '▒'
            if(col - 1 >= 0):
                self.board[row+1][col-1] = '▒'
                self.board[row][col-1] = '▒'
        if(row - 1 >= 0):
            self.board[row-1][col] = '▒'
            if(col + 1 < 10):
                self.board[row-1][col+1] = '▒'
                self.board[row][col+1] = '▒'
            if(col - 1 >= 0):
                self.board[row-1][col-1] = '▒'
                self.board[row][col-1] = '▒'
    
    def fill_water_around_middle(self, row: int, col: int, dir: str):
        if(row + 1 < 10 and col + 1 < 10):
            self.board[row+1][col+1] = '▒'
        if(row + 1 < 10 and col - 1 >= 0):
            self.board[row+1][col-1] = '▒'
        if(row - 1 >= 0 and col + 1 < 10):
            self.board[row-1][col+1] = '▒'
        if(row - 1 >= 0 and col - 1 >= 0):
            self.board[row-1][col-1] = '▒'

    def fill_water_around_top(self, row: int, col: int, dir: str):
        if(row + 1 < 10 and col + 1 < 10):
                self.board[row+1][col+1] = '▒'
                self.board[row][col+1] = '▒'
                if(col - 1 >= 0):
                    self.board[row+1][col-1] = '▒'
                    self.board[row][col-1] = '▒'
        if(row - 1 >= 0):
            self.board[row-1][col] = '▒'
            if(col + 1 < 10):
                self.board[row-1][col+1] = '▒'
                self.board[row][col+1] = '▒'
            if(col - 1 >= 0):
                self.board[row-1][col-1] = '▒'
                self.board[row][col-1] = '▒'
        pass

    def fill_water_around_bottom(self, row: int, col: int, dir: str):
        if(row + 1 < 10):
            self.board[row+1][col] = '▒'
            if(col + 1 < 10):
                self.board[row+1][col+1] = '▒'
                self.board[row][col+1] = '▒'
            if(col - 1 >= 0):
                self.board[row+1][col-1] = '▒'
                self.board[row][col-1] = '▒'
        if(row - 1 >= 0 and col + 1 < 10):
            self.board[row-1][col+1] = '▒'
            self.board[row][col+1] = '▒'
        if(row - 1 >= 0 and col - 1 >= 0):
            self.board[row-1][col-1] = '▒'
            self.board[row][col-1] = '▒'
        pass
    
    def fill_water_around_right(self, row: int, col: int, dir: str):
        if(col + 1 < 10):
            self.board[row][col+1] = '▒'
            if(row + 1 < 10):
                self.board[row+1][col+1] = '▒'
                self.board[row+1][col] = '▒'
            if(row - 1 >= 0):
                self.board[row-1][col+1] = '▒'
                self.board[row-1][col] = '▒'
        if(col - 1 >= 0 and row + 1 < 10):
            self.board[row+1][col-1] = '▒'
            self.board[row+1][col] = '▒'
        if(col - 1 >= 0 and row - 1 >= 0):
            self.board[row-1][col-1] = '▒'
            self.board[row-1][col] = '▒'
        pass

    def fill_water_around_left(self, row: int, col: int, dir: str):
        if(col - 1 >= 0):
            self.board[row][col-1] = '▒'
            if(row + 1 < 10):
                self.board[row+1][col-1] = '▒'
                self.board[row+1][col] = '▒'
            if(row - 1 >= 0):
                self.board[row-1][col-1] = '▒'
                self.board[row-1][col] = '▒'
        if(col + 1 < 10 and row + 1 < 10):
            self.board[row+1][col+1] = '▒'
            self.board[row+1][col] = '▒'
        if(col + 1 < 10 and row - 1 >= 0):
            self.board[row-1][col+1] = '▒'
            self.board[row-1][col] = '▒'
        pass

    # TODO: outros metodos da classe

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

bimaru_read()