import numpy as np

def choose_alternate_direction(current_direction):
    directions = ['up', 'down', 'left', 'right']
    directions.remove(current_direction)
    return np.random.choice(directions)


def get_next_action(player_state, enemy_tanks, foods, bullets, sences, pre_state):
    player_rect = player_state['rect']
    player_direction = player_state['direction']
    if pre_state:
        pre_position = pre_state['rect']
        pre_direction = pre_state['direction']
        if player_rect[:2] == pre_position[:2]:
            alternate_direction = choose_alternate_direction(player_state['direction'])
            return {'move': alternate_direction, 'shoot': True}
    return {'move': player_direction, 'shoot': True}