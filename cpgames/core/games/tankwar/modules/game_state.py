import re
import pygame
import numpy as np
from .sprites import *

from collections import defaultdict


class TankWarState:
    def __init__(self):
        pass
    def get_state(self, tank_player1: PlayerTank, 
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

        map_state = self.process_state(map_state)
        return map_state
    
    def process_state(self, state: dict):
        def reformat(g):
            if '_Sprite__g' in g:
                _id = g.pop('_Sprite__g')
                _id = re.sub('[{<()>}]', '', str(_id))
                _id = re.sub('\s+', '_', _id)
            return _id
        
        for tank in ['tank_player1_state', 'tank_player2_state']:
            if tank in state:
                _id = reformat(state[tank])
                state[tank]['_id'] = _id
                for k in ['player_tank_images', 
                        'bullet_images',
                        'protected_mask',
                        'boom_image',
                        'tank_image',
                        'tank_direction_image',
                        'image']:
                    state[tank].pop(k)
                state[tank]['init_position'] = list(state[tank]['init_position'])
                state[tank]['rect'] = list(state[tank]['rect'])

        if 'enemy_tank_group_state' in state:
            for i, __ in enumerate(state['enemy_tank_group_state']):
                _id = reformat(state['enemy_tank_group_state'][i])
                state['enemy_tank_group_state'][i]['_id'] = _id
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
                    state[tank][i]['_id'] = _id
                    for k in ['bullet_images','image']:
                        state[tank][i].pop(k)
                    state[tank][i]['position'] = list(state[tank][i]['position'])
                    state[tank][i]['rect'] = list(state[tank][i]['rect'])

        if 'enemy_bullets_group_state' in state:
            for i, __ in enumerate(state['enemy_bullets_group_state']):
                _id = reformat(state['enemy_bullets_group_state'][i])
                state['enemy_bullets_group_state'][i]['_id'] = _id
                for k in ['bullet_images','image']:
                        state['enemy_bullets_group_state'][i].pop(k)
                state['enemy_bullets_group_state'][i]['rect'] = list(state['enemy_bullets_group_state'][i]['rect'])
                state['enemy_bullets_group_state'][i]['position'] = list(state['enemy_bullets_group_state'][i]['position'])
        
        if 'sences_group_state' in state:
            for k in state['sences_group_state']:
                for i, __ in enumerate(state['sences_group_state'][k]):
                    _id = reformat(state['sences_group_state'][k][i])
                    state['sences_group_state'][k][i]['_id'] = _id
                    state['sences_group_state'][k][i].pop('image')
                    state['sences_group_state'][k][i]['rect'] = list(state['sences_group_state'][k][i]['rect'])
        
        if 'foods_group_state' in state:
            for i, __ in enumerate(state['foods_group_state']):
                    _id = reformat(state['foods_group_state'][i])
                    state['foods_group_state'][i]['_id'] = _id
                    state['foods_group_state'][i].pop('image')
                    state['foods_group_state'][i]['rect'] = list(state['foods_group_state'][i]['rect'])
        return state

    def decide(self, game_state):
        """Game Statement:
            scenes:
                - name: brick
                    rect: the position list of brick in MAP, default: [x, y, w, h] = [x, y, 24, 24]
                - name: iron
                    rect: the position list of iron in MAP, default: [x, y, w, h] = [x, y, 24, 24]
                - name: ice
                    rect: the position list of ice in MAP, default: [x, y, w, h] = [x, y, 24, 24]
                - name: river
                    rect: the position list of river in MAP, default: [x, y, w, h] = [x, y, 24, 24]
                - name: tree
                    rect: the position list of tree in MAP, default: [x, y, w, h] = [x, y, 24, 24]
            tank:
                name: player name
                border_len: the edge width of MAP, default: 3
                screensize: screen size, default: [630, 630]
                init_direction: init direction of tank, default: up
                init_position: init position of tank, default: player_1: [3, 579], player_2: [579, 579]
                protectd_mask_flash_time: 25
                protected_mask_count: 0
                protected_mask_pointer: False
                boom_last_time: 5
                booming_flash: False
                boom_count: 0
                points: 0,
                is_keep_still: False
                keep_still_time: 250
                direction: up
                is_protected: False
                protected_time: 1500
                speed: 8
                bullet_cooling_time: 30
                is_bullet_cooling: False
                tankLevel: 0
                rect: [x, y, w, h] = [x, y, 48, 48]
            bullet:
                direction:
                position:
                speed: 8
                is_stronger: default: False
                border_len:
            foods:
                - name: tank
                    exist_time: default: 1000
                    rect: [x, y, w, h] = [x, y, 32, 32]
                - name: clock
                    exist_time: default 1000
                    rect: [x, y, w, h] = [x, y, 32, 32]
                - name: boom
                    exist_time: default: 1000
                    rect: [x, y, w, h] = [x, y, 32, 32]
                - name: gun
                    exist_time: default: 1000
                    rect: [x, y, w, h] = [x, y, 32, 32]
                - name: star
                    exist_time: default: 1000
                    rect: [x, y, w, h] = [x, y, 32, 32]
                - name: protect
                    exist_time: default: 1000
                    rect: [x, y, w, h] = [x, y, 32, 32]
            enemy_tanks:
                border_len: 3
                screensize: [630, 630]
                tank_type: 
                tankLevel: 
                food: None
                direction: rect: [x, y, 48, 48]
                boom_last_time: 5
                boom_count: 0
                booming_flag: False
                bullet_cooling_time: 110
                bullet_cooling_count: 0
                is_bullet_cooling: False
                is_borning: True
                borning_left_time: 90
                is_keep_still: False
                keep_still_time: 500
                keep_still_count:
                speed: random
        """
        return {'move': 'up', 'shoot': True}