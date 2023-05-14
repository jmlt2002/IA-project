
import numpy as np

ROWS = 10
COLUMNS = 10

#USEFULL DEFINITIONS
Hint = (str, bool)
Position = (int, int)
Action = (str, Position)

#BOATS
Four_boat = (Position, Position, Position, Position)
Three_boat = (Position, Position, Position)
Two_boat = (Position, Position)
One_boat = Position

board = np.zeros((ROWS, COLUMNS))
rows = np.zeros(ROWS)
columns = np.zeros(COLUMNS)

hints = np.array(Hint)

print(hints)