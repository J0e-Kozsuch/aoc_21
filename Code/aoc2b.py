import csv


class Sub:
    def __init__(self, x_pos = 0, y_pos = 0, aim = 0):
        self._x_pos = x_pos
        self._y_pos = y_pos
        self._aim = aim

    def move(self, string):
        direction, distance = string.split(' ')

        if direction == 'forward':
            self._x_pos += int(distance)
            self._y_pos += self._aim * int(distance)

        elif direction == 'down':
            self._aim += int(distance)

        elif direction == 'up':
            self._aim -= int(distance)

        else:
            raise Exception('undefined direction')
    


 

file = open(r'C:\Users\16099\Documents\AOC_21\aoc2_movement.csv')
reader = csv.reader(file)

sub = Sub()
count = 0

for line in reader:
    count+=1
    sub.move(line[0])
##    if count == 8:
##        break

print(sub._x_pos, sub._y_pos, sub._aim)
