'''
Given the size of Tank Map is 630x630, The 
'''


class TankState:
    def __init__(self):
        pass

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
        return {'move': None, 'shoot': False}