import csv


file = open(r'C:\Users\16099\Documents\AOC_21\aoc3_binary.csv')
reader = csv.reader(file)


def create_bit_dict(list_bit_nums, position):
    bit_dict = {0:[], 1:[]}

    for bit_num in list_bit_nums:
        
        if bit_num[position] == 1:
            bit_dict[1].append(bit_num)
        else:
            bit_dict[0].append(bit_num)
        
    return bit_dict


list_bit_nums = []

for line in reader:
    list_bits = [int(x) for x in line[0]]

    list_bit_nums.append(list_bits)
    
    first_bit_nums = list_bit_nums[:]

    
# Find O2
position = 0

while len(list_bit_nums) > 1:

    bit_dict = create_bit_dict(list_bit_nums, position)
    
    if len(bit_dict[0]) > len(bit_dict[1]):
        list_bit_nums = bit_dict[0]
    else:
        list_bit_nums = bit_dict[1]

    position += 1

o2_bit_list = list_bit_nums[0]

# Find CO2

list_bit_nums = first_bit_nums[:]
position = 0

while len(list_bit_nums) > 1:

    bit_dict = create_bit_dict(list_bit_nums, position)

    print(len(bit_dict[0]), len(bit_dict[1]))
    
    if len(bit_dict[1]) < len(bit_dict[0]):
        list_bit_nums = bit_dict[1]
    else:
        list_bit_nums = bit_dict[0]

    position += 1

co2_bit_list = list_bit_nums[0]


o2_num = 0
co2_num = 0

for ind in range(12):
    o2_bit = o2_bit_list[ind]
    co2_bit = co2_bit_list[ind]

    o2_num += o2_bit * 2**(11 - ind)
    co2_num += co2_bit * 2**(11 - ind)
    
print(o2_num, co2_num)
