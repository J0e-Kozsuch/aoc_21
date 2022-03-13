

class Game():

    def __init__(self, player_1_pos, player_2_pos):
        self._positions = [player_1_pos, player_2_pos]

        # 0 for player 1 and 1 for player 2
        self._turn = 0

        self._scores = [0,0]

        self._next_dice_roll = 1

        self._number_rolls = 0


    def _play_turn(self):
        
        moves = 0
        
        for _ in range(3):
            moves += self._next_dice_roll
            self._next_dice_roll += 1
            if self._next_dice_roll > 100:
                self._next_dice_roll = 1

        landing_position_sum = self._positions[ self._turn ] + moves

        landing_position = landing_position_sum % 10

        if landing_position == 0:
            landing_position = 10

        self._positions[ self._turn ] = landing_position

        self._scores[ self._turn ] += landing_position

        self._number_rolls += 3

        self._turn = (self._turn + 1) % 2
        

    def play_game(self):

        while max(self._scores) < 1000:
            self._play_turn()

        print(f"Scores are {self._scores} after {self._number_rolls}")

g = Game(4, 10)

g.play_game()

    
        

        
        


