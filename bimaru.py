# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 61:
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
HORIZONTAL = True
VERTICAL = False

#USEFUL DEFINITIONS
Hint = (str, bool)
Position = (int, int)
Placement = (str, Position)
Action = tuple(Placement)

#acoes = [four_boat1, four_boat2]
#acoes = [(4_cenas), (4cenas)]
#acoes = [(('L',pos),('M', pos),('M', pos),('R', pos)) , (('L',pos),('M', pos),('M', pos),('R', pos))]
         #---primeiro barco----------------------------  segundo_barco-------------------------------


#BOATS
Four_boat = (Position, Position, Position, Position, bool)
Three_boat = (Position, Position, Position, bool)
Two_boat = (Position, Position, bool) #last str indicates direction
One_boat = Position




class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self):
        self.board = np.full((10, 10), '0')
        self.rows= [0]*ROWS
        self.columns = [0]*COLUMNS
        self.initial_row_value = [0]*ROWS   #listas para guardar os valores iniciais das col e lin
        self.initial_column_value = [0]*COLUMNS  #para passar logo a frente na procura de barcos
        self.remaining_boats = 10
        self.remaining_four_boats = 1
        self.remaining_three_boats = 2
        self.remaining_two_boats = 3
        self.remaining_one_boats = 4

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
        rows_raw = input().split()
        self.rows = rows_raw[1:]
        self.initial_row_value = np.array(self.rows, dtype=int)
        self.rows = np.array(self.rows, dtype=int)
        for i in range(len(self.rows)):
            self.rows[i] = int(self.rows[i])

        #read columns values
        columns_raw = input().split()
        self.columns = columns_raw[1:]
        self.initial_column_value = np.array(self.columns, dtype=int)
        self.columns = np.array(self.columns, dtype=int)
        for i in range(len(self.columns)):
            if(self.columns[i] == 0):
                for j in range(len(self.rows)):
                    self.board[j][i] = 'W'
            else:
                self.columns[i] = int(self.columns[i])

        #read hints
        hint_total = int(input())

        for i in range(hint_total):
            hint = input().split()
            self.board[int(hint[1])][int(hint[2])] = hint[3]
            if(hint[3] != 'W'):
                self.rows[int(hint[1])] -= 1
                self.columns[int(hint[2])] -= 1

            if(hint[3] == 'M'):
                self.fill_water_around_middle(int(hint[1]), int(hint[2]), hint[3])
            elif(hint[3] == 'C'):
                self.remaining_boats -= 1
                self.remaining_one_boats -=1
                self.fill_water_around_circle(int(hint[1]), int(hint[2]), hint[3])
            elif(hint[3] == 'B'):
                self.fill_water_around_bottom(int(hint[1]), int(hint[2]), hint[3])
            elif(hint[3] == 'T'):
                self.fill_water_around_top(int(hint[1]), int(hint[2]), hint[3])
            elif(hint[3] == 'L'):
                self.fill_water_around_left(int(hint[1]), int(hint[2]), hint[3])
            elif(hint[3] == 'R'):
                self.fill_water_around_right(int(hint[1]), int(hint[2]), hint[3])

        for i in range(10):
            if(self.rows[i] == 0):
                for j in range(len(self.rows)):
                    if(not self.board[i][j].isalpha()):
                        self.board[i][j] = 'W'
            if(self.columns[i] == 0):
                for j in range(len(self.rows)):
                    if(not self.board[j][i].isalpha()):
                        self.board[j][i] = 'W'
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

    def four_boats_line(self, four_boats:list , row):
        "Procura numa linha(row) quatro posicoes seguidas para colocar um barco"
        "e armazena-os no em four_boats"

        for column in range(COLUMNS-3):
            if self.board[row][column] == 'L' or self.board[row][column] == '0':
                second_pos = self.board[row][column+1]
                third_pos = self.board[row][column+2]
                fourth_pos = self.board[row][column+3]
                if ((second_pos == 'M' or second_pos == '0') and
                    (third_pos == 'M' or third_pos == '0') and
                    (fourth_pos == 'R' or fourth_pos == '0')):
                        four_boats.append(Four_boat((row,column),(row,column+1),
                                            (row,column+2), (row,column+3), HORIZONTAL))
        pass

    def four_boats_column(self, four_boats:list , column):
        "Procura numa coluna(column) quatro posições seguidas para colocar um barco"
        "e armazena-os no em four_boats"

        for row in range(ROWS-3):
            if self.board[row][column] == 'T' or self.board[row][column] == '0':
                second_pos = self.board[row+1][column]
                third_pos = self.board[row+2][column]
                fourth_pos = self.board[row+3][column]
                if ((second_pos == 'M' or second_pos == '0') and
                    (third_pos == 'M' or third_pos == '0') and
                    (fourth_pos == 'B' or fourth_pos == '0')):
                        four_boats.append(Four_boat((row,column),(row+1,column),
                                            (row+2,column), (row+3,column), VERTICAL))
        pass

    def three_boats_line(self, three_boats:list , row):
        "Procura numa linha(row) tres posições seguidas para colocar um barco"
        "e armazena-os no em three_boats"

        for column in range(COLUMNS-2):
            if self.board[row][column] == 'L' or self.board[row][column] == '0':
                second_pos = self.board[row][column+1]
                third_pos = self.board[row][column+2]
                if ((second_pos == 'M' or second_pos == '0') and
                    (third_pos == 'R' or third_pos == '0')):
                        three_boats.append(Three_boat((row,column),(row,column+1),
                                            (row,column+2), HORIZONTAL))
        pass

    def three_boats_column(self, three_boats:list, column):
        "Procura numa coluna(column) tres posições seguidas para colocar um barco"
        "e armazena-os no em three_boats"

        for row in range(ROWS-2):
            if self.board[row][column] == 'T' or self.board[row][column] == '0':
                second_pos = self.board[row+1][column]
                third_pos = self.board[row+2][column]
                if ((second_pos == 'M' or second_pos == '0') and
                    (third_pos == 'B' or third_pos == '0')):
                        three_boats.append(Three_boat((row,column),(row+1,column),
                                            (row+2,column), VERTICAL))
        pass

    def two_boats_line(self, two_boats:list, row):
        "Procura numa linha(row) duas posições seguidas para colocar um barco"
        "e armazena-os no em two_boats"

        for column in range(COLUMNS-1):
            if self.board[row][column] == 'L' or self.board[row][column] == '0':
                second_pos = self.board[row][column+1]
                if (second_pos == 'R' or second_pos == '0'):
                    two_boats.append(Two_boat((row,column),(row,column+1), HORIZONTAL))
        pass

    def two_boats_column(self, two_boats:list, column):
        "Procura numa coluna(column) duas posições seguidas para colocar um barco"
        "e armazena-os no em two_boats"

        for row in range(ROWS-1):
            if self.board[row][column] == 'T' or self.board[row][column] == '0':
                second_pos = self.board[row+1][column]
                if (second_pos == 'B' or second_pos == '0'):
                        two_boats.append(Two_boat((row,column),(row+1,column), VERTICAL))
        pass

    def one_boats(self, one_boats:list, row):
        "Procura numa linha (row) uma posicao para colocar um barco"
        "e armazena-o em one_boats"
        
        for column in range(COLUMNS-1):
            if self.board[row][column] == '0':
                one_boats.append(One_boat((row,column)))
        pass

    def look_for_four_boat(self) -> list:
        "Procura no tabuleiro espaços onde colocar barcos de 4"

        all_four_boats = list
        for row in range(ROWS):
            if self.rows[row] > 0 and self.initial_row_value[row] >= 4:
                self.four_boats_line(all_four_boats, row)
        for column in range(COLUMNS):
            if self.columns[column] > 0 and self.initial_column_value[column] >=4:
                self.four_boats_column(all_four_boats, column)

        return all_four_boats
    
    def look_for_three_boat(self) -> list:
        "Procura no tabuleiro espacos onde colocar barcos de 3"

        all_three_boats = list
        for row in range(ROWS):
            if self.rows[row] > 0 and self.initial_row_value[row] >= 3:
                self.three_boats_line(all_three_boats, row)
        for column in range(COLUMNS):
            if self.columns[column] > 0 and self.initial_column_value[column] >=3:
                self.three_boats_column(all_three_boats, column)

        return all_three_boats
    
    def look_for_two_boat(self) -> list:
        "Procura no tabuleiro espacos onde colocar barcos de 2"

        all_two_boats = list
        for row in range(ROWS):
            if self.rows[row] > 0 and self.initial_row_value[row] >= 2:
                self.two_boats_line(all_two_boats, row)
        for column in range(COLUMNS):
            if self.columns[column] > 0 and self.initial_column_value[column] >=2:
                self.two_boats_column(all_two_boats, column)

        return all_two_boats

    def look_for_one_boat(self) -> list:
        "Procura no tabuleiro espacos onde colocar barcos de 1"

        all_one_boats = list
        for row in range(ROWS):
            if self.rows[row] > 0 and self.initial_row_value[row] >= 1:
                self.one_boats(all_one_boats, row)

        return all_one_boats

    def place_four_boat(self, four_boat:Four_boat) -> Action:
        "Recebe um barco de quatro e transforma-o numa ação"

        if (Four_boat[4] == VERTICAL):
            placement1 = Placement('T', four_boat[0])
            placement2 = Placement('M', four_boat[1])
            placement3 = Placement('M', four_boat[2])
            placement4 = Placement('B', four_boat[3])
        
        else:
            placement1 = Placement('L', four_boat[0])
            placement2 = Placement('M', four_boat[1])
            placement3 = Placement('M', four_boat[2])
            placement4 = Placement('R', four_boat[3])

        self.remaining_boats -= 1
        self.remaining_four_boats -=1
        return Action(placement1,placement2,placement3, placement4)
    
    def place_three_boat(self, three_boat: Three_boat) -> Action:
        "Recebe um barco de tres e transforma-o numa acao"
 
        if (Three_boat[3] == VERTICAL):
            placement1 = Placement('T', three_boat[0])
            placement2 = Placement('M', three_boat[1])
            placement3 = Placement('B', three_boat[2])
        
        else:
            placement1 = Placement('L', three_boat[0])
            placement2 = Placement('M', three_boat[1])
            placement3 = Placement('R', three_boat[2])

        self.remaining_boats -= 1
        self.remaining_three_boats -=1
        return Action(placement1,placement2,placement3)
    
    def place_two_boat(self, two_boat: Two_boat) -> Action:
        "Recebe um barco de dois e transforma-o numa acao"

        if (Two_boat[2] == VERTICAL):
            placement1 = Placement('T', two_boat[0])
            placement2 = Placement('B', two_boat[1])
        
        else:
            placement1 = Placement('L', two_boat[0])
            placement2 = Placement('R', two_boat[1])

        self.remaining_boats -= 1
        self.remaining_two_boats -=1
        return Action(placement1,placement2)
    
    def place_one_boat(self, one_boat: One_boat) -> Action:
        "Recebe um barco de um e transforma-o numa açao"

        placement1 = Placement("C", one_boat[0])

        self.remaining_boats -= 0
        self.remaining_one_boats -=1
        return Action(placement1)
    
    def fill_water_row(self , row):
        """ Preenche com agua a respetiva linha do board"""

        for column in range(COLUMNS):
            if (self.board[row][column] == '0'):
                self.board[row][column] = 'W'
    
    def fill_water_column(self , column):
        """ Preenche com agua a respetiva coluna do board"""

        for row in range(ROWS):
            if (self.board[row][column] == '0'):
                self.board[row][column] = 'W'

    def place(self, placement: Placement):
        """Recebe um placement com um simbolo e uma posicao -> Placement(simbolo,posicao)
        e coloca esse simbolo na respetiva posicao do board """

        x = placement[1][0]
        y = placement[1][1]
        simbol = placement[0]

        self.board[x][y] = simbol

        ##reduzir colunas e linhas
        self.rows[x] -= 1
        self.columns[y] -= 1

        #preencher linhas e colunas que chegaram a 0
        if (self.rows[x] == 0):
            self.fill_water_row(x)
        if (self.columns[y] == 0):
            self.fill_water_column(y)

        #preencher com agua a volta dos simbolos 
        if (simbol == 'T'):
            self.fill_water_around_top(x,y)     #ESTAS FUNCOES TEM
        elif (simbol == 'B'):                   # QUE SER ADAPTADAS
            self.fill_water_around_bottom(x,y)         # !!!!!!
        elif (simbol == 'M'):
            self.fill_water_around_middle(x,y)
        elif (simbol == 'R'):
            self.fill_water_around_right(x,y)
        elif (simbol == 'L'):
            self.fill_water_around_left(x,y)
        else:
            self.fill_water_around_circle(x,y)
        pass
    



class BimaruState:
    state_id = 0

    def __init__(self, board:Board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    def look_for_actions(self) -> tuple(Action):
        """ Procura por ações a realizar no estado atual."""

        if (self.board.remaining_four_boats >0):
            return self.board.look_for_four_boat()
        if (self.board.remaining_three_boats >0):
            return self.board.look_for_three_boat()
        if (self.board.remaining_four_boats >0):
            return self.board.look_for_two_boat()
        if (self.board.remaining_two_boats >0):
            return self.board.look_for_one_boat()
    
    def execute(self, action:Action):
        """ Aplica uma ação ao estado atual."""

        for placement in action:
            self.board.place(placement)
        pass




class Bimaru(Problem):

    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = BimaruState(Board)
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        return state.look_for_actions()

    def result(self, state: BimaruState, action:Action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        return state.execute(action)

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        return state.board.remaining_boats == 0

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO:
        pass

    # TODO: outros metodos da classe




def bimaru_read():
    board = Board()
    board.parse_instance(board)
    board.print_board()
    pass

if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    bimaru_read()
    pass



