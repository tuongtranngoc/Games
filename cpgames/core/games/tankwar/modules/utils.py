import re
import pygame
from .sprites import *

from collections import defaultdict


def get_state(tank_player1: PlayerTank, 
                tank_player2: PlayerTank, 
                enemy_tank_group: pygame.sprite.Group,
                player1_bullets_group: pygame.sprite.Group, 
                player2_bullets_group: pygame.sprite.Group,
                enemy_bullets_group: pygame.sprite.Group,
                sences_group: dict,
                foods_group: pygame.sprite.Group):
    
    map_state = defaultdict()
    # Tank player 1
    tank_player1_state = {k: v for k, v in tank_player1.__dict__.items()}
    map_state['tank_player1_state'] = tank_player1_state
    # Tank player 2
    tank_player2_state = {k: v for k, v in tank_player2.__dict__.items()}
    map_state['tank_player2_state'] = tank_player2_state
    # Enemy tank group 
    enemy_tank_group_state = [{k: v for k, v in enemy_tank.__dict__.items()} for enemy_tank in enemy_tank_group.sprites()]
    map_state['enemy_tank_group_state'] = enemy_tank_group_state
    
    player1_bullets_group_state = [{k: v for k, v in player1_bullets.__dict__.items()} for player1_bullets in player1_bullets_group.sprites()]
    map_state['player1_bullets_group_state'] = player1_bullets_group_state

    player2_bullets_group_state = [{k: v for k, v in player2_bullets.__dict__.items()} for player2_bullets in player2_bullets_group.sprites()]
    map_state['player2_bullets_group_state'] = player2_bullets_group_state
    
    enemy_bullets_group_state = [{k: v for k, v in enemy_bullets.__dict__.items()} for enemy_bullets in enemy_bullets_group.sprites()]
    map_state['enemy_bullets_group_state'] = enemy_bullets_group_state

    sences_group_state = dict()
    for group in sences_group:
        sences_group_state[group] = [{k: v for k, v in seneces.__dict__.items()} for seneces in sences_group[group].sprites()]
    map_state['sences_group_state'] = sences_group_state

    foods_group_state = [{k: v for k, v in foods.__dict__.items()} for foods in foods_group.sprites()]
    map_state['foods_group_state'] = foods_group_state

    map_state = process_state(map_state)
    return map_state

def process_state(state: dict):
    def reformat(g):
        if '_Sprite__g' in g:
            _id = g.pop('_Sprite__g')
            _id = re.sub('[{<()>}]', '', str(_id))
            _id = re.sub('\s+', '_', _id)
            return _id
        return None
            
    
    for tank in ['tank_player1_state', 'tank_player2_state']:
        if tank in state:
            _id = reformat(state[tank])
            state[tank]['group_id'] = _id
            for k in ['player_tank_images', 
                    'bullet_images',
                    'protected_mask',
                    'boom_image',
                    'tank_image',
                    'tank_direction_image',
                    'image']:
                state[tank].pop(k)
            state[tank]['init_position'] = list(state[tank]['init_position'])
            state[tank]['direction'] = str(state[tank]['direction'])
            state[tank]['rect'] = list(state[tank]['rect'])

    if 'enemy_tank_group_state' in state:
        for i, __ in enumerate(state['enemy_tank_group_state']):
            _id = reformat(state['enemy_tank_group_state'][i])
            state['enemy_tank_group_state'][i]['group_id'] = _id
            if state['enemy_tank_group_state'][i]['food']:
                food = {k:v for k, v in state['enemy_tank_group_state'][i]['food'].__dict__.items()}
                for k in ['image', '_Sprite__g']:
                    food.pop(k)
                state['enemy_tank_group_state'][i].pop('food')
                state['enemy_tank_group_state'][i]['food'] = food
                state['enemy_tank_group_state'][i]['food']['rect'] = list(state['enemy_tank_group_state'][i]['food']['rect'])
                
            for k in ['bullet_images',
                        'appear_images',
                        'enemy_tank_images',
                        'tank_image',
                        'tank_direction_image',
                        'image',
                        'boom_image']:
                state['enemy_tank_group_state'][i].pop(k)
            state['enemy_tank_group_state'][i]['rect'] = list(state['enemy_tank_group_state'][i]['rect'])
                
    for tank in ['player1_bullets_group_state', 'player2_bullets_group_state']:
        if tank in state:
            for i, __ in enumerate(state[tank]):
                _id = reformat(state[tank][i])
                state[tank][i]['group_id'] = _id
                for k in ['bullet_images','image']:
                    state[tank][i].pop(k)
                state[tank][i]['position'] = list(state[tank][i]['position'])
                state[tank][i]['direction'] = str(state[tank][i]['direction'])
                state[tank][i]['rect'] = list(state[tank][i]['rect'])
    
    if 'enemy_bullets_group_state' in state:
        for i, __ in enumerate(state['enemy_bullets_group_state']):
            _id = reformat(state['enemy_bullets_group_state'][i])
            state['enemy_bullets_group_state'][i]['group_id'] = _id
            for k in ['bullet_images','image']:
                    state['enemy_bullets_group_state'][i].pop(k)
            state['enemy_bullets_group_state'][i]['rect'] = list(state['enemy_bullets_group_state'][i]['rect'])
            state['enemy_bullets_group_state'][i]['position'] = list(state['enemy_bullets_group_state'][i]['position'])
            state['enemy_bullets_group_state'][i]['direction'] = str(state['enemy_bullets_group_state'][i]['direction'])
    
    if 'sences_group_state' in state:
        for k in state['sences_group_state']:
            for i, __ in enumerate(state['sences_group_state'][k]):
                _id = reformat(state['sences_group_state'][k][i])
                state['sences_group_state'][k][i]['group_id'] = _id
                state['sences_group_state'][k][i].pop('image')
                state['sences_group_state'][k][i]['rect'] = list(state['sences_group_state'][k][i]['rect'])
    
    if 'foods_group_state' in state:
        for i, __ in enumerate(state['foods_group_state']):
            _id = reformat(state['foods_group_state'][i])
            state['foods_group_state'][i]['group_id'] = _id
            state['foods_group_state'][i].pop('image')
            state['foods_group_state'][i]['rect'] = list(state['foods_group_state'][i]['rect'])
    return state
