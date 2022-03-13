
import numpy as np
from itertools import combinations
import time

class Cuboid:

    def __init__(self,
                 x_min, x_max,
                 y_min, y_max,
                 z_min, z_max,
                 value
                 ):

        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.z_min = z_min
        self.z_max = z_max

        self.value = value

        self.vertices = self._list_vertices()



    def min_max_corners(self):
        return {'min': (self.x_min, self.y_min, self.z_min), 'max': (self.x_max, self.y_max, self.z_max) }


    def _list_vertices(self):

        vertices = []
        
        for x in [self.x_min, self.x_max]:
            for y in [self.y_min, self.y_max]:
                for z in [self.z_min, self.z_max]:
                    vertices.append((x,y,z))

        return vertices


    def calculate_volume(self):

        x = self.x_max - self.x_min
        y = self.y_max - self.y_min
        z = self.z_max - self.z_min

        return x * y * z

                    

class Reactor_Grid:

    def __init__(self):
        self.cuboids = []

    def _intersecting_point(self, cuboid1, cuboid2):
        '''
        given cuboid variables, find all possible points where their extended planes could interesect
        '''

        cuboid1_min, cuboid1_max = list(cuboid1.min_max_corners().values())
        cuboid2_min, cuboid2_max = list(cuboid2.min_max_corners().values())

        x_values = list( set([cuboid1_min[0], cuboid1_max[0], cuboid2_min[0], cuboid2_max[0] ]) )
        y_values = list( set([cuboid1_min[1], cuboid1_max[1], cuboid2_min[1], cuboid2_max[1] ]) )
        z_values = list( set([cuboid1_min[2], cuboid1_max[2], cuboid2_min[2], cuboid2_max[2] ]) )

        points = []

        for x in x_values:
            for y in y_values:
                for z in z_values:
                    
                    points.append([x, y, z])

        return points

    
    
    def _is_cuboid_in_cuboid(self, cuboid1, cuboid2):
        '''
        given two cuboids, determine if the first is within second
        '''

        cuboid1_min, cuboid1_max = list(cuboid1.min_max_corners().values())

        cuboid2_min, cuboid2_max = list(cuboid2.min_max_corners().values())

        if cuboid1_min == cuboid2_min and cuboid1_max == cuboid2_max:
            return 'equal'

        if cuboid1_min[0] >= cuboid2_min[0] and \
           cuboid1_min[1] >= cuboid2_min[1] and \
           cuboid1_min[2] >= cuboid2_min[2] and \
           cuboid1_max[0] <= cuboid2_max[0] and \
           cuboid1_max[1] <= cuboid2_max[1] and \
           cuboid1_max[2] <= cuboid2_max[2]:
            return 'first_in_second'

        if cuboid1_min[0] <= cuboid2_min[0] and \
           cuboid1_min[1] <= cuboid2_min[1] and \
           cuboid1_min[2] <= cuboid2_min[2] and \
           cuboid1_max[0] >= cuboid2_max[0] and \
           cuboid1_max[1] >= cuboid2_max[1] and \
           cuboid1_max[2] >= cuboid2_max[2]:
            return 'second_in_first'

        return 'false'
            
           
            

    def create_all_cuboids_from_two(self, cuboid1, cuboid2):
        '''
        receive two cuboids and find all possible cuboids
        return null if no cuboid in both of others
        return cuboid object with value = 1 if it is in both
        '''
        
        start = time.time()
        points = self._intersecting_point(cuboid1, cuboid2)
        intersecting_time = time.time() - start

        cuboid_in_cuboid_time = 0

        for first_index, first_point in enumerate(points[:-1]):
            for second_point in points[first_index + 1:]:
                # look for min and max corners. exclude those that are tangential
                x_match = first_point[0] == second_point[0]
                y_match = first_point[1] == second_point[1]
                z_match = first_point[2] == second_point[2]

                if not (x_match or y_match or z_match):
                    x_min = min(first_point[0], second_point[0])
                    x_max = max(first_point[0], second_point[0])
                    
                    y_min = min(first_point[1], second_point[1])
                    y_max = max(first_point[1], second_point[1])

                    z_min = min(first_point[2], second_point[2])
                    z_max = max(first_point[2], second_point[2])

                    sub_cuboid = Cuboid( x_min, x_max, y_min, y_max, z_min, z_max, 1)

                    start = time.time()
                    in_first = self._is_cuboid_in_cuboid(sub_cuboid, cuboid1)
                    in_second = self._is_cuboid_in_cuboid(sub_cuboid, cuboid2)
                    cuboid_in_cuboid_time += (time.time() - start)
                    

                    if in_first == 'first_in_second' and in_second == 'first_in_second':
                        
                        return [sub_cuboid, intersecting_time, cuboid_in_cuboid_time]
                    
        return [None,  intersecting_time, cuboid_in_cuboid_time]

        

    def split_cuboids(self, inside_cuboid, og_cuboid1, og_cuboid2):
        '''
        given the insisde_cuboid is within the other two,
        split the other two into distinct cuboids
        discard any cuboids with 0 value

        May return cuboids that overlap as it only discards ones that encompass others
        '''
        
        new_cuboids = []

        inside_vertices = inside_cuboid.vertices

        for og_cuboid in [og_cuboid1, og_cuboid2]:

            value = og_cuboid.value

            if value == 0:
                continue

            og_cuboid_vertices = og_cuboid.vertices

            comb_verts = og_cuboid_vertices + inside_vertices

            x_values = set( [ vert[0] for vert in comb_verts ] )
            x_pairs = [ [min(pair), max(pair)] for pair in combinations(x_values, 2) ]
            
            y_values = set( [ vert[1] for vert in comb_verts ] )
            y_pairs = [ [min(pair), max(pair)] for pair in combinations(y_values, 2) ]
            
            z_values = set( [ vert[2] for vert in comb_verts ] )
            z_pairs = [ [min(pair), max(pair)] for pair in combinations(z_values, 2) ]

            for x_min, x_max in x_pairs:
                for y_min, y_max in y_pairs:
                    for z_min, z_max in z_pairs: 

                        new_cuboid = Cuboid(x_min, x_max, y_min, y_max, z_min, z_max, value)

                        new_cuboids.append( new_cuboid )

        pop_list = []

        # Remove new cuboid that encompasses another
        
        for index1, cuboid1 in enumerate(new_cuboids[:-1]):
            for index2, cuboid2 in enumerate(new_cuboids[index1 + 1: ]):
                encompass = self._is_cuboid_in_cuboid(cuboid1, cuboid2)
                
                if encompass == 'false':
                    continue
                elif encompass == 'first_in_second':
                    pop_list.append( index1 + index2 + 1 )
                elif encompass == 'second_in_first':
                    pop_list.append( index1 )
                elif encompass == 'equal':
                    pop_list.append( index1 )
                else:
                    pass

        pop_list = list( set( pop_list ))
        
        pop_list.sort(reverse = True)

        for index in pop_list:
            new_cuboids.pop(index)


        ## Ensure new cuboids are in existing cuboids

        return_list = []

        for cuboid in new_cuboids:
            in_first = self._is_cuboid_in_cuboid(cuboid, og_cuboid1)
            in_second = self._is_cuboid_in_cuboid(cuboid, og_cuboid2)

            if in_first or in_second:
                return_list.append(cuboid)

            

        return return_list 
            
                    
        


    def iterate_cuboids_for_overlap(self, start_index):
        '''
        single run on comparing all cuboids to check for overlap
        '''

        cuboid_in_cuboid_time = 0
        intersecting_time = 0
        finding_intersect_time = 0
        split_cuboid_time = 0
        
        for index1, cuboid1 in enumerate(self.cuboids[start_index:]):
            for index2, cuboid2 in enumerate(self.cuboids[index1+1:]):

                start = time.time()
                intersecting_cuboid,  intersecting_time_temp, cuboid_in_cuboid_time_temp = self.create_all_cuboids_from_two(cuboid1, cuboid2)
                finding_intersect_time_temp = time.time() - start - intersecting_time_temp - cuboid_in_cuboid_time_temp

                finding_intersect_time += finding_intersect_time_temp
                intersecting_time += intersecting_time_temp
                cuboid_in_cuboid_time += cuboid_in_cuboid_time_temp
                
                if intersecting_cuboid is not None: 
                    start = time.time()
                    split_cuboids = self.split_cuboids( intersecting_cuboid, cuboid1, cuboid2)
                    split_cuboid_time = time.time() - start

                    self.cuboids.pop(start_index + index1 + 1 + index2)
                    self.cuboids.pop(start_index + index1)
                    

