
# Read in text file
file = open(r'C:\Users\16099\AppData\Local\Programs\Python\Python310\AOC_21_Puzzle_Input\aoc22_cube_steps.txt')
by = file.read()
file.close()


text_lines = by.split("\n")




class reactor_grid:

    def __init__(self):

        # offset is what is subtracted from index to locate zero in each range
        # essentially what is the length of negative numbers in each range
        self.x_len = 101
        self.x_offset = 50

        self.y_len = 101
        self.y_offset = 50
        
        self.z_len = 101
        self.z_offset = 50

        # 0 is off, 1 is on
        self.grid = [ [ [ 0 for _ in range(self.z_len)] for _ in range(self.y_len)] for _ in range(self.x_len)]
                

    def _adjust_cubes(self, coordinates, on_off_binary):
        '''
        given list of coordinates and binary, adjust values in self.grid
        '''
        for coord in coordinates:
            x,y,z = coord
            if 0 > x or x > self.x_len or\
               0 > y or y > self.y_len or\
               0 > z or z > self.z_len:
                pass
            else:
                self.grid[x][y][z] = on_off_binary
        

    def interpret_line_and_act(self, line):
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

        coordinate_list = []

        # ranges are inclusive, hence the +1
        for x_coord in range(x_min, x_max + 1):
            for y_coord in range(y_min, y_max + 1):
                for z_coord in range(z_min, z_max + 1):
                    x_index = x_coord + self.x_offset
                    y_index = y_coord + self.y_offset
                    z_index = z_coord + self.z_offset
                    coordinate_list.append((x_index, y_index, z_index))
                    self._adjust_cubes([(x_index,y_index,z_index)], value)

    def count_on_cubes(self):
        count = 0
        
        for x_coord in range(self.x_len):
            for y_coord in range(self.y_len):
                for z_coord in range(self.z_len): 
                    count += self.grid[x_coord][y_coord][z_coord]

        return(count)

        
            
        
r_grid = reactor_grid()


for line in text_lines[:20]:
    r_grid.interpret_line_and_act(line)

print(r_grid.count_on_cubes())

