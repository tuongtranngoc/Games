class TankState:
    def __init__(self):
        pass

    def decide(self, game_state):
        """Game Statement:
            scenes:
                brick: 
                iron: 
                ice:  
                river: 
                tree:
            tank:
                player_name:
                position:
                direction:
                protected_mask:
                tankLevel:
            bullet:
                
            foods:

            enemy_tanks: 
        """
        return {'move': None, 'shoot': False}