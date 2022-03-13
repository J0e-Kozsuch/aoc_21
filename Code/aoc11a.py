
file = open(r'C:\Users\16099\Documents\AOC_21\aoc11_octopus_flashes.txt')
by = file.read()

text_lines = by.split("\n")

oct_grid = [[int(i) for i in line] for line in text_lines]

flash_count = 0

def list_adjacent_cells(row,col):
    cell_list = []
    if row == 0:
        if col == 0:
            return [(1,0),(0,1),(1,1)]
        elif col == 9:
            return [(0,8),(1,8),(1,9)]
        else:
            return [(0,col - 1),(0,col + 1),(1,col), (1, col -1), (1, col +1)]

    elif row == 9:
        if col == 0:
            return [(9,1),(8,0),(8,1)]
        elif col == 9:
            return [(8,8),(8,9),(9,8)]
        else:
            return [(9,col - 1),(9,col + 1),(8,col), (8, col -1), (8, col +1)]


    if col == 0:
        return [(row-1,0),(row+1,0),(row-1,1), (row, 1), (row+1, 1)]

    elif col == 9:
        return [(row-1,9),(row+1,9),(row-1,8), (row, 8), (row+1, 8)]

    return [(row-1,col-1),(row-1,col),(row-1,col+1),
            (row+1,col-1),(row+1,col), (row+1, col+1),
            (row,col-1),(row, col+1)]
       


def iteration(oct_grid):
    '''
    ADD 1, PROCESS FLASHES UNTIL NO DOUBLE DIGITS. RETURN OCT_GRID
    '''
    global flash_count

    dd_count = 0

    for row in range(10):
        for col in range(10):
            oct_grid[row][col] += 1
            if oct_grid[row][col] > 9:
                dd_count += 1


    while dd_count > 0:
        for row in range(10):
            for col in range(10):
                if oct_grid[row][col] > 9:
                    for adj_row, adj_col in list_adjacent_cells(row,col):
                        if oct_grid[adj_row][adj_col] != 0:
                            oct_grid[adj_row][adj_col] += 1
                            
                    oct_grid[row][col] = 0
                    flash_count += 1

        dd_count = 0
        for row in range(10):
            for col in range(10):
                if oct_grid[row][col] > 9:
                    dd_count += 1
                    
    return oct_grid
                    
                    
                        
            

for _ in range(100):

    oct_grid = iteration(oct_grid)


print(flash_count)

