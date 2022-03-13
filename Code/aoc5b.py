
file = open(r'C:\Users\16099\Documents\AOC_21\aoc5_gas_lines.txt')
by = file.read()

text_lines = by.split("\n")


# convert text to rows of two points

lines = [line.split(" -> ") for line in text_lines]
lines = [[[int(i) for i in line[0].split(',')],
         [int(i) for i in line[1].split(',')]]
         for line in lines]

# create grid 0-1000, init values = 0
grid = [[0 for _ in range(1000)] for _ in range(1000)]


# add 1 for each passing line
def draw_line(line):
    global grid
    
    start = line[0]
    finish = line[1]

    if start[0] != finish[0] and start[1] == finish[1]:
        #horizontal
        start_x = start[0]
        finish_x = finish[0]

        y_ind = start[1]

        for x_ind in range(min(start_x,finish_x), max(start_x,finish_x) + 1):
            grid[y_ind][x_ind] += 1
            
    elif start[0] == finish[0]:
        #vertical
        start_y = start[1]
        finish_y = finish[1]

        x_ind = start[0]

        for y_ind in range(min(start_y,finish_y), max(start_y,finish_y) + 1):
            grid[y_ind][x_ind] += 1

    else:
        #diagonal
        x1 = start[0]
        x2 = finish[0]
        steps = abs(x2 - x1)
        direction_x = abs(x2 - x1) / (x2 - x1)

        y1 = start[1]
        y2 = finish[1]
        direction_y = abs(y2 - y1) / (y2 - y1)

        for ind in range(steps + 1):
            grid[int(y1 + ind * direction_y)][int(x1 + ind * direction_x)] += 1
        



for line in lines:
    draw_line(line)


# count double crossed points
count_double_plus = 0

for row in grid:
    for value in row:
        if value > 1:
            count_double_plus += 1

print(count_double_plus)


        
