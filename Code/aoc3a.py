import csv


file = open(r'C:\Users\16099\Documents\AOC_21\aoc3_binary.csv')
reader = csv.reader(file)

bits_sum = [0 for _ in range(12)]
bin_num_count = 0

for line in reader:
    line_bits = [int(x) for x in line[0]]

    bin_num_count += 1
    
    bits_sum = [bits_sum[x] + line_bits[x] for x in range(12)]


gamma = 0
epsilon = 0

for i in range(12):

    exponent = 11 - i
    count_1 = bits_sum[i]

    if count_1 > 500:
        gamma += 2**exponent
    else:
        epsilon += 2**exponent


        
    
