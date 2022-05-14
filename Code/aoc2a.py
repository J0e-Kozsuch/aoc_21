import csv



class Sub:
    def __init__(self, x_pos = 0, y_pos = 0):
        self._x_pos = x_pos
        self._y_pos = y_pos

    def move(self, string):
        direction, distance = string.split(' ')

        if direction == 'forward':
            self._x_pos += int(distance)

        elif direction == 'down':
            self._y_pos += int(distance)

        elif direction == 'up':
            self._y_pos -= int(distance)

        else:
            raise Exception('undefined direction')
    


 

file = open(r'C:\Users\16099\Documents\AOC_21\aoc2_movement.csv')
reader = csv.reader(file)

sub = Sub()
count = 0

for line in reader:
    count+=1
    sub.move(line[0])
    if count == 6:
        break
