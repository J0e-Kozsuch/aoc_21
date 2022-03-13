
import re
import itertools
import copy
import datetime as dt


ODD_ROTATIONS = [(0,2,1),(1,0,2),(2,1,0)]
ODD_ROTATIONS_MULTIPLIER = [(1,1,-1), (1,-1,1),(-1,-1,-1),(-1,1,1)]

EVEN_ROTATIONS = [(0,1,2),(1,2,0),(2,0,1)]
EVEN_ROTATIONS_MULTIPLIER = [(1,1,1), (1,-1,-1),(-1,-1,1),(-1,1,-1)]

ALL_ROTATIONS_AND_MULTS = list(itertools.product(EVEN_ROTATIONS, EVEN_ROTATIONS_MULTIPLIER)) + \
                          list(itertools.product(ODD_ROTATIONS, ODD_ROTATIONS_MULTIPLIER))

class object_map:

    def __init__(self, beacons, sensors, shift = None):
        self._beacons = beacons
        self._sensors = sensors
        self._shift = shift

    def set_sensors(self, sensors):
        self._sensors = sensors

    def set_beacons(self, beacons):
        self._beacons = beacons

    def set_shift(self, shift):
        self._shift = shift

    def get_beacons(self):
        return self._beacons

    def get_sensors(self):
        return self._sensors

    def get_shift(self):
        return self._shift


    

def create_shifted_maps(object_map_):
    '''
    create new object map for each beacon in inputed map
    each new map will be shifted relative to the point
    '''
    
    transformed_objects = []

    sensor_list = object_map_.get_sensors()
    beacon_list = object_map_.get_beacons()
    
    for ref_beacon in beacon_list:
        
        x_shift = -ref_beacon[0]
        y_shift = -ref_beacon[1]
        z_shift = -ref_beacon[2]

        transformed_beacons = []

        for beacon in beacon_list:
            transformed_beacons.append(
                  (beacon[0] + x_shift,\
                   beacon[1] + y_shift,\
                   beacon[2] + z_shift)
                  )
            
        transformed_sensors = []

        for sensor in sensor_list:
            transformed_sensors.append(
                  (sensor[0] + x_shift,\
                   sensor[1] + y_shift,\
                   sensor[2] + z_shift)
                  )

        new_object = object_map(beacons = transformed_beacons, \
                                sensors = transformed_sensors, \
                                shift = (x_shift,y_shift,z_shift)
                                )
        
        transformed_objects.append(new_object)
        
    return transformed_objects

                                       
def create_rotated_maps(object_map_):
    '''
    create new object map for 24 possible rotations
    '''

    beacons = object_map_.get_beacons()
    sensors = object_map_.get_sensors()
    
    new_objects = []

    for rotation, mult in ALL_ROTATIONS_AND_MULTS:

        new_beacons = []
        for beacon in beacons:
            new_beacons.append(
                (beacon[rotation[0]] * mult[0],
                 beacon[rotation[1]] * mult[1],
                 beacon[rotation[2]] * mult[2])
                                )
        new_sensors = []
        for sensor in sensors:
            new_sensors.append(
                (sensor[rotation[0]] * mult[0],
                 sensor[rotation[1]] * mult[1],
                 sensor[rotation[2]] * mult[2])
                                )
        new_object = object_map(beacons = new_beacons, sensors = new_sensors)

        new_objects.append(new_object)

                                         
    return new_objects



def init_object_maps():

    # Read in text file
    file = open(r'C:\Users\16099\AppData\Local\Programs\Python\Python310\AOC_21_Puzzle_Input\aoc19_scanners.txt')
    by = file.read()
    file.close()

    text_lines = by.split("\n")

    # Read text lines and interpret
    object_map_list = []

    for line in text_lines:
        
        if line == '':
            new_object = object_map(beacons = [(point[0],point[1],point[2]) for point in beacon_list], \
                                    sensors = [(0,0,0)])
            object_map_list.append(new_object)
        
        elif line[:2] == '--':
            beacon_list = []
            scanner_num = re.findall('\d{1,3}',line)[0]

        else:
            beacon_list.append([int(x) for x in line.split(',')])

    new_object = object_map(beacons = [(point[0],point[1],point[2]) for point in beacon_list], \
                                    sensors = [(0,0,0)])
    object_map_list.append(new_object)

    return object_map_list






object_map_list = init_object_maps()


# combine
start = dt.datetime.now()

prev_len = len(object_map_list)+1

while len(object_map_list) > 1:
    # break if last iteration did not join two maps
    if prev_len == len(object_map_list):
        break
    
    prev_len = len(object_map_list)
    
    end = dt.datetime.now()
    diff = end - start
    print(len(object_map_list), diff.seconds)
    
    match = False

    # create rotated, then shifted maps for all except 1st.
    # These are calculated before comparing to reference map. 1st map will be first reference map that will not be rotated.

    beacon_rotated_map_list = [create_rotated_maps(b_map) for b_map in object_map_list[1:]]
    
    beacon_shifted_map_list = [[create_shifted_maps(b_map) for b_map in unique_b_map] for unique_b_map in beacon_rotated_map_list]

    # iterate through 0 to second to last map as reference.
    # Subsequent will be rotated and shifted. If match found, append to reference map. continue
    for ref_index, reference_object in enumerate(object_map_list[:-1]):
        reference_shifted_map_list = create_shifted_maps(reference_object)

        for reference_shifted_map in reference_shifted_map_list:
            shift = reference_shifted_map.get_shift()
            ref_beacons = reference_shifted_map.get_beacons()
            ref_sensors = reference_shifted_map.get_sensors()

            for sub_index, sub_map_list in enumerate(beacon_shifted_map_list):
                if ref_index > sub_index:
                    continue

                for sub_shifted_map_list in sub_map_list:
                    for sub_rotated_object_map in sub_shifted_map_list:

                        sub_rotated_beacons = sub_rotated_object_map.get_beacons()
                        sub_rotated_sensors = sub_rotated_object_map.get_sensors()
                        
                        sub_b_map_set = set(sub_rotated_beacons)
                        ref_b_map_set = set(ref_beacons)

                        if len(ref_b_map_set.intersection(sub_b_map_set)) >= 3:

                            object_map_list.pop(sub_index+1)
                            object_map_list.pop(ref_index)

                            new_beacons = ref_b_map_set.union(sub_b_map_set)

                            new_sensors = ref_sensors + sub_rotated_sensors
                            
                            # shift back to original position
                            new_beacons = [(point[0] - shift[0],point[1] - shift[1],point[2] - shift[2]) for point in new_beacons]

                            new_sensors = [(point[0] - shift[0],point[1] - shift[1],point[2] - shift[2]) for point in new_sensors]
                            
                            new_map = object_map(beacons = new_beacons, sensors = new_sensors)

                            object_map_list = [new_map] + object_map_list

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

    
    
sensor_positions = object_map_list[0].get_sensors()

max_distance = -1

for sensor1 in sensor_positions:
    for sensor2 in sensor_positions:
        manhattan_distance = abs(sensor1[0] - sensor2[0]) + abs(sensor1[1] - sensor2[1]) + abs(sensor1[2] - sensor2[2])

        if manhattan_distance > max_distance:
            print(manhattan_distance)
            max_distance = manhattan_distance


    

         
