
file = open(r'C:\Users\16099\Documents\AOC_21\aoc9_cave_height.txt')
by = file.read()

text_lines = by.split("\n")

text_lines = [[int(num) for num in list(line)] for line in text_lines]

num_rows = len(text_lines)

risk_level_sum = 0

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
            print(row_num_queue)
            print(row_index, col_index, poss_hole)
            risk_level_sum += 1
            risk_level_sum += poss_hole

        row_num_queue.pop(0)

    # check for low nums on right boundary

    poss_hole = row_num_queue[1]
    left = row_num_queue[0]

    if left > poss_hole and ((row_index > 0 and text_lines[row_index - 1][col_index + 1] > poss_hole) or row_index == 0)\
        and ((row_index < num_rows - 1 and text_lines[row_index + 1][col_index + 1] > poss_hole) or row_index == num_rows - 1):
        print(row_index, col_index, poss_hole)
        risk_level_sum += 1
        risk_level_sum += poss_hole

    
        
           

            
            
        
