import datetime as dt


file = open(r'C:\Users\16099\Documents\AOC_21\aoc14_pair_insertion.txt')
by = file.read()

text_lines = by.split("\n")


## split text file
polymer = text_lines[0]

insertion_dict = {}

for line in text_lines[2:]:
    pair, insert = line.split(" -> ")
    insertion_dict[pair] = insert



## recursive function

##
##def recur_function(poly,count):
##    global element_dict
##
##    if count == TOTAL_STEPS:
##        try:
##            element_dict[poly[0]] += 1
##        except:
##            element_dict[poly[0]] = 1
##        try:
##            element_dict[poly[1]] += 1
##        except:
##            element_dict[poly[1]] = 1
##
##        return None
##
##    for index, element in enumerate(poly[:-1]):
##        next_element = poly[index+1]
##
##        pair = element + next_element
##
##        insert_element = insertion_dict[pair]
##
##        recur_function(element + insert_element + next_element, count + 1)
##        

pair_dict = {}

for index, element in enumerate(polymer[:-1]):
    next_element = polymer[index+1]

    pair = element + next_element

    try:
        pair_dict[pair] += 1
    except:
        pair_dict[pair] = 1


for _ in range(40):
    new_pair_dict = {}
    for pair, count in pair_dict.items():
        
        insert_element = insertion_dict[pair]

        try:
            new_pair_dict[pair[0] + insert_element] += count
        except:
            new_pair_dict[pair[0] + insert_element] = count
        try:
            new_pair_dict[insert_element + pair[1]] += count
        except:
            new_pair_dict[insert_element + pair[1]] = count

    pair_dict = new_pair_dict

    
## count elements from pairs

element_dict = {polymer[-1]: 1}

for pair,count in pair_dict.items():

    try:
        element_dict[pair[0]] += count
    except:
        element_dict[pair[0]] = count

        
print(max(element_dict.values()) - min(element_dict.values()))
