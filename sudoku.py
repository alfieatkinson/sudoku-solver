import os
from z3 import *
from itertools import combinations

def exactly_one(literals: list[list[list[any]]]) -> bool:
    c = []
    for pair in combinations(literals, 2):
        a, b = pair[0], pair[1]
        c += [Or(Not(a), Not(b))]
    # At least one is true
    c += [Or(literals)]
    return And(c)

def show(model, literals: list[list[list[any]]]) -> None:
    lines = []
    for i in range(9):
        lines += [[]]
        for j in range(9):
            digit = 0
            for x in range(9):
                if model.evaluate(literals[i][j][x]):
                    digit = x + 1
            lines[i] += [digit]
    
    for line in lines:
        print(" ".join([str(x) for x in line]))

def solve(grid: list[list[int]]):
    # Define the literals
    # Sudoku: 9x9 grid
    # For each cell there are 9 different digits
    # literals: 9x9x9 grid
    literals = []
    for i in range(9):
        literals += [[]]
        for j in range(9):
            literals[i] += [[]]
            for digit in range(9):
                literals[i][j] += [Bool("x_%i_%i_%i" % (i, j, digit))]

    # Create a solver instance
    s = Solver()

    # Add the first set of constraints
    # Only one possible value per cell
    for i in range(9):
        for j in range(9):
            s.add(exactly_one(literals[i][j]))

    # Each value should be used only once per row
    for i in range(9):
        for x in range(9):
            row = []
            for j in range(9):
                row += [literals[i][j][x]]
            s.add(exactly_one(row))

    # Each value should be used only once per column
    for j in range(9):
        for x in range(9):
            s.add(exactly_one([literals[i][j][x] for i in range(9)]))

    # Each value used only once in each subgrid
    # 3x3 subgrids, each with 3x3 cells
    for i in range(3):
        for j in range(3):
            for k in range(9):
                cells = []
                for x in range(3):
                    for y in range(3):
                        cells += [literals[3 * i + x][3 * j + y][k]]
                s.add(exactly_one(cells))

    # Now assume grid[][] represents the values in the grid
    # 0 means there is no value
    # We add the constraints
    for i in range(9):
        for j in range(9):
            if grid[i][j] > 0:
                s.add(literals[i][j][grid[i][j] - 1])

    if str(s.check()) == 'sat':
        show(s.model(), literals)
    else:
        print('unsat')


if __name__ == '__main__':
    file = os.path.realpath(__file__) + "\\..\\inputs\\grid1.txt"
    grid = []
    with open(file, 'r') as F:
        for line in F.readlines():
            grid.append([int(x) for x in line.split(" ")])
        #print(grid)
        solve(grid)
        exit(0)