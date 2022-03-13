
file = open(r'C:\Users\16099\Documents\AOC_21\aoc6_lantern_fish.txt')
by = file.read()

text_lines = by.split("\n")

fish_list = [int(i) for i in text_lines[0].split(',')]
fish_dict = {i:0 for i in range(9)}
for num in fish_list:
    fish_dict[num] += 1

# iterate through list

for _ in range(256):
    new_fish_dict = {i:0 for i in range(9)}
    
    for key,value in fish_dict.items():
        if key == 0:
            new_fish_dict[6] += value
            new_fish_dict[8] = value
            
        else:
            new_fish_dict[key - 1] += value

    fish_dict = new_fish_dict

print(len(fish_dict))
