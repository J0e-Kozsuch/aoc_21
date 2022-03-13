import csv

file = open(r'C:\Users\16099\Documents\AOC_21\aoc1a_ocean_depth.csv')
reader = csv.reader(file)

count = 0
lines = []
queue = [10**6, 10**6, 10**6]
prev_sum = sum(queue)

for line in reader:
    value = int(line[0])
    queue.pop(0)
    queue.append(value)
    new_sum = sum(queue)
    if new_sum > prev_sum:
        count+=1
    prev_sum = new_sum
    lines.append(value)
 
