
cache = {}
    
        
def play_turn_until_end(player_positions, player_scores = (0,0), rolls_into_turn = 0, turn_sum = 0, player_turn = 0):
    global cache
    
    universe_dict = {'1': 0, '2': 0}

    try:
        return cache[(player_positions,player_scores,player_turn)]
    except:
        pass

    if max(player_scores) >= 21:
        player_turn = int( (player_turn + 1) % 2 ) 
        universe_dict[ str(player_turn + 1) ] = 1
        cache[(player_positions,player_scores,player_turn)] = universe_dict
        return universe_dict

    elif rolls_into_turn < 3:
        for i in range(1,4):
            new_turn_sum = turn_sum + i
            new_rolls_into_turn = rolls_into_turn + 1
            new_universe_dict = play_turn_until_end(player_positions = player_positions, player_scores = player_scores, \
                                                    rolls_into_turn = new_rolls_into_turn, turn_sum = new_turn_sum, player_turn = player_turn)

            universe_dict['1'] += new_universe_dict['1']
            universe_dict['2'] += new_universe_dict['2']

        return universe_dict

    else:
        starting_score = player_scores[:] 
        
        landing_position_sum = player_positions[ player_turn ] + turn_sum

        landing_position = int(landing_position_sum % 10)

        if landing_position == 0:
            landing_position = 10

        if player_turn == 1:
            new_player_positions = (player_positions[0],landing_position)
            new_player_scores = (player_scores[0],player_scores[1] + landing_position)
        else:
            new_player_positions = (landing_position,player_positions[1])
            new_player_scores = (player_scores[0] + landing_position,player_scores[1])

        rolls_into_turn = 0
        
        turn_sum = 0
        
        player_turn = int((player_turn + 1) % 2)

        universe_dict = play_turn_until_end(player_positions = new_player_positions, player_scores = new_player_scores, \
                                                rolls_into_turn = rolls_into_turn, turn_sum = turn_sum, player_turn = player_turn)

        cache[(new_player_positions,new_player_scores,player_turn)] = universe_dict

        return universe_dict
        
a = play_turn_until_end(player_positions = (4,10))

print(a)

