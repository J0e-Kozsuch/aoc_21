import datetime as dt


file = open(r'C:\Users\16099\Documents\AOC_21\aoc16_bits.txt')
by = file.read()

text_lines = by.split("\n")


bit_string = ''

for value in text_lines[0]:
    # format changes integer to string with binary number
    binary = format(int(value,16), 'b')
    while len(binary) < 4:
        binary = '0' + binary
    bit_string = bit_string + binary


packet_list = []

class Packet:

    def __init__(self, packet_string, parent):
        global packet_list

        self.parent = parent
        self.children = []
        packet_list.append(self)
        self.full_packet_string = packet_string                  
        self.version = 0
        self.type = 0
        self.value = None
        self.length_type = None
        self.remaining_string = None

    def decode_packet(self):

        self.version = int(self.full_packet_string[:3], 2)
        self.type = int(self.full_packet_string[3:6], 2)

        if self.type == 4:
            self._decode_literal(self.full_packet_string[6:])
            
        elif self.full_packet_string[6] == '0':
            self.length_type = '0'
            self._decode_type_0(self.full_packet_string[7:])

        else: # length type is 1
            self.length_type = '1'
            self._decode_type_1(self.full_packet_string[7:])
    
        
    def _decode_literal(self, integer_string): 

        final_binary_string = ''

        while integer_string[0] != '0':
            final_binary_string += integer_string[1:5]
            integer_string = integer_string[5:]

        final_binary_string += integer_string[1:5]

        self.remaining_string = integer_string[5:]

        self.value = int(final_binary_string, 2)

    def _decode_type_0(self, subpocket_string):
        length_of_subpackets = int(subpocket_string[:15],2)

        self.remaining_string = subpocket_string[15 + length_of_subpackets:]

        subpocket_string = subpocket_string[15:15 + length_of_subpackets]

        while len(subpocket_string) > 0:

            new_packet = Packet(subpocket_string, parent = self)
            new_packet.decode_packet()
            self.children.append(new_packet)

            subpocket_string = new_packet.remaining_string

        self._calculate_value()
  

    def _decode_type_1(self, subpocket_string):
        num_subpackets = int(subpocket_string[:11],2)

        subpocket_string = subpocket_string[11:]

        while num_subpackets > 0:

            new_packet = Packet(subpocket_string, parent = self)
            new_packet.decode_packet()
            self.children.append(new_packet)

            subpocket_string = new_packet.remaining_string

            num_subpackets -= 1

        self.remaining_string = subpocket_string

        self._calculate_value()

        

    def _calculate_value(self):
        child_values = [child.value for child in self.children]
        
        if self.type == 0:
            sum_value = 0
            for child_value in child_values:
                sum_value += child_value
            self.value = sum_value

        elif self.type == 1:
            prod_value = 1
            for child_value in child_values:
                prod_value *= child_value
            self.value = prod_value

        elif self.type == 2:
            self.value = min(child_values)

        elif self.type == 3:
            self.value = max(child_values)

        elif self.type == 5:
            if child_values[0] > child_values[1]:
                self.value = 1
            else:
                self.value = 0

        elif self.type == 6:
            if child_values[0] < child_values[1]:
                self.value = 1
            else:
                self.value = 0

        elif self.type == 7:
            if child_values[0] == child_values[1]:
                self.value = 1
            else:
                self.value = 0
            
            

        



    
p = Packet(bit_string, None)
p.decode_packet()

print(p.value)

            


        
        
        
        



