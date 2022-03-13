
file = open(r'C:\Users\16099\Documents\AOC_21\aoc10_syntax_errors.txt')
by = file.read()

text_lines = by.split("\n")

point_dict = {')': 3, ']': 57, '}': 1197, '>': 25137}
char_dict = {'(':')','[':']','{':'}','<':'>'}

reverse_char_dict = {value:key for key,value in char_dict.items()}


total_points = 0

for line in text_lines:
    open_stack = []

    for char in line:
        if char in char_dict.keys():
            open_stack.append(char)
        else:
            expected_open = reverse_char_dict[char]
            if open_stack[-1] == expected_open:
                open_stack.pop(-1)
            else:
                points = point_dict[char]
                total_points += points
                break

print(total_points)


    
        
           

            
            
        
