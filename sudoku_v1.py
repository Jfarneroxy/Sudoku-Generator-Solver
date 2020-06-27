import numpy as np
from random import sample
import ast
import pprint

base = 3
side = base*base

# pattern for a baseline valid solution
def pattern(row,col):
    return (base*(row%base)+row//base+col)%side

# randomize rows, columns and numbers (of valid base pattern)
def shuffle(s):
    return sample(s,len(s))


def generate_empty():
    table=[]
    rangeBase = range(base)
    rows = [ g*base + row for g in shuffle(rangeBase) for row in shuffle(rangeBase) ]
    cols = [ g*base + col for g in shuffle(rangeBase) for col in shuffle(rangeBase) ]
    nums = shuffle(range(1,base*base+1))

    # produce board using randomized baseline pattern
    initial_table = [[nums[pattern(row,col)] for col in cols] for row in rows]
    squares = side*side
    empties = squares * 3//4
    for p in sample(range(squares),empties):
        initial_table[p//side][p%side] = 0

    numSize = len(str(side))


    for line in initial_table:
        line = "[" + "  ".join(f"{n or '0':{numSize}}" + "," for n in line) + "]"
        line = ast.literal_eval(line)
        #print(line)
        table.append(line)

    #print(np.matrix(table))
    #print(table)
    return table



#solves generated table through backtracking
def solve(g_table):
    find = find_empty(g_table)
    if find:
        row, col = find
    else:
        return True

    for i in range(1,10):
        if valid(g_table, (row, col), i):
            g_table[row][col]=i

            if solve(g_table):
                return True
            g_table[row][col] = 0

    return False


def valid(table, pos, num):


    #check row
    for i in range(0, len(table)):
        if table[pos[0]][i] == num and pos[1] != i:
            return False
    #check col
    for i in range(0, len(table)):
        if table[i][pos[1]] == num and pos[1] != i:
            return False

    box_x = pos[1]//3
    box_y = pos[0]//3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 +3):
            if table[i][j] == num and (i,j) != pos:
                return False
    return True

def find_empty(table):
    for i in range(len(table)):
        for j in range(len(table[0])):
            if table[i][j] == 0:
                return(i, j)
    return None



def print_board(table):
    for i in range(len(table)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - -")
        for j in range(len(table[0])):
            if j % 3 ==0:
                print(" | ", end ="")
            if j == 8:
                print(table[i][j], end = "\n")
            else:
                print(str(table[i][j]) + " ", end="")




t = generate_empty()
pp = pprint.PrettyPrinter(width=41, compact = True)
print("here is unsolved sudoku")
print_board(t)

solve(t)
print("here is solved sudoku")
print_board(t)
