
file = open(r'C:\Users\16099\Documents\AOC_21\aoc7_crab_position.txt')
by = file.read()

text_lines = by.split("\n")

crab_list = [int(i) for i in text_lines[0].split(',')]

# find average
list_sum = 0
for pos in crab_list:
    list_sum += pos
average = int(list_sum / len(crab_list))

# move ticker in descending direction until min found

def fuel_consumption(pos):
    fuel_usage = 0
    for crab_pos in crab_list:
        fuel_usage += abs(crab_pos - pos)
    return fuel_usage

ticker_pos = average
ticker_fuel = fuel_consumption(ticker_pos)

while True:
    print(ticker_pos)
    left_pos = ticker_pos - 1
    right_pos = ticker_pos + 1

    left_fuel = fuel_consumption(left_pos)
    right_fuel = fuel_consumption(right_pos)
    

    if left_fuel < ticker_fuel:
        ticker_pos = left_pos
        ticker_fuel = left_fuel

    elif right_fuel < ticker_fuel:
        ticker_pos = right_pos
        ticker_fuel = right_fuel

    else:
        break

    
