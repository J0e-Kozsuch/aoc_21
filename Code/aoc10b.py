
file = open(r'C:\Users\16099\Documents\AOC_21\aoc10_syntax_errors.txt')
by = file.read()

text_lines = by.split("\n")

point_dict = {'(': 1, '[': 2, '{': 3, '<': 4}
char_dict = {'(':')','[':']','{':'}','<':'>'}

reverse_char_dict = {value:key for key,value in char_dict.items()}

incomplete_scores = []

for line in text_lines:
    corrupted = False
    open_stack = []
    point_total = 0

    for char in line:
        if char in char_dict.keys():
            open_stack.append(char)
        else:
            expected_open = reverse_char_dict[char]
            if open_stack[-1] == expected_open:
                open_stack.pop(-1)
            else:
                corrupted = True
                break
            
    if corrupted:
        continue
    
    open_stack.reverse()

    for char in open_stack:
        point_total *= 5
        point_total += point_dict[char]

    incomplete_scores.append(point_total)
    
print(incomplete_scores)


    
        
           

            
            
        
