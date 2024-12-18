'''
Function:
    用于运行某一游戏关卡
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import pygame
import random
from .sprites import *
from ....utils import QuitGame
from ....games.tankwar.modules.utils import get_state
from ....games.tankwar.modules.game_state import TankWarState
# from ....games.tankwar.modules.dochallenges.db_status import DBStatus


class GameLevel():
    def __init__(self, gamelevel, levelfilepath, is_dual_mode, cfg, resource_loader, **kwargs):
        self.cfg = cfg
        # 关卡地图路径
        self.gamelevel = gamelevel
        self.levelfilepath = levelfilepath
        # 资源加载器
        self.resource_loader = resource_loader
        self.sounds = self.resource_loader.sounds
        # 是否为双人模式
        self.is_dual_mode = is_dual_mode
        # 地图规模参数
        self.border_len = cfg.BORDER_LEN
        self.grid_size = cfg.GRID_SIZE
        self.width, self.height = cfg.SCREENSIZE
        self.panel_width = cfg.PANEL_WIDTH
        # 字体
        self.font = resource_loader.fonts['gaming']
        # Quit Game Timer
        self.countdown_time = 120
        # 关卡场景元素
        self.scene_elems = {
            'brick_group': pygame.sprite.Group(),
            'iron_group': pygame.sprite.Group(),
            'ice_group': pygame.sprite.Group(), 
            'river_group': pygame.sprite.Group(),
            'tree_group': pygame.sprite.Group()
        }
        # 解析关卡文件
        self.__parseLevelFile()

        # self.status = DBStatus()
        self.tankwar_state = TankWarState()
        
    '''Game Start'''
    def start(self, screen):
        screen, resource_loader = pygame.display.set_mode((self.width+self.panel_width, self.height)), self.resource_loader
        # 背景图片
        background_img = resource_loader.images['others']['background']
        # 定义精灵组
        player1_tanks_group = pygame.sprite.Group()
        player2_tanks_group = pygame.sprite.Group()
        enemy_tanks_group = pygame.sprite.Group()
        player1_bullets_group = pygame.sprite.Group()
        player2_bullets_group = pygame.sprite.Group()
        enemy_bullets_group = pygame.sprite.Group()
        foods_group = pygame.sprite.Group()
        # 定义敌方坦克生成事件
        generate_enemies_event = pygame.constants.USEREVENT
        pygame.time.set_timer(generate_enemies_event, 20000)
        # 我方大本营
        home = Home(position=self.home_position, images=resource_loader.images['home'])
        # 我方坦克
        tank_player1 = PlayerTank(
            name='player1', position=self.player_tank_positions[0], player_tank_images=resource_loader.images['player'], 
            border_len=self.border_len, screensize=[self.width, self.height], bullet_images=resource_loader.images['bullet'], 
            protected_mask=resource_loader.images['others']['protect'], boom_image=resource_loader.images['others']['boom_static']
        )
        player1_tanks_group.add(tank_player1)
        if self.is_dual_mode:
            tank_player2 = PlayerTank(
                name='player2', position=self.player_tank_positions[1], player_tank_images=resource_loader.images['player'], 
                border_len=self.border_len, screensize=[self.width, self.height], bullet_images=resource_loader.images['bullet'], 
                protected_mask=resource_loader.images['others']['protect'], boom_image=resource_loader.images['others']['boom_static']
            )
            player2_tanks_group.add(tank_player2)

        for position in self.enemy_tank_positions:
            enemy_tanks_group.add(EnemyTank(
                enemy_tank_images=resource_loader.images['enemy'], appear_image=resource_loader.images['others']['appear'], position=position, 
                border_len=self.border_len, screensize=[self.width, self.height], bullet_images=resource_loader.images['bullet'], 
                food_images=resource_loader.images['food'], boom_image=resource_loader.images['others']['boom_static']
            ))
        # 游戏开始音乐
        self.sounds['start'].play()
        clock = pygame.time.Clock()
        start_ticks = pygame.time.get_ticks()
        # 该关卡通过与否的flags
        is_win = None
        is_running = True
        # 游戏主循环
        pre_state_1 = {}
        pre_state_2 = {}
        while is_running:
            screen.fill((0, 0, 0))
            screen.blit(background_img, (0, 0))
            # 用户事件捕捉
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                # --敌方坦克生成
                elif event.type == generate_enemies_event:
                    if self.max_enemy_num > len(enemy_tanks_group):
                        for position in self.enemy_tank_positions:
                            if len(enemy_tanks_group) == self.total_enemy_num:
                                break
                            enemy_tank = EnemyTank(
                                enemy_tank_images=resource_loader.images['enemy'], appear_image=resource_loader.images['others']['appear'], position=position, 
                                border_len=self.border_len, screensize=[self.width, self.height], bullet_images=resource_loader.images['bullet'], 
                                food_images=resource_loader.images['food'], boom_image=resource_loader.images['others']['boom_static']
                            )
                            if (not pygame.sprite.spritecollide(enemy_tank, enemy_tanks_group, False, None)) and (not pygame.sprite.spritecollide(enemy_tank, player1_tanks_group, False, None) or not pygame.sprite.spritecollide(enemy_tank, player2_tanks_group, False, None)):
                                enemy_tanks_group.add(enemy_tank)
            seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
            self.time_left = max(0, self.countdown_time - seconds_passed)
            tankwar_state = get_state(tank_player1,
                                        tank_player2,
                                        enemy_tanks_group,
                                        player1_bullets_group,
                                        player2_bullets_group,
                                        enemy_bullets_group,
                                        self.scene_elems,
                                        foods_group)
            # import ipdb; ipdb.set_trace();
            player1_action = self.tankwar_state.player1_action(pre_state_1, tankwar_state)
            player2_action = self.tankwar_state.player2_action(pre_state_2, tankwar_state)
            pre_state_1 = tankwar_state
            pre_state_2 = tankwar_state
            # Player actions
            # Player 1 uses WSAD to move, press Space to shoot
            if self.time_left >= 0:
                if player1_action['shoot']:
                    bullet = tank_player1.shoot()
                    if bullet:
                        self.sounds['fire'].play() if tank_player1.tanklevel < 2 else self.sounds['Gunfire'].play()
                        player1_bullets_group.add(bullet)
                if player1_action['move']:
                    player1_tanks_group.remove(tank_player1)
                    tank_player1.move(player1_action['move'], self.scene_elems, player1_tanks_group, enemy_tanks_group, home)
                    player1_tanks_group.add(tank_player1)
                        
            # Player 1 uses ↑↓←→ to move, press 0 to shoot
            if self.is_dual_mode and (self.time_left >= 0):
                if player2_action['shoot']:
                    bullet = tank_player2.shoot()
                    if bullet:
                        self.sounds['fire'].play() if tank_player2.tanklevel < 2 else self.sounds['Gunfire'].play()
                        player2_bullets_group.add(bullet)
                if player2_action['move']:
                    player2_tanks_group.remove(tank_player2)
                    tank_player2.move(player2_action['move'], self.scene_elems, player2_tanks_group, enemy_tanks_group, home)
                    player2_tanks_group.add(tank_player2)

            pygame.sprite.groupcollide(player1_bullets_group, self.scene_elems.get('brick_group'), True, True)
            pygame.sprite.groupcollide(player2_bullets_group, self.scene_elems.get('brick_group'), True, True)
            pygame.sprite.groupcollide(enemy_bullets_group, self.scene_elems.get('brick_group'), True, True)

            for bullet in player1_bullets_group:
                if pygame.sprite.spritecollide(bullet, self.scene_elems.get('iron_group'), bullet.is_stronger, None):
                    player1_bullets_group.remove(bullet)
            for bullet in player2_bullets_group:
                if pygame.sprite.spritecollide(bullet, self.scene_elems.get('iron_group'), bullet.is_stronger, None):
                    player2_bullets_group.remove(bullet)
            pygame.sprite.groupcollide(enemy_bullets_group, self.scene_elems.get('iron_group'), True, False)

            # Bullet colliding
            pygame.sprite.groupcollide(player1_bullets_group, enemy_bullets_group, True, True)
            pygame.sprite.groupcollide(player2_bullets_group, enemy_bullets_group, True, True)
            pygame.sprite.groupcollide(player1_bullets_group, player2_bullets_group, True, True)

            # Player kill enemy
            def __playerKillEnemy(enemy_tank, player_tank, point=1):
                if enemy_tank.food:
                    foods_group.add(tank.food)
                    tank.food = None
                if enemy_tank.decreaseTankLevel():
                    self.sounds['bang'].play()
                    self.total_enemy_num -= 1
                    player_tank.addPoint(point)
            # Player kill player
            def __playerKillPlayer(player1_tank, player2_tank):
                if player1_tank.is_protected:
                        self.sounds['blast'].play()
                else:
                    if player1_tank.decreaseTankLevel():
                        self.sounds['bang'].play()
                        if player2_tank is not None:
                            player2_tank.addPoint(1)

            # Player is killed by player
            for tank in enemy_tanks_group:
                if pygame.sprite.spritecollide(tank, player1_bullets_group, True, None):
                    __playerKillEnemy(tank, tank_player1)
                if pygame.sprite.spritecollide(tank, player2_bullets_group, True, None):
                    __playerKillEnemy(tank, tank_player2)
            
            # Player-1 is killed by enemy
            for tank in player1_tanks_group:
                if pygame.sprite.spritecollide(tank, enemy_bullets_group, True, None):
                    __playerKillPlayer(tank, None)
                if pygame.sprite.spritecollide(tank, player2_bullets_group, True, None):
                    __playerKillPlayer(tank, tank_player2)
                    
            # Player-2 is killed by enemy
            for tank in player2_tanks_group:
                if pygame.sprite.spritecollide(tank, enemy_bullets_group, True, None):
                    __playerKillPlayer(tank, None)
                if pygame.sprite.spritecollide(tank, player1_bullets_group, True, None):
                    __playerKillPlayer(tank, tank_player1)
                            
            if self.time_left <= 0:
                is_running = False
                
            if pygame.sprite.groupcollide(player1_tanks_group, self.scene_elems.get('tree_group'), False, False) or \
                pygame.sprite.groupcollide(player2_tanks_group, self.scene_elems.get('tree_group'), False, False):
                self.sounds['hit'].play()
            
            def __playerEeatFood(player_tank: PlayerTank, enemy_tank_group, other_ptank_group):
                for food in foods_group:
                    if pygame.sprite.collide_rect(player_tank, food):
                        if food.name == 'boom':
                            self.sounds['add'].play()
                            for _ in enemy_tank_group:
                                self.sounds['bang'].play()
                            self.total_enemy_num -= len(enemy_tank_group)
                            player_tank.addPoint(len(enemy_tank_group))
                            enemy_tank_group = pygame.sprite.Group()
                            for p_tank in other_ptank_group:
                                p_tank.decreaseTankLevel()
                        elif food.name == 'clock':
                            self.sounds['add'].play()
                            for p_tank in other_ptank_group:
                                p_tank.setStill()
                            for enemy_tank in enemy_tank_group:
                                enemy_tank.setStill()
                        elif food.name == 'gun':
                            self.sounds['add'].play()
                            player_tank.improveTankLevel()
                        elif food.name == 'protect':
                            self.sounds['add'].play()
                            player_tank.setProtected()
                        elif food.name == 'star':
                            self.sounds['add'].play()
                            player_tank.improveTankLevel()
                            player_tank.setProtected()
                        foods_group.remove(food)
                return enemy_tank_group, other_ptank_group
                        
            def __doChallenge(p_tank, player_level):
                tank_levels = self.status.query_status()
                if tank_levels[player_level] is True:
                    p_tank.improveTankLevel()
                    self.status.update_status(self.status.init_data)

            # --我方坦克吃到食物
            for player_tank in player1_tanks_group:
                enemy_tanks_group, player2_tanks_group = __playerEeatFood(player_tank, enemy_tanks_group, player2_tanks_group)
                # __doChallenge(player_tank, 'player1_level')
                        
            for player_tank in player2_tanks_group:
                enemy_tanks_group, player1_tanks_group = __playerEeatFood(player_tank, enemy_tanks_group, player1_tanks_group)
                # __doChallenge(player_tank, 'player2_level')

            # 画场景地图
            for key, value in self.scene_elems.items():
                if key in ['ice_group', 'river_group']:
                    value.draw(screen)
            # 更新并画我方子弹
            for bullet in player1_bullets_group:
                if bullet.move():
                    player1_bullets_group.remove(bullet)
            player1_bullets_group.draw(screen)
            for bullet in player2_bullets_group:
                if bullet.move():
                    player2_bullets_group.remove(bullet)
            player2_bullets_group.draw(screen)
            # 更新并画敌方子弹
            for bullet in enemy_bullets_group:
                if bullet.move():
                    enemy_bullets_group.remove(bullet)
            enemy_bullets_group.draw(screen)
            # 更新并画我方坦克
            for tank in player1_tanks_group:
                tank.update()
                tank.draw(screen)
            for tank in player2_tanks_group:
                tank.update()
                tank.draw(screen)
            # 更新并画敌方坦克
            for tank in enemy_tanks_group:
                enemy_tanks_group.remove(tank)
                tank.update(self.scene_elems, player1_tanks_group, enemy_tanks_group, home)
                data_return = tank.update(self.scene_elems, player2_tanks_group, enemy_tanks_group, home)
                enemy_tanks_group.add(tank)
                if data_return.get('bullet'):
                    enemy_bullets_group.add(data_return.get('bullet'))
                if data_return.get('boomed'):
                    enemy_tanks_group.remove(tank)
            enemy_tanks_group.draw(screen)
            
            # 画场景地图
            for key, value in self.scene_elems.items():
                if key not in ['ice_group', 'river_group']:
                    value.draw(screen)
            # 画大本营
            home.draw(screen)
            # 更新并显示食物
            for food in foods_group:
                if food.update():
                    foods_group.remove(food)
            foods_group.draw(screen)
            self.__showGamePanel(screen, tank_player1, tank_player2) if self.is_dual_mode else self.__showGamePanel(screen, tank_player1)

            if tank_player1.points > tank_player2.points:
                is_win = "Player 1"
            elif tank_player1.points < tank_player2.points:
                is_win = "Player 2"
            else:
                is_win = None
            
            pygame.display.flip()
            clock.tick(self.cfg.FPS)
        screen = pygame.display.set_mode((self.width, self.height))
        return is_win
    
    '''显示游戏面板'''
    def __showGamePanel(self, screen, tank_player1, tank_player2=None):
        color_white = (255, 255, 255)
        top_idx = 1
        
        # Time Counting
        time_count_tip = self.font.render('Time: %s' % self.time_left, True, color_white)
        time_count_rect = time_count_tip.get_rect()
        time_count_rect.left, time_count_rect.top = self.width+5, self.height/30
        screen.blit(time_count_tip, time_count_rect)

        top_idx += 1
        line_tip = self.font.render("*" * 20, True, color_white)
        line_tip_rect = line_tip.get_rect()
        line_tip_rect.left, line_tip_rect.top = self.width+5, self.height*top_idx/30
        screen.blit(line_tip, line_tip_rect)
        
        # Status of player 1
        top_idx += 1
        player1_state_tip = self.font.render('State-P1:', True, color_white)
        player1_state_tip_rect = player1_state_tip.get_rect()
        player1_state_tip_rect.left, player1_state_tip_rect.top = self.width+5, self.height*top_idx/30
        screen.blit(player1_state_tip, player1_state_tip_rect)

        top_idx += 1
        player1_point_tip = self.font.render('Point: %s' % tank_player1.points, True, color_white)
        player1_point_tip_rect = player1_point_tip.get_rect()
        player1_point_tip_rect.left, player1_point_tip_rect.top = self.width+5, self.height*top_idx/30
        screen.blit(player1_point_tip, player1_point_tip_rect)
        
        top_idx += 1
        player1_state_tip = self.font.render('Tank-Level: %s' % max(0, tank_player1.tanklevel), True, color_white)
        player1_state_tip_rect = player1_state_tip.get_rect()
        player1_state_tip_rect.left, player1_state_tip_rect.top = self.width+5, self.height*top_idx/30
        screen.blit(player1_state_tip, player1_state_tip_rect)

        top_idx += 1
        line_tip = self.font.render("*" * 20, True, color_white)
        line_tip_rect = line_tip.get_rect()
        line_tip_rect.left, line_tip_rect.top = self.width+5, self.height*top_idx/30
        screen.blit(line_tip, line_tip_rect)

        # 玩家二状态提示
        top_idx += 1
        player2_state_tip = self.font.render('State-P2:', True, color_white)
        player2_state_tip_rect = player2_state_tip.get_rect()
        player2_state_tip_rect.left, player2_state_tip_rect.top = self.width+5, self.height*top_idx/30
        screen.blit(player2_state_tip, player2_state_tip_rect)
        
        top_idx += 1
        player2_point_tip = self.font.render('Point: %s' % tank_player2.points, True, color_white)
        player2_point_tip_rect = player2_point_tip.get_rect()
        player2_point_tip_rect.left, player2_point_tip_rect.top = self.width+5, self.height*top_idx/30
        screen.blit(player2_point_tip, player2_point_tip_rect)
        
        top_idx += 1
        player2_state_tip = self.font.render('Tank-Level: %s' % max(0, tank_player2.tanklevel), True, color_white) if tank_player2 else self.font.render('TLevel: None', True, color_white)
        player2_state_tip_rect = player2_state_tip.get_rect()
        player2_state_tip_rect.left, player2_state_tip_rect.top = self.width+5, self.height*top_idx/30
        screen.blit(player2_state_tip, player2_state_tip_rect)

        top_idx += 1
        line_tip = self.font.render("*" * 20, True, color_white)
        line_tip_rect = line_tip.get_rect()
        line_tip_rect.left, line_tip_rect.top = self.width+5, self.height*top_idx/30
        screen.blit(line_tip, line_tip_rect)
        
        top_idx += 1
        game_level_tip = self.font.render('Game Map: %s' % self.gamelevel, True, color_white)
        game_level_tip_rect = game_level_tip.get_rect()
        game_level_tip_rect.left, game_level_tip_rect.top = self.width+5, self.height*top_idx/30
        screen.blit(game_level_tip, game_level_tip_rect)
        
        # 剩余敌人数量
        top_idx += 1
        remaining_enemy_tip = self.font.render('Remain Enemy: %s' % self.total_enemy_num, True, color_white)
        remaining_enemy_tip_rect = remaining_enemy_tip.get_rect()
        remaining_enemy_tip_rect.left, remaining_enemy_tip_rect.top = self.width+5, self.height*top_idx/30
        screen.blit(remaining_enemy_tip, remaining_enemy_tip_rect)
        
        top_idx += 1
        line_tip = self.font.render("*" * 20, True, color_white)
        line_tip_rect = line_tip.get_rect()
        line_tip_rect.left, line_tip_rect.top = self.width+5, self.height*top_idx/30
        screen.blit(line_tip, line_tip_rect)

        # 玩家一操作提示
        top_idx += 1
        player1_operate_tip = self.font.render('Operate-P1:', True, color_white)
        player1_operate_tip_rect = player1_operate_tip.get_rect()
        player1_operate_tip_rect.left, player1_operate_tip_rect.top = self.width+5, self.height*top_idx/30
        screen.blit(player1_operate_tip, player1_operate_tip_rect)

        top_idx += 1
        player1_operate_tip = self.font.render('K_w: Up', True, color_white)
        player1_operate_tip_rect = player1_operate_tip.get_rect()
        player1_operate_tip_rect.left, player1_operate_tip_rect.top = self.width+5, self.height*top_idx/30
        screen.blit(player1_operate_tip, player1_operate_tip_rect)

        top_idx += 1
        player1_operate_tip = self.font.render('K_s: Down', True, color_white)
        player1_operate_tip_rect = player1_operate_tip.get_rect()
        player1_operate_tip_rect.left, player1_operate_tip_rect.top = self.width+5, self.height*top_idx/30
        screen.blit(player1_operate_tip, player1_operate_tip_rect)

        top_idx += 1
        player1_operate_tip = self.font.render('K_a: Left', True, color_white)
        player1_operate_tip_rect = player1_operate_tip.get_rect()
        player1_operate_tip_rect.left, player1_operate_tip_rect.top = self.width+5, self.height*top_idx/30
        screen.blit(player1_operate_tip, player1_operate_tip_rect)

        top_idx += 1
        player1_operate_tip = self.font.render('K_d: Right', True, color_white)
        player1_operate_tip_rect = player1_operate_tip.get_rect()
        player1_operate_tip_rect.left, player1_operate_tip_rect.top = self.width+5, self.height*top_idx/30
        screen.blit(player1_operate_tip, player1_operate_tip_rect)

        top_idx += 1
        player1_operate_tip = self.font.render('K_SPACE: Shoot', True, color_white)
        player1_operate_tip_rect = player1_operate_tip.get_rect()
        player1_operate_tip_rect.left, player1_operate_tip_rect.top = self.width+5, self.height*top_idx/30
        screen.blit(player1_operate_tip, player1_operate_tip_rect)

        top_idx += 1
        line_tip = self.font.render("*" * 20, True, color_white)
        line_tip_rect = line_tip.get_rect()
        line_tip_rect.left, line_tip_rect.top = self.width+5, self.height*top_idx/30
        screen.blit(line_tip, line_tip_rect)

        # 玩家二操作提示
        top_idx += 1
        player2_operate_tip = self.font.render('Operate-P2:', True, color_white)
        player2_operate_tip_rect = player2_operate_tip.get_rect()
        player2_operate_tip_rect.left, player2_operate_tip_rect.top = self.width+5, self.height*top_idx/30
        screen.blit(player2_operate_tip, player2_operate_tip_rect)

        top_idx += 1
        player2_operate_tip = self.font.render('K_UP: Up', True, color_white)
        player2_operate_tip_rect = player2_operate_tip.get_rect()
        player2_operate_tip_rect.left, player2_operate_tip_rect.top = self.width+5, self.height*top_idx/30
        screen.blit(player2_operate_tip, player2_operate_tip_rect)

        top_idx += 1
        player2_operate_tip = self.font.render('K_DOWN: Down', True, color_white)
        player2_operate_tip_rect = player2_operate_tip.get_rect()
        player2_operate_tip_rect.left, player2_operate_tip_rect.top = self.width+5, self.height*top_idx/30
        screen.blit(player2_operate_tip, player2_operate_tip_rect)

        top_idx += 1
        player2_operate_tip = self.font.render('K_LEFT: Left', True, color_white)
        player2_operate_tip_rect = player2_operate_tip.get_rect()
        player2_operate_tip_rect.left, player2_operate_tip_rect.top = self.width+5, self.height*top_idx/30
        screen.blit(player2_operate_tip, player2_operate_tip_rect)

        top_idx += 1
        player2_operate_tip = self.font.render('K_RIGHT: Right', True, color_white)
        player2_operate_tip_rect = player2_operate_tip.get_rect()
        player2_operate_tip_rect.left, player2_operate_tip_rect.top = self.width+5, self.height*top_idx/30
        screen.blit(player2_operate_tip, player2_operate_tip_rect)

        top_idx += 1
        player2_operate_tip = self.font.render('K_KP0: Shoot', True, color_white)
        player2_operate_tip_rect = player2_operate_tip.get_rect()
        player2_operate_tip_rect.left, player2_operate_tip_rect.top = self.width+5, self.height*top_idx/30
        screen.blit(player2_operate_tip, player2_operate_tip_rect)
        # 玩家一状态提示
        
    def __parseLevelFile(self):
        f = open(self.levelfilepath, errors='ignore')
        num_row = -1
        for line in f.readlines():
            line = line.strip('\n')
            # 注释
            if line.startswith('#') or (not line):
                continue
            # 敌方坦克总数量
            elif line.startswith('%TOTALENEMYNUM'):
                self.total_enemy_num = int(line.split(':')[-1])
            # 场上敌方坦克最大数量
            elif line.startswith('%MAXENEMYNUM'):
                self.max_enemy_num = int(line.split(':')[-1])
            # 大本营位置
            elif line.startswith('%HOMEPOS'):
                self.home_position = line.split(':')[-1]
                self.home_position = [int(self.home_position.split(',')[0]), int(self.home_position.split(',')[1])]
                self.home_position = (self.border_len+self.home_position[0]*self.grid_size, self.border_len+self.home_position[1]*self.grid_size)
            # 大本营周围位置
            elif line.startswith('%HOMEAROUNDPOS'):
                self.home_around_positions = line.split(':')[-1]
                self.home_around_positions = [[int(pos.split(',')[0]), int(pos.split(',')[1])] for pos in self.home_around_positions.split(' ')]
                self.home_around_positions = [(self.border_len+pos[0]*self.grid_size, self.border_len+pos[1]*self.grid_size) for pos in self.home_around_positions]
            # 我方坦克初始位置
            elif line.startswith('%PLAYERTANKPOS'):
                self.player_tank_positions = line.split(':')[-1]
                self.player_tank_positions = [[int(pos.split(',')[0]), int(pos.split(',')[1])] for pos in self.player_tank_positions.split(' ')]
                self.player_tank_positions = [(self.border_len+pos[0]*self.grid_size, self.border_len+pos[1]*self.grid_size) for pos in self.player_tank_positions]
            # 敌方坦克初始位置
            elif line.startswith('%ENEMYTANKPOS'):
                self.enemy_tank_positions = line.split(':')[-1]
                self.enemy_tank_positions = [[int(pos.split(',')[0]), int(pos.split(',')[1])] for pos in self.enemy_tank_positions.split(' ')]
                self.enemy_tank_positions = [(self.border_len+pos[0]*self.grid_size, self.border_len+pos[1]*self.grid_size) for pos in self.enemy_tank_positions]
            # 地图元素
            else:
                num_row += 1
                for num_col, elem in enumerate(line.split(' ')):
                    position = self.border_len+num_col*self.grid_size, self.border_len+num_row*self.grid_size
                    if elem == 'B':
                        self.scene_elems['brick_group'].add(Brick(position, self.resource_loader.images['scene']['brick']))
                    elif elem == 'I':
                        self.scene_elems['iron_group'].add(Iron(position, self.resource_loader.images['scene']['iron']))
                    elif elem == 'R':
                        self.scene_elems['river_group'].add(River(position, random.choice([self.resource_loader.images['scene']['river1'], self.resource_loader.images['scene']['river2']])))
                    elif elem == 'C':
                        self.scene_elems['ice_group'].add(Ice(position, self.resource_loader.images['scene']['ice']))
                    elif elem == 'T':
                           self.scene_elems['tree_group'].add(Tree(position, self.resource_loader.images['scene']['tree']))