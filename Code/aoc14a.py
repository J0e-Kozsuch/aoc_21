
file = open(r'C:\Users\16099\Documents\AOC_21\aoc14_pair_insertion.txt')
by = file.read()

text_lines = by.split("\n")


## split text file
polymer = text_lines[0]

insertion_dict = {}

for line in text_lines[2:]:
    pair, insert = line.split(" -> ")
    insertion_dict[pair] = insert



## create insertion function

def insertion_step(polymer):
    new_polymer = polymer[0]

    for index, value in enumerate(polymer[:-1]):

        next_value = polymer[index+1]

        pair = value + next_value

        insert_value = insertion_dict[pair]

        new_polymer += insert_value
        new_polymer += next_value

    return new_polymer


## iterate

element_dict = {}


for _ in range(10):
    polymer = insertion_step(polymer)

for element in polymer:
    try:
        element_dict[element] += 1
    except:
        element_dict[element] = 1
print(element_dict)


