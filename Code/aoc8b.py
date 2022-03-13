
file = open(r'C:\Users\16099\Documents\AOC_21\aoc8_number_output.txt')
by = file.read()

text_lines = by.split("\n")

code_list = []

for line in text_lines:
    seven_segment_codes, outputs = line.split('|')
    code_list.append(
                    (seven_segment_codes.strip().split(" "),
                       outputs.strip().split(" "))
                      )
    

# count the number of 1, 4, 7, 8

num_dict = {
            'abcefg': '0', 'cf': '1', 'acdeg': '2',
            'acdfg': '3', 'bcdf': '4', 'abdfg': '5',
            'abdefg': '6', 'acf': '7', 'abcdefg': '8',
            'abcdfg': '9'
            }

alpha_list = 'a b c d e f g'.split(' ')

alpha_conv_dict = {}

sum_of_decipher_nums = 0


for segment_strings, four_outputs in code_list:
    
    alpha_conv_dict = {}

    strings_lengths = [len(string) for string in segment_strings]

    # determine 1, 4, 7 and three 6-segement codes, 0, 6 and 9
    init_one = segment_strings[ strings_lengths.index(2)]
    init_four = segment_strings[ strings_lengths.index(4)]
    init_seven = segment_strings[ strings_lengths.index(3)]
    
    init_069 = [segment_strings[index] for index, length in enumerate(strings_lengths) if length == 6]
    
    # determine 6, then use 1 and 6 to determine c and f
    one_letter1, one_letter2 = init_one
    
    for index, string in enumerate(init_069):

        if one_letter1 in string and one_letter2 in string:
            continue

        break
    
    init_six = string
    init_069.pop(index)
    init_09 = init_069[:]

    if one_letter1 not in init_six:
        alpha_conv_dict[one_letter1] = 'c'
        alpha_conv_dict[one_letter2] = 'f'
    else:
        alpha_conv_dict[one_letter1] = 'f'
        alpha_conv_dict[one_letter2] = 'c'
    
    # use 1 and 7 to determine a
    for letter in init_seven:
        if letter not in init_one:
           alpha_conv_dict[letter] = 'a'
           break

    # determine 9, then use 4 and 9 to determine d.
    found = False
    
    for letter_index, letter_four in enumerate(init_four):
        for string_index, string in enumerate(init_09):
            if letter_four not in string:
                found = True
                break
        if found:
            break
        
    init_nine = init_09[1-string_index]
    alpha_conv_dict[letter_four] = 'd'
                 
    # use 9 to determine e
    for letter in alpha_list:
        if letter not in init_nine:
           alpha_conv_dict[letter] = 'e'

    # use 4 to determine b
    for letter in init_four:
        if letter not in alpha_conv_dict.keys():
            alpha_conv_dict[letter] = 'b'

    # final letter is g
    for letter in alpha_list:
        if letter not in alpha_conv_dict.keys():
            alpha_conv_dict[letter] = 'g'

    # transform segments to correct codes

    
    decipher_dict = {} # transforms inputted strings to string of correct number

    for string in segment_strings:
        
        letter_list = list(string)
        letter_list.sort()
        og_sorted_code = ''
        
        for letter in letter_list:
            og_sorted_code += letter
        
        deciphered_string = ''
        for letter in og_sorted_code:
            deciphered_string += alpha_conv_dict[letter]

        letter_list = list(deciphered_string)
        letter_list.sort()
        dec_sorted_code = ''
        for letter in letter_list:
            dec_sorted_code += letter

        decipher_dict[og_sorted_code] = num_dict[dec_sorted_code]

    # decipher outputs
    string_of_output = ''
    for num_string in four_outputs:
        string_list = list(num_string)
        string_list.sort()
        new_code = ''
        for letter in string_list:
            new_code += letter
        string_of_output += decipher_dict[new_code]

    sum_of_decipher_nums += int(string_of_output)

print(num_dict)
