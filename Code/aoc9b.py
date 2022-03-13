
file = open(r'C:\Users\16099\Documents\AOC_21\aoc9_cave_height.txt')
by = file.read()

text_lines = by.split("\n")

text_lines = [[int(num) for num in list(line)] for line in text_lines]

num_rows = len(text_lines)

low_points = []

for row_index, line in enumerate(text_lines):
    row_num_queue = [9]
    row_num_queue.append(line[0])

    for col_index, num in enumerate(line[1:]):
        
        row_num_queue.append(num)

        right = row_num_queue[2]
        poss_hole = row_num_queue[1]
        left = row_num_queue[0]

        if left > poss_hole < right and ((row_index > 0 and text_lines[row_index - 1][col_index] > poss_hole)  or row_index == 0)\
           and ((row_index < num_rows - 1 and text_lines[row_index + 1][col_index] > poss_hole) or row_index == num_rows - 1):
            low_points.append((row_index, col_index))

        row_num_queue.pop(0)

    # check for low nums on right boundary

    poss_hole = row_num_queue[1]
    left = row_num_queue[0]

    if left > poss_hole and ((row_index > 0 and text_lines[row_index - 1][col_index + 1] > poss_hole) or row_index == 0)\
        and ((row_index < num_rows - 1 and text_lines[row_index + 1][col_index + 1] > poss_hole) or row_index == num_rows - 1):
        
        low_points.append((row_index, col_index + 1))



def return_adjacent(row,column):
    '''
    returns all adjacent points that aren't 9 and haven't been previously selected
    '''
    global grid
    
    adjacent_points = []
    
    if row > 0 and text_lines[row-1][column] != 9 and grid[row-1][column]!=1:
        grid[row-1][column] = 1
        adjacent_points += [(row - 1,column)] + return_adjacent(row-1,column)

    if row < 99 and text_lines[row+1][column] != 9 and grid[row+1][column]!=1:
        grid[row+1][column] = 1
        adjacent_points += [(row + 1,column)] + return_adjacent(row+1,column)

    if column > 0 and text_lines[row][column-1] != 9 and grid[row][column-1]!=1:
        grid[row][column-1] = 1
        adjacent_points += [(row ,column-1)] + return_adjacent(row,column-1)

    if column < 99 and text_lines[row][column+1] != 9 and grid[row][column+1]!=1:
        grid[row][column+1] = 1
        adjacent_points += [(row,column+1)] + return_adjacent(row,column+1)

    return adjacent_points


    
        

# create grid for tracking selections

grid = [[0 for _ in range(100)] for _ in range(100)]


third = 0
second = 0
first = 0

for point in low_points:
    
    adjacent_points = return_adjacent(point[0],point[1])

    basin_size = len(adjacent_points)
    
    if basin_size > third:
        if basin_size > second:
            if basin_size > first:
                third=second
                second=first
                first = basin_size
            else:
                third = second
                second = basin_size
        else:
            third = basin_size
        
        
       

    
        
           

            
            
        
