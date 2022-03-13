
file = open(r'C:\Users\16099\Documents\AOC_21\aoc4_bingo.txt')
by = file.read()

lines = by.split("\n")

# I will be keeping nums as strings
bingo_nums = lines[0].split(",")

class Board:
    def __init__(self, board_lines):
        '''
        create object board variable
        '''
        self.board_array = []

        for line in board_lines:
            new_line = line.split(" ")
            new_line = [value for value in new_line if value!='']
            self.board_array.append(new_line)
        
    def __str__(self):
        return str(self.board_array)
        
    def calculate_score(self, called_num):
        remaining_sum = 0

        for row in self.board_array:
            for num in row:
                if num != '*':
                    remaining_sum += int(num)

        return remaining_sum * int(called_num)

    def check_win(self):
        transposed_board = [[],[],[],[],[]]

        for row_ind, row in enumerate(self.board_array):
            if row == ['*','*','*','*','*']:
                return True
            for col_ind, num in enumerate(row):
                transposed_board[col_ind].append(num)

        for row in transposed_board:
            if row == ['*','*','*','*','*']:
                return True

        return False

    

    def find_called_num(self, called_num):
        for ind_row, row in enumerate(self.board_array):
            for ind_col, value in enumerate(row):
                if value == called_num:
                    return (ind_row, ind_col)

        return None
                

    def play_turn(self, called_num):

        indices = self.find_called_num(called_num)
        if indices:
            ind_row, ind_col = indices
            self.board_array[ind_row][ind_col] = '*'

        won = self.check_win()

        if won:
            return self.calculate_score(called_num)

        return None
            
        
        



bingo_boards = []

for ind in range(100):
    board_lines = lines[2 + 6*ind: 7 + 6*ind]
    bingo_boards.append(Board(board_lines))


last_round = False
winning_scores = []

for num in bingo_nums:
    

    for board in bingo_boards:
        
        winning_score = board.play_turn(num)
        
        if winning_score:
            winning_scores.append(winning_score)
            print(str(board), "\n", winning_score)
            last_round = True
        
        
    if last_round:
        break
    
print(winning_scores)
