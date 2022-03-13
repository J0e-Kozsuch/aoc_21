
file = open(r'C:\Users\16099\Documents\AOC_21\aoc12_cave_paths.txt')
by = file.read()

text_lines = by.split("\n")

# create path dict
path_list = []
for line in text_lines:
    start, finish = line.split("-")
    path_list.append([start,finish])
    path_list.append([finish,start])
    

# recursive function
def next_cave(path):
    
    current_cave = path[-1]
    all_next_paths = []
    recur = False 

    has_visited_small_cave_twice = False

    lower_ordered_path = [cave for cave in path if (cave.lower() == cave and cave not in ['start','end'])]
    lower_ordered_path.sort()
    
    for index, value in enumerate(lower_ordered_path):
        if value == lower_ordered_path[index-1] and index != 0:
            has_visited_small_cave_twice = True
    
    for con in path_list:
        if con[0] == current_cave and not ((con[1] == con[1].lower() and con[1] in path) and (has_visited_small_cave_twice or con[1] == 'start')) and 'end' != current_cave:
            new_path = path + [con[1]]
            next_branches = next_cave(new_path)
            for next_branch in next_branches:
                all_next_paths.append(next_branch)
            recur = True
            
    if recur:
        return all_next_paths
    else:
        
        return [path]


                              
            
    
        

# call recursive and cummulate paths with end

start_path = ['start']

all_paths = next_cave(start_path)

all_paths_with_end = [path for path in all_paths if 'end' in path]


