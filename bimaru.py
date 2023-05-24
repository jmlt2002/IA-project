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

# RecordType = Dict[Union[int, str], Set[str]]

Hint = (str, bool)
Position = (int, int)
Placement = (str, Position)
Action = (Placement)

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
        self.hints = 0
        self.all_hints = list()

    def new_duplicate_board(self):
        duplicate_board = Board()
        duplicate_board.board = np.copy(self.board)
        duplicate_board.rows= np.copy(self.rows)
        duplicate_board.columns = np.copy(self.columns)
        duplicate_board.initial_row_value = np.copy(self.initial_row_value)   #listas para guardar os valores iniciais das col e lin
        duplicate_board.initial_column_value = np.copy(self.initial_column_value)  #para passar logo a frente na procura de barcos
        duplicate_board.remaining_boats = self.remaining_boats
        duplicate_board.remaining_four_boats = self.remaining_four_boats
        duplicate_board.remaining_three_boats = self.remaining_three_boats
        duplicate_board.remaining_two_boats = self.remaining_two_boats
        duplicate_board.remaining_one_boats = self.remaining_one_boats
        duplicate_board.hints = self.hints
        duplicate_board.all_hints = self.all_hints
        return duplicate_board
        
    
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
        self.hints = hint_total

        for i in range(hint_total):
            hint = input().split()
            self.board[int(hint[1])][int(hint[2])] = hint[3]

            if(hint[3] == 'W'):
                self.hints -= 1

            elif(hint[3] == 'M'):
                self.fill_water_around_middle(int(hint[1]), int(hint[2]))
            elif(hint[3] == 'C'):
                self.rows[int(hint[1])] -= 1
                self.columns[int(hint[2])] -= 1
                self.remaining_boats -= 1
                self.remaining_one_boats -= 1
                self.hints -= 1
                self.fill_water_around_circle(int(hint[1]), int(hint[2]))
            elif(hint[3] == 'B'):
                self.fill_water_around_bottom(int(hint[1]), int(hint[2]))
            elif(hint[3] == 'T'):
                self.fill_water_around_top(int(hint[1]), int(hint[2]))
            elif(hint[3] == 'L'):
                self.fill_water_around_left(int(hint[1]), int(hint[2]))
            elif(hint[3] == 'R'):
                self.fill_water_around_right(int(hint[1]), int(hint[2]))

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
        
        for i in range(10):
            for j in range(10):
                if(self.board[i][j] == 'W'):
                    print('.', end=' ')
                else:
                    print(self.board[i][j], end=' ')
            print()
        pass

    # FILLS WATER TILES ADJACENT TO SHIPS------------------------------
    def fill_water_around_circle(self, row: int, col: int):
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
    
    def fill_water_around_middle(self, row: int, col: int):
        if(row + 1 < 10 and col + 1 < 10):
            self.board[row+1][col+1] = 'W'
        if(row + 1 < 10 and col - 1 >= 0):
            self.board[row+1][col-1] = 'W'
        if(row - 1 >= 0 and col + 1 < 10):
            self.board[row-1][col+1] = 'W'
        if(row - 1 >= 0 and col - 1 >= 0):
            self.board[row-1][col-1] = 'W'

    def fill_water_around_top(self, row: int, col: int):
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

    def fill_water_around_bottom(self, row: int, col: int):
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
    
    def fill_water_around_right(self, row: int, col: int):
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

    def fill_water_around_left(self, row: int, col: int):
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

    def place_four_boat(self, four_boat:Four_boat) -> Action:
        "Recebe um barco de quatro e transforma-o numa ação"

        if (four_boat[4] == VERTICAL):
            placement1 = ('T', four_boat[0])
            placement2 = ('M', four_boat[1])
            placement3 = ('M', four_boat[2])
            placement4 = ('B', four_boat[3])
        
        else:
            placement1 = ('L', four_boat[0])
            placement2 = ('M', four_boat[1])
            placement3 = ('M', four_boat[2])
            placement4 = ('R', four_boat[3])

        return (placement1,placement2,placement3, placement4)
    
    def place_three_boat(self, three_boat: Three_boat) -> Action:
        "Recebe um barco de tres e transforma-o numa acao"
 
        if (three_boat[3] == VERTICAL):
            placement1 = ('T', three_boat[0])
            placement2 = ('M', three_boat[1])
            placement3 = ('B', three_boat[2])
        
        else:
            placement1 = ('L', three_boat[0])
            placement2 = ('M', three_boat[1])
            placement3 = ('R', three_boat[2])

        return (placement1,placement2,placement3)
    
    def place_two_boat(self, two_boat: Two_boat) -> Action:
        "Recebe um barco de dois e transforma-o numa acao"

        if (two_boat[2] == VERTICAL):
            placement1 = ('T', two_boat[0])
            placement2 = ('B', two_boat[1])
        
        else:
            placement1 = ('L', two_boat[0])
            placement2 = ('R', two_boat[1])

        return (placement1, placement2)
    
    def place_one_boat(self, one_boat: One_boat) -> Action:
        "Recebe um barco de um e transforma-o numa açao"

        placement1 = ("C", one_boat)

        return (placement1,)
    
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

    def place(self, placement : Placement):
        """Recebe um placement com um simbolo e uma posicao -> Placement(simbolo,posicao)
        e coloca esse simbolo na respetiva posicao do board """

        x = placement[1][0]
        y = placement[1][1]
        simbol = placement[0]

        # reduzir colunas e linhas
        if(self.board[x][y] != '0'):
            self.hints -= 1
        
        self.rows[x] -= 1
        self.columns[y] -= 1

        self.board[x][y] = simbol

        #preencher linhas e colunas que chegaram a 0
        if (self.rows[x] == 0):
            self.fill_water_row(x)
        if (self.columns[y] == 0):
            self.fill_water_column(y)

        #preencher com agua a volta dos simbolos 
        if (simbol == 'T'):
            self.fill_water_around_top(x,y)     
        elif (simbol == 'B'):                 
            self.fill_water_around_bottom(x,y)         
        elif (simbol == 'M'):
            self.fill_water_around_middle(x,y)
        elif (simbol == 'R'):
            self.fill_water_around_right(x,y)
        elif (simbol == 'L'):
            self.fill_water_around_left(x ,y)
        else:
            self.fill_water_around_circle(x,y)
        pass

    def four_boats_line(self, four_boats:list , row: int):
        "Procura numa linha(row) quatro posicoes seguidas para colocar um barco"
        "e armazena-os no em four_boats"


        for column in range(COLUMNS-3):

            if (self.columns[column] <= 0):
                continue
            if (self.columns[column+1] <= 0):
                continue
            if (self.columns[column+2] <= 0):
                continue
            if (self.columns[column+3] <= 0):
                continue

            if(not ((column > 0 and self.board[row][column-1] != '0' and self.board[row][column-1] != 'W') or 
                    (column+3 < 9 and self.board[row][column+4] != '0' and self.board[row][column+4] != 'W'))):
                            
                if self.board[row][column] == 'L' or self.board[row][column] == '0':
                    second_pos = self.board[row][column+1]
                    third_pos = self.board[row][column+2]
                    fourth_pos = self.board[row][column+3]
                    if ((second_pos == 'M' or second_pos == '0') and
                        (third_pos == 'M' or third_pos == '0') and
                        (fourth_pos == 'R' or fourth_pos == '0')):
                            f_boat = ((row,column),(row,column+1),
                                                (row,column+2), (row,column+3), HORIZONTAL)
                            four_boats.append(self.place_four_boat(f_boat))
        pass

    def four_boats_column(self, four_boats : list , column):
        "Procura numa coluna(column) quatro posições seguidas para colocar um barco"
        "e armazena-os no em four_boats"
        
        for row in range(ROWS-3):

            if (self.rows[row] <= 0):
                continue
            if (self.rows[row+1] <= 0):
                continue
            if (self.rows[row+2] <= 0):
                continue
            if (self.rows[row+3] <= 0):
                continue

            if(not ((row > 0 and self.board[row-1][column] != '0' and self.board[row-1][column] != 'W') or 
                    (row+3 < 9 and self.board[row+4][column] != '0' and self.board[row+4][column] != 'W'))):
                
                if self.board[row][column] == 'T' or self.board[row][column] == '0':
                    second_pos = self.board[row+1][column]
                    third_pos = self.board[row+2][column]
                    fourth_pos = self.board[row+3][column]
                    if ((second_pos == 'M' or second_pos == '0') and
                        (third_pos == 'M' or third_pos == '0') and
                        (fourth_pos == 'B' or fourth_pos == '0')):
                            f_boat = ((row,column),(row+1,column),
                                                (row+2,column), (row+3,column), VERTICAL)
                            four_boats.append(self.place_four_boat(f_boat))
        pass

    def three_boats_line(self, three_boats:list , row):
        "Procura numa linha(row) tres posições seguidas para colocar um barco"
        "e armazena-os no em three_boats"

        for column in range(COLUMNS-2):

            if (self.columns[column] <= 0):
                continue
            if (self.columns[column+1] <= 0):
                continue
            if (self.columns[column+2] <= 0):
                continue

            if(not ((column > 0 and self.board[row][column-1] != '0' and self.board[row][column-1] != 'W') or 
                    (column+2 < 9 and self.board[row][column+3] != '0' and self.board[row][column+3] != 'W'))):
                
                if self.board[row][column] == 'L' or self.board[row][column] == '0':
                    second_pos = self.board[row][column+1]
                    third_pos = self.board[row][column+2]
                    if ((second_pos == 'M' or second_pos == '0') and
                        (third_pos == 'R' or third_pos == '0')):
                            t_boat = ((row,column),(row,column+1),
                                                (row,column+2), HORIZONTAL)
                            three_boats.append(self.place_three_boat(t_boat))
        pass

    def three_boats_column(self, three_boats:list, column):
        "Procura numa coluna(column) tres posições seguidas para colocar um barco"
        "e armazena-os no em three_boats"

        for row in range(ROWS-2):

            if (self.rows[row] <= 0):
                continue
            if (self.rows[row+1] <= 0):
                continue
            if (self.rows[row+2] <= 0):
                continue


            if(not ((row > 0 and self.board[row - 1][column] != '0' and self.board[row - 1][column] != 'W') or 
                    (row+2 < 9 and self.board[row+3][column] != '0' and self.board[row+3][column] != 'W'))):
                
                if self.board[row][column] == 'T' or self.board[row][column] == '0':
                    second_pos = self.board[row+1][column]
                    third_pos = self.board[row+2][column]
                    if ((second_pos == 'M' or second_pos == '0') and
                        (third_pos == 'B' or third_pos == '0')):
                            t_boat = ((row,column),(row+1,column),
                                                (row+2,column), VERTICAL)
                            three_boats.append(self.place_three_boat(t_boat))
        pass

    def two_boats_line(self, two_boats:list, row):
        "Procura numa linha(row) duas posições seguidas para colocar um barco"
        "e armazena-os no em two_boats"

        for column in range(COLUMNS-1):

            if (self.columns[column] <= 0):
                continue
            if (self.columns[column+1] <= 0):
                continue

            if(not ((column > 0 and self.board[row][column-1] != '0' and self.board[row][column-1] != 'W') or 
                    (column+2 < 9 and self.board[row][column+2] != '0' and self.board[row][column+2] != 'W'))):
                
                if self.board[row][column] == 'L' or self.board[row][column] == '0':
                    second_pos = self.board[row][column+1]
                    if (second_pos == 'R' or second_pos == '0'):
                        t_boat = ((row,column),(row,column+1), HORIZONTAL)
                        two_boats.append(self.place_two_boat(t_boat))
        pass

    def two_boats_column(self, two_boats:list, column):
        "Procura numa coluna(column) duas posições seguidas para colocar um barco"
        "e armazena-os no em two_boats"

        for row in range(ROWS-1):

            if (self.rows[row] <= 0):
                continue
            if (self.rows[row+1] <= 0):
                continue

            if(not ((row > 0 and self.board[row - 1][column] != '0' and self.board[row - 1][column] != 'W') or 
                    (row+2 < 9 and self.board[row+2][column] != '0' and self.board[row+2][column] != 'W'))):
                
                if self.board[row][column] == 'T' or self.board[row][column] == '0':
                    second_pos = self.board[row+1][column]
                    if (second_pos == 'B' or second_pos == '0'):
                            t_boat = ((row,column),(row+1,column), VERTICAL)
                            two_boats.append(self.place_two_boat(t_boat))
        pass

    def one_boats(self, one_boats:list, row):
        "Procura numa linha (row) uma posicao para colocar um barco"
        "e armazena-o em one_boats"
        
        for column in range(COLUMNS):

            if (self.rows[row] <= 0):
                continue

            if self.board[row][column] == '0':
                o_boat = ((row,column))
                one_boats.append(self.place_one_boat(o_boat))
        pass

    def look_for_four_boat(self) -> list:
        """Procura no tabuleiro espaços onde colocar barcos de 4"""

        all_four_boats = list()
        for row in range(ROWS):
            if (self.rows[row] >= 4 and self.initial_row_value[row] >= 4):
                self.four_boats_line(all_four_boats, row)
        for column in range(COLUMNS):
            if (self.columns[column] >= 4 and self.initial_column_value[column] >= 4):
                self.four_boats_column(all_four_boats, column)

        return all_four_boats
    
    def look_for_three_boat(self) -> list:
        """Procura no tabuleiro espacos onde colocar barcos de 3"""

        all_three_boats = list()
        for row in range(ROWS):
            if (self.rows[row] >= 3 and self.initial_row_value[row] >= 3):
                self.three_boats_line(all_three_boats, row)
        for column in range(COLUMNS):
            if (self.columns[column] >= 3 and self.initial_column_value[column] >= 3):
                self.three_boats_column(all_three_boats, column)

        return all_three_boats
    
    def look_for_two_boat(self) -> list:
        """Procura no tabuleiro espacos onde colocar barcos de 2"""

        all_two_boats = list()
        for row in range(ROWS):
            if (self.rows[row] >= 2 and self.initial_row_value[row] >= 2):
                self.two_boats_line(all_two_boats, row)
        for column in range(COLUMNS):
            if (self.columns[column] >= 2 and self.initial_column_value[column] >= 2):
                self.two_boats_column(all_two_boats, column)

        return all_two_boats

    def look_for_one_boat(self) -> list:
        "Procura no tabuleiro espacos onde colocar barcos de 1"

        all_one_boats = list()
        for row in range(ROWS):
            if (self.rows[row] >= 1 and self.initial_row_value[row] >= 1):
                self.one_boats(all_one_boats, row)

        return all_one_boats

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

        if (self.board.hints < 0):
            return tuple()
        if (self.board.remaining_four_boats > 0):
            return self.board.look_for_four_boat()
        if (self.board.remaining_three_boats > 0):
            return self.board.look_for_three_boat()
        if (self.board.remaining_two_boats > 0):
            return self.board.look_for_two_boat()
        if (self.board.remaining_one_boats > 0):
            return self.board.look_for_one_boat()

        return tuple()
    
    def execute(self, action:Action):
        """ Aplica uma ação ao estado atual."""

        child = BimaruState(self.board.new_duplicate_board())
        size = len(action)

        child.board.remaining_boats -= 1
        if (size == 4):
            child.board.remaining_four_boats -= 1
        elif (size == 3):
            child.board.remaining_three_boats -= 1
        elif (size == 2):
            child.board.remaining_two_boats -= 1
        else:
            child.board.remaining_one_boats -= 1

        for placement in action:
            child.board.place(placement)
        
        return child
    



class Bimaru(Problem):

    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = BimaruState(board)
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
        res = state.execute(action)
        return res

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        #if(state.board.remaining_boats != 0):
           # return False
        #for i in range(10):
            #if(state.board.rows[i] != 0):
                ##return False
            #if(state.board.columns[i] != 0):
               # return False
        if (state.board.remaining_boats == 0 and state.board.hints == 0):
                return True
        return False

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO:
        pass

    # TODO: outros metodos da classe




def bimaru_read():
    board = Board()
    board.parse_instance(board)
    return board

if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = bimaru_read()
    bimaru_problem = Bimaru(board)
    result = depth_first_tree_search(bimaru_problem)
    if(result == None):
        print("NO RESULT")
    else:
        result.state.board.print_board()
    pass