##                    print(cuboid1.min_max_corners())
##                    print(cuboid2.min_max_corners())
##                    for cuboid in split_cuboids:
##                        print(cuboid.value, "___" , cuboid.min_max_corners())

                    split_cuboids = [cuboid for cuboid in split_cuboids if cuboid.value == 1]

                    self.cuboids += split_cuboids
                    
                    return [start_index, cuboid_in_cuboid_time, intersecting_time, finding_intersect_time, split_cuboid_time]

        return [start_index + 1, cuboid_in_cuboid_time, intersecting_time, finding_intersect_time, split_cuboid_time]

            

    def process_cuboids(self):

        start_index = 0

        print("Length of Cuboids: "+ str(len(self.cuboids)))

        while start_index < len(self.cuboids):

            [start_index,\
             cuboid_in_cuboid_time, intersecting_time,\
             finding_intersect_time, split_cuboid_time] = self.iterate_cuboids_for_overlap(start_index)
##            print(f"cuboid_in_cuboid_time: {cuboid_in_cuboid_time} \n \
##                  intersecting_time: {intersecting_time} \n \
##                  finding_intersect_time: {finding_intersect_time} \n \
##                  split_cuboid_time: {split_cuboid_time}")
            print("Length of Cuboids: "+ str(len(self.cuboids)))

        

    
        

    def interpret_line(self, line):
        '''
        given line of input, interpret and convert cube values
        '''
        instruction = line.split(" ")[0]

        if instruction == 'on':
            value = 1
        elif instruction == 'off':
            value = 0
        else:
            raise Exception("instruction is not on or off")

        coord_ranges_raw = line.split(" ")[1]
        x_range_raw, y_range_raw, z_range_raw = line.split(",")

        x_min, x_max = [int(i) for i in x_range_raw.split("=")[1].split("..")]

        y_min, y_max = [int(i) for i in y_range_raw.split("=")[1].split("..")]

        z_min, z_max = [int(i) for i in z_range_raw.split("=")[1].split("..")]

        self.cuboids.append(Cuboid(x_min, x_max, y_min, y_max, z_min, z_max, value))




# Read in text file
file = open(r'C:\Users\16099\AppData\Local\Programs\Python\Python310\AOC_21_Puzzle_Input\aoc22_cube_steps.txt')
by = file.read()
file.close()


text_lines = by.split("\n")

reactor_grid = Reactor_Grid()

for line in text_lines[:20]:
    reactor_grid.interpret_line(line)

reactor_grid.process_cuboids()
    
total_volume = 0
for cuboid in reactor_grid.cuboids:
    total_volume += cuboid.calculate_volume()

print(total_volume)

