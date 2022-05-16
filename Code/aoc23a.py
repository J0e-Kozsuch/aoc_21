BOARD = [
    list("#############"),
    list("#...........#"),
    list("###B#A#C#D###"),
    list("###A#B#C#D###"),
    list("#############"),
]

ROOM_HEIGHT = len(BOARD) - 3

# delete?
# letter_col_dict = {'A':3,'B':5,'C':7,'D':9}
COL_LETTER_DICT = {3: "A", 5: "B", 7: "C", 9: "D"}

ENERGY_COST = {"A": 1, "B": 10, "C": 100, "D": 1000}


class Board:
    def __init__(self, board=BOARD):
        self.grid = BOARD

    def check_room_availability(self, col: int, letter: str):
        """
        given room col and letter to enter, determines T/F and lowest row if T
        """

        room_required_letter = COL_LETTER_DICT[col]

        # first check to see if right room for the letter
        if letter != room_required_letter:
            return False

        first_spot_open = False

        # check if only right letters are in room and first spot to land
        for row in range(2, 2 + ROOM_HEIGHT):
            if self.grid[row][col] == ".":
                first_spot_open = row
            elif self.grid[row][col] != room_required_letter:
                return False

        return first_spot_open

    def check_victory(self):

        for col in (3, 5, 7, 9):
            letter = COL_LETTER_DICT[col]
            for row in range(2, 2 + ROOM_HEIGHT):
                if self.grid[row][col] != letter:
                    return False

        for col in range(1,12):
            if self.grid[1][col] != '.':
                return False
        return True

    def find_letters_to_move(self) -> list:
        """
        scan hallway and tops of rooms for letters
        returns list of (letter, coordinate) pairs
        """

        letters_to_move = []

        ## hallway
        for col in range(1, 12):
            char = self.grid[1][col]
            if char != ".":
                letters_to_move.append((char, (1, col)))

        ## rooms
        for col in (3, 5, 7, 9):

            room_required_letter = COL_LETTER_DICT[col]

            room_is_enter_only = (
                sum(
                    [
                        iter_row[col] not in [room_required_letter, "."]
                        for iter_row in self.grid[2 : 2 + ROOM_HEIGHT]
                    ]
                )
                == 0
            )

            if room_is_enter_only:
                continue

            for row in range(2, 2 + ROOM_HEIGHT):
                if self.grid[row][col] == ".":
                    continue

                else:
                    letters_to_move.append((self.grid[row][col], (row, col)))
                    break

        return letters_to_move

    def find_spaces_to_move_from_hallway(self, letter: str, starting_col: int) -> list:
        """
        find letters with an adjacent dot and then a clear path to movable space
        will pass to check_room_availability() if dot is open in front of room
        returns list of landing spots in hallway and in rooms
        """

        moves = []

        # move forward in hallway
        col_move_ind = starting_col + 1

        while self.grid[1][col_move_ind] not in ["A", "B", "C", "D", "#"]:
            if col_move_ind in [1, 2, 4, 6, 8, 10, 11]:
                moves.append((1, col_move_ind))
            else:
                room_spot_opening = self.check_room_availability(col_move_ind, letter)
                if room_spot_opening:
                    moves.append((room_spot_opening, col_move_ind))
            col_move_ind = col_move_ind + 1

        # move backwards in hallway
        col_move_ind = starting_col - 1

        while self.grid[1][col_move_ind] not in ["A", "B", "C", "D", "#"]:
            if col_move_ind in [1, 2, 4, 6, 8, 10, 11]:
                moves.append((1, col_move_ind))
            else:
                room_spot_opening = self.check_room_availability(col_move_ind, letter)
                if room_spot_opening:
                    moves.append((room_spot_opening, col_move_ind))
            col_move_ind = col_move_ind - 1

        return moves

    def make_move(self, starting_spot: tuple, ending_spot: tuple):
        """
        ingests starting and finishing of letter to move
        changes board self.grid, returns nothing
        """
        self.grid[ending_spot[0]][ending_spot[1]] = self.grid[starting_spot[0]][
            starting_spot[1]
        ][:]

        self.grid[starting_spot[0]][starting_spot[1]] = "."

    def find_moves(self) -> dict:
        """
        find all possible moves, return list of starting and ending coordinates
        """
        starting = self.find_letters_to_move()

        possible_moves = {}

        for starting_letter, starting_spot in starting:

            # requires energy to get from room to hallway
            spots_moved_to_hallway = starting_spot[0] - 1

            next_moves = self.find_spaces_to_move_from_hallway(
                starting_letter, starting_spot[1]
            )

            # if letter starts in hallway, can't move to hallway
            if starting_spot[0] == 1:
                next_moves = [
                    landing_spot for landing_spot in next_moves if landing_spot[0] != 1
                ]

            # calculate energy
            for landing_spot in next_moves:

                spots_moved_horizontally = abs(landing_spot[1] - starting_spot[1])
                spots_moved_vertically = abs(landing_spot[0] - 1)

                spots_moved = spots_moved_to_hallway + spots_moved_vertically + spots_moved_horizontally

                energy_spent = spots_moved * ENERGY_COST[starting_letter]

                possible_moves[(starting_spot, landing_spot)] = energy_spent

        return possible_moves

    def print_board(self):
        for row in self.grid:
            print(row)

    def return_copied_grid(self):
        new_board_grid = []
        for row in self.grid:
            new_board_grid.append(row[:])
        return new_board_grid


def recursive_func(energy: int, board_states: list) -> tuple:

    starting_board = Board(board_states[-1])

    moves = starting_board.find_moves()

    if moves == dict():
        if starting_board.check_victory():
            return (energy, board_states)

        return (99999, board_states)

    next_moves = {}

    for (starting_spot, landing_spot), energy_spent in moves.items():

        board = Board(starting_board.return_copied_grid())

        board.make_move(starting_spot, landing_spot)

        move_energy = energy + energy_spent
        move_board_states = board_states[:] + [board.return_copied_grid()[:]]

        e1, bss1 = recursive_func(move_energy, move_board_states)

        next_moves[e1] = bss1

    lowest_energy = min(next_moves.keys())

    final_board_states = next_moves[lowest_energy]

    return (lowest_energy,final_board_states)

a = recursive_func(0, [BOARD])

print(a[0])
for board in a[1]:
    board

