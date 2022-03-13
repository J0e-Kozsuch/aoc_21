import csv

file = open(r'C:\Users\16099\Documents\AOC_21\aoc1a_ocean_depth.csv')
reader = csv.reader(file)

count = 0
lines = []

prev_value = float("inf")

for line in reader:
    value = int(line[0])
    if value > prev_value:
        count+=1
    lines.append(value)
    prev_value = value
 
