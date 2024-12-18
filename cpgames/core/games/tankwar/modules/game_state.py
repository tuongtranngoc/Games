from ....games.tankwar.unittest.test_1 import get_next_action


class TankWarState:

    def player1_action(self, pre_state, game_state):
        
        player_state = game_state['tank_player1_state']
        enemy_tanks_state = game_state['enemy_tank_group_state']
        foods = game_state['foods_group_state']
        enemy_bullets = game_state['foods_group_state']
        sences = game_state['sences_group_state']
        pre_state = pre_state.get('tank_player1_state', {})
        
        action = get_next_action(player_state, enemy_tanks_state, foods, enemy_bullets, sences, pre_state)
        return {
            'move': action.get('move', 'up'),
            'shoot': action.get('move', False),
        }
    
    def player2_action(self, pre_state, game_state):
        player_state = game_state['tank_player2_state']
        enemy_tanks_state = game_state['enemy_tank_group_state']
        foods = game_state['foods_group_state']
        enemy_bullets = game_state['foods_group_state']
        sences = game_state['sences_group_state']
        pre_state = pre_state.get('tank_player2_state', {})
        
        action = get_next_action(player_state, enemy_tanks_state, foods, enemy_bullets, sences, pre_state)
        
        return {
            'move': action.get('move', 'up'),
            'shoot': action.get('move', False),
        }