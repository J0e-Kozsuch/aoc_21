

BINARY_COVERSION = {'.':'0','#':'1'}


# Read in text file
file = open(r'C:\Users\16099\AppData\Local\Programs\Python\Python310\AOC_21_Puzzle_Input\aoc20_light_pixels.txt')
by = file.read()
file.close()

text_lines = by.split("\n")

enhancement_alg = text_lines[0]

pixel_list_of_lists = [[pixel for pixel in line] for line in text_lines[2:]]

class Pixel_Map:

    def __init__(self, arg_pixel_list_of_lists, border = '.'):
        self._map = arg_pixel_list_of_lists
        self._border = border


    def _add_pixel_border(self):
        '''
         Add two pixel border
         '''
        
        self._map = [[self._border] * 2 + line + [self._border] * 2 for line in self._map]

        horizontal_border = [[self._border] * len(self._map[0])]

        self._map = horizontal_border * 2 + self._map + horizontal_border * 2



    def _enhance_pixel(self, row, col):
        '''
        Given pixel and location of pixel,
        read surrounding pixels and enahance the nine pixels into one
        '''
        top_row = self._map[row-1][col-1:col+2]
        middle_row = self._map[row][col-1:col+2]
        bot_row = self._map[row+1][col-1:col+2]

        flattened_binary = ''

        for pixel in top_row + middle_row + bot_row:
            flattened_binary += BINARY_COVERSION[pixel]

        binary_num = int(flattened_binary, 2)

        return enhancement_alg[binary_num]

    def _change_border(self):
        if self._border == '.':
            self._border = '#'
        else:
            self._border = '.'


    def enhance(self):
        '''
        Given original pixel map (without border)
        creates enhanced pixel map with two additional rows and columns
        '''
        self._add_pixel_border()

        row_width = len(self._map[0]) - 1

        new_map = []

        for row in range(1, len(self._map) - 1):
            new_row = []

            for col in range(1, row_width):
                new_row.append( self._enhance_pixel(row,col) )

            new_map.append(new_row)

        self._map = new_map

        self._change_border()

    def count_lit_pixels(self):

        count = 0

        for row in self._map:
            for pixel in row:
                if pixel == '#':
                    count += 1

        return count
                    
                
            
pixel_map = Pixel_Map(pixel_list_of_lists)

for _ in range(50):
    pixel_map.enhance()


print(pixel_map.count_lit_pixels())


