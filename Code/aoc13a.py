
file = open(r'C:\Users\16099\Documents\AOC_21\aoc13_paper_folds.txt')
by = file.read()

text_lines = by.split("\n")

dots = [line.split(',') for line in text_lines[:-13]]
folds = [line.split(" ")[-1] for line in text_lines[-12:]]

grid = [['' for _ in range(1311)] for _ in range(895)]

for dot in dots:
    grid[int(dot[1])][int(dot[0])] = '.'

for fold in folds:

    if fold[0] == 'y':
        cut_num = int(fold.split("=")[1])
        
        new_grid = grid[:cut_num][:]

        for line_index, line in enumerate(grid[-1:cut_num:-1]):
            for col_index, value in enumerate(line):
                if value == '.':
                    new_grid[line_index][col_index] = '.'

        grid = new_grid[:]
        

    else:
        cut_num = int(fold.split("=")[1])
        
        new_grid = [[value for value in line[:cut_num]] for line in grid]

        for line_index, line in enumerate(grid):
            for col_index, value in enumerate(line[-1:cut_num:-1]):
                if value == '.':
                    new_grid[line_index][col_index] = '.'

        grid = new_grid[:]

    



