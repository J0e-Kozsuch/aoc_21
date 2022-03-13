
import re
import itertools
import datetime as dt

# Read in text file
file = open(r'C:\Users\16099\AppData\Local\Programs\Python\Python310\AOC_21_Puzzle_Input\aoc19_scanners.txt')
by = file.read()
file.close()

text_lines = by.split("\n")


# Read text lines and interpret
scanner_beacon_dict = {}

beacon_list = []
scanner_num = '0'
for line in text_lines[1:]:
    
    if line == '':
        continue
    
    elif line[:2] == '--':
        
        scanner_beacon_dict[scanner_num] = [(point[0],point[1],point[2]) for point in beacon_list]
        
        beacon_list = []
        scanner_num = re.findall('\d{1,3}',line)[0]

    else:
        beacon_list.append([int(x) for x in line.split(',')])


scanner_beacon_dict[scanner_num] = [(point[0],point[1],point[2]) for point in beacon_list]



class beacon_map:

    def __init__(self):
        self._coord_points = []

    def set_coord_points(self, a_list):
        self._coord_points = a_list

    def add_coord_points(self, a_list):
        new_set = self._coord_points + a_list
        self._coord_points = list(set(new_set))

    def get_coord_points(self):
        return self._coord_points

    

def create_shifted_maps(coord_list):
    
    transformed_dict = {}
    
    for index, point in enumerate(coord_list):
        transformed_points = [(0,0,0)]
        
        x_shift = -point[0]
        y_shift = -point[1]
        z_shift = -point[2]

        coord_list_copy = coord_list[:]

        coord_list_copy.pop(index)

        for secondary_point in coord_list_copy:
            transformed_points.append(
                                      (secondary_point[0] + x_shift,\
                                       secondary_point[1] + y_shift,\
                                       secondary_point[2] + z_shift)
                                      )
        
        transformed_dict[(x_shift,y_shift,z_shift)] = transformed_points


    return transformed_dict

                                       
def create_rotated_maps(coord_list):
    
    odd_rotations = [(0,2,1),(1,0,2),(2,1,0)]
    odd_rotation_multipliers = [(1,1,-1), (1,-1,1),(-1,-1,-1),(-1,1,1)]

    even_rotations = [(0,1,2),(1,2,0),(2,0,1)]
    even_rotation_multipliers = [(1,1,1), (1,-1,-1),(-1,-1,1),(-1,1,-1)]
    
    list_of_lists = []

    for rotation in odd_rotations:
        for mult in odd_rotation_multipliers:

            new_coord_list = []
            for point in coord_list:
                new_coord_list.append(
                                        (point[rotation[0]] * mult[0],
                                         point[rotation[1]] * mult[1],
                                         point[rotation[2]] * mult[2])
                                    )
            list_of_lists.append(new_coord_list)

    for rotation in even_rotations:
        for mult in even_rotation_multipliers:

            new_coord_list = []
            for point in coord_list:
                new_coord_list.append(
                                        (point[rotation[0]] * mult[0],
                                         point[rotation[1]] * mult[1],
                                         point[rotation[2]] * mult[2])
                                    )
            list_of_lists.append(new_coord_list)

                                         
    return list_of_lists







# create list of beacon_map objects

all_beacon_map_list = [beacon_map() for _ in range(len(scanner_beacon_dict))]

for index, b_map in enumerate(all_beacon_map_list):
    b_map.set_coord_points( scanner_beacon_dict[str(index)] )


# combine the beacon_maps
start = dt.datetime.now()

prev_len = len(all_beacon_map_list)+1

while len(all_beacon_map_list) > 1:
    # break if last iteration did not join two maps
    if prev_len == len(all_beacon_map_list):
        break
    prev_len = len(all_beacon_map_list)
    
    end = dt.datetime.now()
    diff = end - start
    print(len(all_beacon_map_list), diff.seconds)
    
    match = False

    # create rotated, then shifted maps for all except 1st.
    # These are calculated before comparing to reference map. 1st map will be first reference map that will not be rotated.

    beacon_rotated_map_list = [create_rotated_maps(b_map.get_coord_points()) for b_map in all_beacon_map_list[1:]]
    
    beacon_shifted_map_list = [[list(create_shifted_maps(b_map).values()) for b_map in unique_b_map] for unique_b_map in beacon_rotated_map_list]

    # iterate through 0 to second to last map as reference.
    # Subsequent will be rotated and shifted. If match found, append to reference map. continue
    for ref_index, og_reference_map in enumerate(all_beacon_map_list[:-1]):
        reference_shifted_map_dict = create_shifted_maps(og_reference_map.get_coord_points())

        for shift, ref_map in reference_shifted_map_dict.items():

            for sub_index, sub_map_list in enumerate(beacon_shifted_map_list):
                if ref_index > sub_index:
                    continue

                for sub_shifted_b_map_list in sub_map_list:
                    for sub_rotated_b_map in sub_shifted_b_map_list:
                        
                        sub_b_map_set = set(sub_rotated_b_map)
                        ref_b_map_set = set(ref_map)

                        if len(ref_b_map_set.intersection(sub_b_map_set)) >= 12:

                            all_beacon_map_list.pop(sub_index+1)
                            all_beacon_map_list.pop(ref_index)

                            new_map_coord = ref_b_map_set.union(sub_b_map_set)
                            # shift back to original position relative to sensor
                            new_map_coord = [(point[0] - shift[0],point[1] - shift[1],point[2] - shift[2]) for point in new_map_coord]

                            new_map = beacon_map()
                            new_map.set_coord_points( new_map_coord )

                            all_beacon_map_list = [new_map] + all_beacon_map_list

                            match = True
                            break
                    if match:
                        break
                    
                if match:
                    break
                
            if match:
                break

        if match:
            break

    
    





    

         
