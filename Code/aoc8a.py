
file = open(r'C:\Users\16099\Documents\AOC_21\aoc8_number_output.txt')
by = file.read()

text_lines = by.split("\n")

code_list = []

for line in text_lines:
    seven_segment_codes, outputs = line.split('|')
    code_list.append(
                    (seven_segment_codes.strip().split(" "),
                       outputs.strip().split(" "))
                      )
    

# count the number of 1, 4, 7, 8

num_dict = {num:0 for num in range(10)}

for _, four_outputs in code_list:

    for output in four_outputs:
        length = len(output)

        if length == 2:
            num_dict[1] += 1
        elif length == 4:
            num_dict[4] += 1
        elif length == 3:
            num_dict[7] += 1
        elif length == 7:
            num_dict[8] += 1
        else:
            pass

print(num_dict)
