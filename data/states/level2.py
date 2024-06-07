from __future__ import division


import pygame as pg
from .. import setup, tools
from .. import constants_2 as c
from .. import game_sound
from .. components_2 import mario
from .. components_2 import collider
from .. components_2 import bricks
from .. components_2 import coin_box
from .. components_2 import enemies
from .. components_2 import checkpoint
from .. components_2 import flagpole
from .. components_2 import info
from .. components_2 import score
from .. components_2 import castle_flag
from .. components_2 import elevator




class Level2(tools._State):
    def __init__(self):
        tools._State.__init__(self)

    def startup(self, current_time, persist):
        """Called when the State object is created"""
        self.game_info = persist
        self.persist = self.game_info
        self.game_info[c.CURRENT_TIME] = current_time
        self.game_info[c.LEVEL_STATE] = c.NOT_FROZEN
        self.game_info[c.MARIO_DEAD] = False
        self.persist['current_level'] = c.LEVEL2

        self.state = c.NOT_FROZEN
        self.death_timer = 0
        self.flag_timer = 0
        self.flag_score = None
        self.flag_score_total = 0

        self.moving_score_list = []
        self.overhead_info_display = info.OverheadInfo(self.game_info, c.LEVEL)
        self.sound_manager = game_sound.Sound(self.overhead_info_display)

        self.setup_background()
        self.setup_ground()
        self.setup_pipes()
        self.setup_steps()
        self.setup_bricks()
        self.setup_coin_boxes()
        self.setup_flag_pole()
        self.setup_enemies()
        self.setup_mario()
        self.setup_checkpoints()
        self.setup_spritegroups()
        self.setup_elevators()

    def setup_background(self):
        """Sets the background image, rect and scales it to the correct
        proportions"""
        self.background = setup.GFX['level_2']
        self.back_rect = self.background.get_rect()
        self.background = pg.transform.scale(self.background,
                                  (int(self.back_rect.width*c.BACKGROUND_MULTIPLER),
                                  int(self.back_rect.height*c.BACKGROUND_MULTIPLER)))
        self.back_rect = self.background.get_rect()
        width = self.back_rect.width
        height = self.back_rect.height

        self.level = pg.Surface((width, height)).convert()
        self.level_rect = self.level.get_rect()
        self.viewport = setup.SCREEN.get_rect(bottom=self.level_rect.bottom)
        self.viewport.x = self.game_info[c.CAMERA_START_X]


    def setup_ground(self):
        """Creates collideable, invisible rectangles over top of the ground for
        sprites to walk on"""
        ground_rect1 = collider.Collider(0, c.GROUND_HEIGHT, 3410, 60)
        ground_rect2 = collider.Collider(3552, c.GROUND_HEIGHT, 1585, 60)
        ground_rect3 = collider.Collider(5231, c.GROUND_HEIGHT, 65, 60)
        ground_rect4 = collider.Collider(5400, c.GROUND_HEIGHT, 537, 60)
        ground_rect5 = collider.Collider(6200, c.GROUND_HEIGHT, 340, 60)
        ground_rect6 = collider.Collider(6862, c.GROUND_HEIGHT, 3000, 60)

        self.ground_group = pg.sprite.Group(ground_rect1, ground_rect2, ground_rect3,
                                            ground_rect4, ground_rect5, ground_rect6)


    def setup_pipes(self):
        """Create collideable rects for all the pipes"""

        pipe1 = collider.Collider(4410, 396, 83, 200)
        pipe2 = collider.Collider(4664, 357, 83, 200)
        pipe3 = collider.Collider(4923, 442, 83, 200)
        pipe4 = collider.Collider(7666, 442, 83, 200)

        self.pipe_group = pg.sprite.Group(pipe1, pipe2,
                                          pipe3, pipe4)


    def setup_steps(self):
        """Create collideable rects for all the steps"""
        step1 = collider.Collider(723, 480, 40, 44)
        step2 = collider.Collider(808, 437, 40, 88)
        step3 = collider.Collider(893, 394, 40, 132)
        step4 = collider.Collider(978, 351, 40, 176)
        step5 = collider.Collider(1063, 351, 40, 176)
        step6 = collider.Collider(1148, 394, 40, 132)
        step7 = collider.Collider(1318, 394, 40, 132)
        step8 = collider.Collider(1403, 437, 40, 88)

        step24 = collider.Collider(2300, 435, 95, 44)


        step9 = collider.Collider(5693, 480, 40, 44)
        step10 = collider.Collider(5736, 437, 40, 88)
        step11 = collider.Collider(5779, 394, 40, 132)
        step12 = collider.Collider(5822, 351, 40, 176)
        step13 = collider.Collider(5865, 351, 40, 176)



        step14 = collider.Collider(7745, 480, 40, 44)
        step15 = collider.Collider(7788, 437, 40, 88)
        step16 = collider.Collider(7831, 394, 40, 132)
        step17 = collider.Collider(7874, 351, 40, 176)
        step18 = collider.Collider(7917, 308, 40, 220)
        step19 = collider.Collider(7960, 265, 40, 264)
        step20 = collider.Collider(8003, 222, 40, 308)
        step21 = collider.Collider(8046, 179, 40, 352)
        step22 = collider.Collider(8089, 179, 40, 396)

        step23 = collider.Collider(8455, 495, 40, 44)

        self.step_group = pg.sprite.Group(step1,  step2,
                                          step3,  step4,
                                          step5,  step6,
                                          step7,  step8,step9,  step10,
                                          step11, step12,
                                          step13, step14,
                                          step15, step16,
                                          step17, step18,
                                          step19, step20,
                                          step21, step22,
                                          step23, step24)





    def setup_bricks(self):
        """Creates all the breakable bricks for the level.  Coin and
        powerup groups are created so they can be passed to bricks."""
        self.coin_group = pg.sprite.Group()
        self.powerup_group = pg.sprite.Group()
        self.brick_pieces_group = pg.sprite.Group()

        # dark
        brick18 = bricks.Brick(1238, 55 + 252)
        brick24 = bricks.Brick(1665, 55 + 294)
        brick25 = bricks.Brick(1665, 55 + 252)
        brick26 = bricks.Brick(1665, 55 + 209)
        brick27 = bricks.Brick(1708, 55 + 294)
        brick28 = bricks.Brick(1752, 55 + 294)
        brick29 = bricks.Brick(1752, 55 + 252)
        brick30 = bricks.Brick(1752, 55 + 209)
        brick31 = bricks.Brick(1794, 55 + 209)
        brick32 = bricks.Brick(1837, 55 + 209)
        brick33 = bricks.Brick(1880, 55 + 209)
        brick34 = bricks.Brick(1880, 55 + 252)
        brick35 = bricks.Brick(1880, 55 + 294)
        brick36 = bricks.Brick(1923, 55 + 294)
        brick37 = bricks.Brick(1966, 55 + 294)
        brick38 = bricks.Brick(1966, 55 + 252)
        brick39 = bricks.Brick(1966, 55 + 209)
        brick40 = bricks.Brick(2221, 55 + 294)
        brick41 = bricks.Brick(2221, 55 + 252)
        brick42 = bricks.Brick(2221, 55 + 209)
        brick43 = bricks.Brick(2221, 55 + 166)
        brick44 = bricks.Brick(2221, 55 + 123)
        brick45 = bricks.Brick(2264, 55 + 294)
        brick46 = bricks.Brick(2264, 55 + 252)
        brick47 = bricks.Brick(2264, 55 + 209)
        brick48 = bricks.Brick(2264, 55 + 166)
        brick49 = bricks.Brick(2264, 55 + 123)

        brick50 = bricks.Brick(2308, 55 + 380)
        brick51 = bricks.Brick(2308, 55 + 337)
        brick52 = bricks.Brick(2308, 55 + 294)
        brick53 = bricks.Brick(2308, 55 + 80)
        brick54 = bricks.Brick(2308, 55 + 37)
        brick55 = bricks.Brick(2351, 55 + 380)
        brick56 = bricks.Brick(2351, 55 + 337)
        brick57 = bricks.Brick(2351, 55 + 294)
        brick58 = bricks.Brick(2351, 55 + 80)
        brick59 = bricks.Brick(2351, 55 + 37)

        brick60 = bricks.Brick(2481, 55 + 294)
        brick61 = bricks.Brick(2481, 55 + 80)
        brick62 = bricks.Brick(2481, 55 + 37)
        brick63 = bricks.Brick(2524, 55 + 294)
        brick64 = bricks.Brick(2524, 55 + 80)
        brick65 = bricks.Brick(2524, 55 + 37)
        brick66 = bricks.Brick(2567, 55 + 294)
        brick67 = bricks.Brick(2567, 55 + 80)
        brick68 = bricks.Brick(2567, 55 + 37)
        brick69 = bricks.Brick(2609, 55 + 294)
        brick70 = bricks.Brick(2609, 55 + 80)
        brick71 = bricks.Brick(2609, 55 + 37)
        brick72 = bricks.Brick(2652, 55 + 294)
        brick73 = bricks.Brick(2652, 55 + 252)
        brick74 = bricks.Brick(2652, 55 + 209)
        brick75 = bricks.Brick(2652, 55 + 166)
        brick76 = bricks.Brick(2652, 55 + 123)
        brick77 = bricks.Brick(2652, 55 + 80)
        brick78 = bricks.Brick(2652, 55 + 37)
        brick79 = bricks.Brick(2695, 55 + 294)
        brick80 = bricks.Brick(2695, 55 + 252)
        brick81 = bricks.Brick(2695, 55 + 209)
        brick82 = bricks.Brick(2695, 55 + 166)
        brick83 = bricks.Brick(2695, 55 + 123)
        brick84 = bricks.Brick(2695, 55 + 80)
        brick85 = bricks.Brick(2695, 55 + 37)

        brick86 = bricks.Brick(2824, 55 + 80)
        brick87 = bricks.Brick(2824, 55 + 37)

        brick88 = bricks.Brick(2867, 55 + 294)
        brick89 = bricks.Brick(2867, 55 + 252)
        brick90 = bricks.Brick(2867, 55 + 209)
        brick91 = bricks.Brick(2867, 55 + 166)
        brick92 = bricks.Brick(2867, 55 + 123)
        brick93 = bricks.Brick(2867, 55 + 80)
        brick94 = bricks.Brick(2867, 55 + 37)
        brick95 = bricks.Brick(2910, 55 + 294)
        brick96 = bricks.Brick(2910, 55 + 80)
        brick97 = bricks.Brick(2910, 55 + 37)
        brick98 = bricks.Brick(2953, 55 + 294)
        brick99 = bricks.Brick(2953, 55 + 252)
        brick100 = bricks.Brick(2953, 55 + 80)
        brick101 = bricks.Brick(2953, 55 + 37)

        brick102 = bricks.Brick(3082, 55 + 294)
        brick103 = bricks.Brick(3082, 55 + 252)
        brick104 = bricks.Brick(3082, 55 + 209)
        brick105 = bricks.Brick(3082, 55 + 166)
        brick106 = bricks.Brick(3082, 55 + 123)
        brick107 = bricks.Brick(3125, 55 + 294)
        brick108 = bricks.Brick(3125, 55 + 252)
        brick109 = bricks.Brick(3125, 55 + 209)
        brick110 = bricks.Brick(3125, 55 + 166)
        brick111 = bricks.Brick(3125, 55 + 123)

        brick112 = bricks.Brick(3254, 55 + 294)
        brick113 = bricks.Brick(3254, 55 + 80)
        brick114 = bricks.Brick(3254, 55 + 37)
        brick115 = bricks.Brick(3297, 55 + 294)
        brick116 = bricks.Brick(3297, 55 + 80)
        brick117 = bricks.Brick(3297, 55 + 37)
        brick118 = bricks.Brick(3340, 55 + 294)
        brick119 = bricks.Brick(3340, 55 + 80)
        brick120 = bricks.Brick(3340, 55 + 37)
        brick121 = bricks.Brick(3383, 55 + 294)
        brick122 = bricks.Brick(3383, 55 + 80)
        brick123 = bricks.Brick(3383, 55 + 37)

        brick124 = bricks.Brick(3595, 55 + 252)
        brick125 = bricks.Brick(3595, 55 + 209)
        brick126 = bricks.Brick(3638, 55 + 252)
        brick127 = bricks.Brick(3638, 55 + 209)
        brick128 = bricks.Brick(3681, 55 + 252)
        brick129 = bricks.Brick(3681, 55 + 209)
        brick130 = bricks.Brick(3724, 55 + 252)
        brick131 = bricks.Brick(3724, 55 + 209)
        brick132 = bricks.Brick(3767, 55 + 252)
        brick133 = bricks.Brick(3767, 55 + 209)
        brick134 = bricks.Brick(3810, 55 + 252)
        brick135 = bricks.Brick(3810, 55 + 209)

        brick136 = bricks.Brick(5224, 55 + 423)
        brick137 = bricks.Brick(5224, 55 + 380)
        brick138 = bricks.Brick(5224, 55 + 337)
        brick139 = bricks.Brick(5267, 55 + 423)
        brick140 = bricks.Brick(5267, 55 + 380)
        brick141 = bricks.Brick(5267, 55 + 337)

        brick156 = bricks.Brick(6211, 55 + 252)
        brick157 = bricks.Brick(6254, 55 + 252)
        brick158 = bricks.Brick(6298, 55 + 252)
        brick159 = bricks.Brick(6340, 55 + 252)
        brick160 = bricks.Brick(6383, 55 + 252)
        brick161 = bricks.Brick(6416, 55 + 252)


        # brick163 = bricks.Brick(6853, 380)
        # brick164 = bricks.Brick(6853, 337)
        # brick165 = bricks.Brick(6896, 423)
        # brick166 = bricks.Brick(6896, 380)
        # brick167 = bricks.Brick(6896, 337)
        # brick168 = bricks.Brick(6939, 423)
        # brick169 = bricks.Brick(6939, 380)
        # brick170 = bricks.Brick(6939, 337)
        # brick171 = bricks.Brick(6982, 423)
        # brick172 = bricks.Brick(6982, 380)
        # brick173 = bricks.Brick(6982, 337)
        # brick174 = bricks.Brick(7025, 423)
        # brick175 = bricks.Brick(7025, 380)
        # brick176 = bricks.Brick(7025, 337)
        # brick177 = bricks.Brick(7058, 423)
        # brick178 = bricks.Brick(7058, 380)
        # brick179 = bricks.Brick(7058, 337)
        # brick180 = bricks.Brick(7101, 423)
        # brick181 = bricks.Brick(7101, 380)
        # brick182 = bricks.Brick(7101, 337)
        # brick183 = bricks.Brick(7144, 423)
        # brick184 = bricks.Brick(7144, 380)
        # brick185 = bricks.Brick(7144, 337)
        # brick186 = bricks.Brick(7187, 423)
        # brick187 = bricks.Brick(7187, 380)
        # brick188 = bricks.Brick(7187, 337)
        # brick189 = bricks.Brick(7230, 423)
        # brick190 = bricks.Brick(7230, 380)
        # brick191 = bricks.Brick(7230, 337)

        #  brick1, brick2,
        # brick3, brick4,
        # brick5, brick6,
        # brick7, brick8,
        # brick9, brick10,
        # brick11, brick12,
        # brick13, brick14,
        # brick15, brick16,
        # brick17, brick18, brick19,
        # brick20, brick21, brick22, brick23,
        self.brick_group = pg.sprite.Group( brick18,
            brick24,
                                           brick25, brick26,
                                           brick27, brick28,
                                           brick29, brick30,
                                           brick31, brick32,
                                           brick33, brick34,
                                           brick35, brick36,
                                           brick37, brick38,
                                           brick39, brick40,
                                           brick41, brick42,
                                           brick43, brick44,
                                           brick45, brick46,
                                           brick47, brick48,
                                           brick49, brick50,
                                           brick51, brick52,
                                           brick53, brick54,
                                           brick55, brick56,
                                           brick57, brick58,
                                           brick59, brick60,brick61,brick62,brick63,brick64,brick65,brick66,brick67,brick68,brick69,brick70,brick71,brick72,brick73,
                                           brick74,brick75,brick76,brick77,brick78,brick79,brick80,brick81,brick82,brick83,brick84,brick85,brick86,brick87,brick88,
                                           brick89,brick90,brick91,brick92,brick93,brick94,brick95,brick96,brick97,brick98,brick99,brick100,brick101,brick102,brick103,
                                           brick104,brick105,brick106,brick107,brick108,brick109,brick110,brick111,brick112,brick113,brick114,brick115,brick116,brick117,
                                           brick118,brick119,brick120,brick121,brick121,brick122,brick123,brick124,brick125,brick126,brick127,brick128,brick129,brick130,
                                           brick131,brick132,brick133,brick134,brick135,brick136,brick137,brick138,brick139,brick140,brick141,brick156,brick157,brick158,brick159,brick160,
                                           brick161)

        # brick163, brick164, brick165, brick166, brick167, brick168, brick169, brick170, brick171, brick172, brick173, brick174, brick175, brick176,
        # brick177, brick178, brick179, brick180, brick181, brick182, brick183, brick184, brick185, brick186, brick187, brick188, brick189, brick190, brick191
# brick142,brick143,brick144,brick145,
#                                            brick146,brick147,brick148,brick149,brick150,brick151,brick152,brick153,brick154,brick155,
    def setup_coin_boxes(self):
        """Creates all the coin boxes and puts them in a sprite group"""
        coin_box1  = coin_box.Coin_box(420, 297, c.COIN, self.coin_group)
        coin_box2  = coin_box.Coin_box(465, 297, c.MUSHROOM, self.powerup_group)
        coin_box3  = coin_box.Coin_box(510, 297, c.COIN, self.coin_group)
        coin_box4  = coin_box.Coin_box(555, 297, c.COIN, self.coin_group)
        coin_box5  = coin_box.Coin_box(600, 297, c.COIN, self.coin_group)

        self.coin_box_group = pg.sprite.Group(coin_box1,  coin_box2,
                                              coin_box3,  coin_box4,
                                              coin_box5)

    def setup_flag_pole(self):
        """Creates the flag pole at the end of the level"""
        self.flag = flagpole.Flag(8482, 102)

        pole0 = flagpole.Pole(8482, 99)
        pole1 = flagpole.Pole(8482, 139)
        pole2 = flagpole.Pole(8482, 179)
        pole3 = flagpole.Pole(8482, 219)
        pole4 = flagpole.Pole(8482, 259)
        pole5 = flagpole.Pole(8482, 299)
        pole6 = flagpole.Pole(8482, 339)
        pole7 = flagpole.Pole(8482, 379)
        pole8 = flagpole.Pole(8482, 419)
        pole9 = flagpole.Pole(8482, 442)

        finial = flagpole.Finial(8482, 99)

        self.flag_pole_group = pg.sprite.Group(self.flag,
                                               finial,
                                               pole0,
                                               pole1,
                                               pole2,
                                               pole3,
                                               pole4,
                                               pole5,
                                               pole6,
                                               pole7,
                                               pole8,
                                               pole9)

    def setup_enemies(self):
        """Creates all the enemies and stores them in a list of lists."""
        #     goomba0 = enemies.Goomba(c.GROUND_HEIGHT, 100)
        #     self.enemy_group = pg.sprite.Group(goomba0)
        goomba0 = enemies.Goomba(193)
        goomba1 = enemies.Goomba(193)
        goomba2 = enemies.Goomba(193)
        goomba3 = enemies.Goomba(c.GROUND_HEIGHT)
        goomba4 = enemies.Goomba()
        goomba5 = enemies.Goomba()
        goomba6 = enemies.Goomba()
        goomba7 = enemies.Goomba()
        goomba8 = enemies.Goomba()
        goomba9 = enemies.Goomba()
        goomba10 = enemies.Goomba(c.GROUND_HEIGHT)
        goomba11 = enemies.Goomba(c.GROUND_HEIGHT)
        goomba12 = enemies.Goomba(c.GROUND_HEIGHT)
        goomba13 = enemies.Goomba()
        goomba14 = enemies.Goomba()
        goomba15 = enemies.Goomba()

        koopa0 = enemies.Koopa(c.GROUND_HEIGHT)
        koopa1 = enemies.Koopa(c.GROUND_HEIGHT)
        koopa2 = enemies.Koopa(c.GROUND_HEIGHT)
        koopa3 = enemies.Koopa(c.GROUND_HEIGHT)

        enemy_group1 = pg.sprite.Group(goomba0, goomba1)
        enemy_group2 = pg.sprite.Group(goomba2)
        enemy_group3 = pg.sprite.Group(koopa0, koopa1)
        enemy_group4 = pg.sprite.Group(koopa2)
        enemy_group5 = pg.sprite.Group(goomba3, goomba4)
        enemy_group6 = pg.sprite.Group(goomba6)
        enemy_group7 = pg.sprite.Group(goomba7)
        enemy_group8 = pg.sprite.Group(goomba8)
        enemy_group9 = pg.sprite.Group(goomba10, goomba11, goomba12)
        enemy_group10 = pg.sprite.Group(koopa3)
        enemy_group11 = pg.sprite.Group()

        self.enemy_group_list = [
            enemy_group1,
            enemy_group2,
            enemy_group3,
            enemy_group4,
            enemy_group5,
            enemy_group6,
            enemy_group7,
            enemy_group8,
            enemy_group9,
            enemy_group10,
            enemy_group11
        ]

    #
    # def setup_piranha_plant(x, y):
    #     piranha = PiranhaPlant(700, 423)
    #     return pg.sprite.Group([piranha])

    def setup_mario(self):
        """Places Mario at the beginning of the level"""
        self.mario = mario.Mario()
        self.mario.rect.x = self.viewport.x + 110
        self.mario.rect.bottom = c.GROUND_HEIGHT

    def setup_checkpoints(self):
        """Creates invisible checkpoints that when collided will trigger
        the creation of enemies from the self.enemy_group_list"""
        check1 = checkpoint.Checkpoint(200, "1")
        check2 = checkpoint.Checkpoint(900, '2')
        check3 = checkpoint.Checkpoint(1400, '3')
        check4 = checkpoint.Checkpoint(2000, '4')
        check5 = checkpoint.Checkpoint(2500, '5')
        check6 = checkpoint.Checkpoint(2800, '6')
        check7 = checkpoint.Checkpoint(2900, '7')
        check8 = checkpoint.Checkpoint(3000, '8')
        check9 = checkpoint.Checkpoint(3700, '9')
        check10 = checkpoint.Checkpoint(6000, '10')
        check11 = checkpoint.Checkpoint(8482, '11', 5, 6)
        check12 = checkpoint.Checkpoint(8753, '12')
        check13 = checkpoint.Checkpoint(2740, 'secret_mushroom', 360, 40, 12)

        self.check_point_group = pg.sprite.Group(check1, check2, check3,
                                                 check4, check5, check6,
                                                 check7, check8, check9,
                                                 check10, check11, check12,
                                                 check13)


    def setup_elevators(self):
        elevator1 = elevator.Elevator(6000, 300, 120, 30, 50, 400, 2)
        elevator2 = elevator.Elevator(6650, 300, 120, 30, 50, 400, 2)
        self.elevator_group = pg.sprite.Group(elevator1, elevator2)
    def setup_spritegroups(self):
        """Sprite groups created for convenience"""
        self.sprites_about_to_die_group = pg.sprite.Group()
        self.shell_group = pg.sprite.Group()
        self.enemy_group = pg.sprite.Group()

        self.ground_step_pipe_group = pg.sprite.Group(self.ground_group,
                                                      self.pipe_group,
                                                      self.step_group)

        self.mario_and_enemy_group = pg.sprite.Group(self.mario,
                                                     self.enemy_group)


    def update(self, surface, keys, current_time):
        """Updates Entire level using states.  Called by the control object"""
        self.game_info[c.CURRENT_TIME] = self.current_time = current_time
        self.handle_states(keys)
        self.check_if_time_out()
        self.blit_everything(surface)
        self.sound_manager.update(self.game_info, self.mario)



    def handle_states(self, keys):
        """If the level is in a FROZEN state, only mario will update"""
        if self.state == c.FROZEN:
            self.update_during_transition_state(keys)
        elif self.state == c.NOT_FROZEN:
            self.update_all_sprites(keys)
        elif self.state == c.IN_CASTLE:
            self.update_while_in_castle()
        elif self.state == c.FLAG_AND_FIREWORKS:
            self.update_flag_and_fireworks()


    def update_during_transition_state(self, keys):
        """Updates mario in a transition state (like becoming big, small,
         or dies). Checks if he leaves the transition state or dies to
         change the level state back"""
        self.mario.update(keys, self.game_info, self.powerup_group)
        for score in self.moving_score_list:
            score.update(self.moving_score_list, self.game_info)
        if self.flag_score:
            self.flag_score.update(None, self.game_info)
            self.check_to_add_flag_score()
        self.coin_box_group.update(self.game_info)
        self.flag_pole_group.update(self.game_info)
        self.check_if_mario_in_transition_state()
        self.check_flag()
        self.check_for_mario_death()
        self.overhead_info_display.update(self.game_info, self.mario)


    def check_if_mario_in_transition_state(self):
        """If mario is in a transition state, the level will be in a FREEZE
        state"""
        if self.mario.in_transition_state:
            self.game_info[c.LEVEL_STATE] = self.state = c.FROZEN
        elif self.mario.in_transition_state == False:
            if self.state == c.FROZEN:
                self.game_info[c.LEVEL_STATE] = self.state = c.NOT_FROZEN


    def update_all_sprites(self, keys):
        """Updates the location of all sprites on the screen."""
        self.mario.update(keys, self.game_info, self.powerup_group)
        for score in self.moving_score_list:
            score.update(self.moving_score_list, self.game_info)
        if self.flag_score:
            self.flag_score.update(None, self.game_info)
            self.check_to_add_flag_score()
        self.flag_pole_group.update()
        self.check_points_check()
        self.enemy_group.update(self.game_info)
        self.sprites_about_to_die_group.update(self.game_info, self.viewport)
        self.shell_group.update(self.game_info)
        self.brick_group.update()
        self.coin_box_group.update(self.game_info)
        self.powerup_group.update(self.game_info, self.viewport)
        self.coin_group.update(self.game_info, self.viewport)
        self.brick_pieces_group.update()
        self.elevator_group.update()
        self.adjust_sprite_positions()
        self.check_if_mario_in_transition_state()
        self.check_for_mario_death()
        self.update_viewport()
        self.overhead_info_display.update(self.game_info, self.mario)


    def check_points_check(self):
        """Detect if checkpoint collision occurs, delete checkpoint,
        add enemies to self.enemy_group"""
        checkpoint = pg.sprite.spritecollideany(self.mario,
                                                 self.check_point_group)
        if checkpoint:
            checkpoint.kill()

            for i in range(1,11):
                if checkpoint.name == str(i):
                    for index, enemy in enumerate(self.enemy_group_list[i -1]):
                        enemy.rect.x = self.viewport.right + (index * 60)
                    self.enemy_group.add(self.enemy_group_list[i-1])

            if checkpoint.name == '11':
                self.mario.state = c.FLAGPOLE
                self.mario.invincible = False
                self.mario.flag_pole_right = checkpoint.rect.right
                if self.mario.rect.bottom < self.flag.rect.y:
                    self.mario.rect.bottom = self.flag.rect.y
                self.flag.state = c.SLIDE_DOWN
                self.create_flag_points()

            elif checkpoint.name == '12':
                self.state = c.IN_CASTLE
                self.mario.kill()
                self.mario.state == c.STAND
                self.mario.in_castle = True
                self.overhead_info_display.state = c.FAST_COUNT_DOWN




            elif checkpoint.name == 'secret_mushroom' and self.mario.y_vel < 0:
                mushroom_box = coin_box.Coin_box(checkpoint.rect.x,
                                        checkpoint.rect.bottom - 40,
                                        '1up_mushroom',
                                        self.powerup_group)
                mushroom_box.start_bump(self.moving_score_list)
                self.coin_box_group.add(mushroom_box)

                self.mario.y_vel = 7
                self.mario.rect.y = mushroom_box.rect.bottom
                self.mario.state = c.FALL

            self.mario_and_enemy_group.add(self.enemy_group)


    def create_flag_points(self):
        """Creates the points that appear when Mario touches the
        flag pole"""
        x = 6900
        y = c.GROUND_HEIGHT - 200
        mario_bottom = self.mario.rect.bottom

        if mario_bottom > (c.GROUND_HEIGHT - 40 - 40):
            self.flag_score = score.Score(x, y, 100, True)
            self.flag_score_total = 100
        elif mario_bottom > (c.GROUND_HEIGHT - 40 - 160):
            self.flag_score = score.Score(x, y, 400, True)
            self.flag_score_total = 400
        elif mario_bottom > (c.GROUND_HEIGHT - 40 - 240):
            self.flag_score = score.Score(x, y, 800, True)
            self.flag_score_total = 800
        elif mario_bottom > (c.GROUND_HEIGHT - 40 - 360):
            self.flag_score = score.Score(x, y, 2000, True)
            self.flag_score_total = 2000
        else:
            self.flag_score = score.Score(x, y, 5000, True)
            self.flag_score_total = 5000


    def adjust_sprite_positions(self):
        """Adjusts sprites by their x and y velocities and collisions"""
        self.adjust_mario_position()
        self.adjust_enemy_position()
        self.adjust_shell_position()
        self.adjust_powerup_position()


    def adjust_mario_position(self):
        """Adjusts Mario's position based on his x, y velocities and
        potential collisions"""
        self.last_x_position = self.mario.rect.right
        self.mario.rect.x += round(self.mario.x_vel)
        self.check_mario_x_collisions()

        if self.mario.in_transition_state == False:
            self.mario.rect.y += round(self.mario.y_vel)
            self.check_mario_y_collisions()

        if self.mario.rect.x < (self.viewport.x + 5):
            self.mario.rect.x = (self.viewport.x + 5)

        elevator = pg.sprite.spritecollideany(self.mario, self.elevator_group)
        if elevator and self.mario.y_vel >= 0:
            self.mario.rect.bottom = elevator.rect.top
            self.mario.y_vel = 0
            self.mario.state = c.WALK
            self.mario.rect.y += elevator.speed * elevator.direction

    def check_mario_x_collisions(self):
        """Check for collisions after Mario is moved on the x axis"""
        collider = pg.sprite.spritecollideany(self.mario, self.ground_step_pipe_group)
        coin_box = pg.sprite.spritecollideany(self.mario, self.coin_box_group)
        brick = pg.sprite.spritecollideany(self.mario, self.brick_group)
        enemy = pg.sprite.spritecollideany(self.mario, self.enemy_group)
        shell = pg.sprite.spritecollideany(self.mario, self.shell_group)
        powerup = pg.sprite.spritecollideany(self.mario, self.powerup_group)

        if coin_box:
            self.adjust_mario_for_x_collisions(coin_box)

        elif brick:
            self.adjust_mario_for_x_collisions(brick)

        elif collider:
            self.adjust_mario_for_x_collisions(collider)

        elif enemy:
            if self.mario.invincible:
                setup.SFX['kick'].play()
                self.game_info[c.SCORE] += 100
                self.moving_score_list.append(
                    score.Score(self.mario.rect.right - self.viewport.x,
                                self.mario.rect.y, 100))
                enemy.kill()
                enemy.start_death_jump(c.RIGHT)
                self.sprites_about_to_die_group.add(enemy)
            elif self.mario.big:
                setup.SFX['pipe'].play()
                self.mario.fire = False
                self.mario.y_vel = -1
                self.mario.state = c.BIG_TO_SMALL
                self.convert_fireflowers_to_mushrooms()
            elif self.mario.hurt_invincible:
                pass
            else:
                self.mario.start_death_jump(self.game_info)
                self.state = c.FROZEN

        elif shell:
            self.adjust_mario_for_x_shell_collisions(shell)

        elif powerup:
            if powerup.name == c.STAR:
                self.game_info[c.SCORE] += 1000

                self.moving_score_list.append(
                    score.Score(self.mario.rect.centerx - self.viewport.x,
                                self.mario.rect.y, 1000))
                self.mario.invincible = True
                self.mario.invincible_start_timer = self.current_time
            elif powerup.name == c.MUSHROOM:
                setup.SFX['powerup'].play()
                self.game_info[c.SCORE] += 1000
                self.moving_score_list.append(
                    score.Score(self.mario.rect.centerx - self.viewport.x,
                                self.mario.rect.y - 20, 1000))

                self.mario.y_vel = -1
                self.mario.state = c.SMALL_TO_BIG
                self.mario.in_transition_state = True
                self.convert_mushrooms_to_fireflowers()
            elif powerup.name == c.LIFE_MUSHROOM:
                self.moving_score_list.append(
                    score.Score(powerup.rect.right - self.viewport.x,
                                powerup.rect.y,
                                c.ONEUP))

                self.game_info[c.LIVES] += 1
                setup.SFX['one_up'].play()
            elif powerup.name == c.FIREFLOWER:
                setup.SFX['powerup'].play()
                self.game_info[c.SCORE] += 1000
                self.moving_score_list.append(
                    score.Score(self.mario.rect.centerx - self.viewport.x,
                                self.mario.rect.y, 1000))

                if self.mario.big and self.mario.fire == False:
                    self.mario.state = c.BIG_TO_FIRE
                    self.mario.in_transition_state = True
                elif self.mario.big == False:
                    self.mario.state = c.SMALL_TO_BIG
                    self.mario.in_transition_state = True
                    self.convert_mushrooms_to_fireflowers()

            if powerup.name != c.FIREBALL:
                powerup.kill()


    def convert_mushrooms_to_fireflowers(self):
        """When Mario becomees big, converts all fireflower powerups to
        mushroom powerups"""
        for brick in self.brick_group:
            if brick.contents == c.MUSHROOM:
                brick.contents = c.FIREFLOWER
        for coin_box in self.coin_box_group:
            if coin_box.contents == c.MUSHROOM:
                coin_box.contents = c.FIREFLOWER


    def convert_fireflowers_to_mushrooms(self):
        """When Mario becomes small, converts all mushroom powerups to
        fireflower powerups"""
        for brick in self.brick_group:
            if brick.contents == c.FIREFLOWER:
                brick.contents = c.MUSHROOM
        for coin_box in self.coin_box_group:
            if coin_box.contents == c.FIREFLOWER:
                coin_box.contents = c.MUSHROOM


    def adjust_mario_for_x_collisions(self, collider):
        """Puts Mario flush next to the collider after moving on the x axis"""
        if self.mario.rect.x < collider.rect.x:
            self.mario.rect.right = collider.rect.left
        else:
            self.mario.rect.left = collider.rect.right

        self.mario.x_vel = 0


    def adjust_mario_for_x_shell_collisions(self, shell):
        """Deals with Mario if he hits a shell moving on the x axis"""
        if shell.state == c.JUMPED_ON:
            if self.mario.rect.x < shell.rect.x:
                self.game_info[c.SCORE] += 400
                self.moving_score_list.append(
                    score.Score(shell.rect.centerx - self.viewport.x,
                                shell.rect.y,
                                400))
                self.mario.rect.right = shell.rect.left
                shell.direction = c.RIGHT
                shell.x_vel = 5
                shell.rect.x += 5

            else:
                self.mario.rect.left = shell.rect.right
                shell.direction = c.LEFT
                shell.x_vel = -5
                shell.rect.x += -5

            shell.state = c.SHELL_SLIDE

        elif shell.state == c.SHELL_SLIDE:
            if self.mario.big and not self.mario.invincible:
                self.mario.state = c.BIG_TO_SMALL
            elif self.mario.invincible:
                self.game_info[c.SCORE] += 200
                self.moving_score_list.append(
                    score.Score(shell.rect.right - self.viewport.x,
                                shell.rect.y, 200))
                shell.kill()
                self.sprites_about_to_die_group.add(shell)
                shell.start_death_jump(c.RIGHT)
            else:
                if not self.mario.hurt_invincible and not self.mario.invincible:
                    self.state = c.FROZEN
                    self.mario.start_death_jump(self.game_info)


    def check_mario_y_collisions(self):
        """Checks for collisions when Mario moves along the y-axis"""
        ground_step_or_pipe = pg.sprite.spritecollideany(self.mario, self.ground_step_pipe_group)
        enemy = pg.sprite.spritecollideany(self.mario, self.enemy_group)
        shell = pg.sprite.spritecollideany(self.mario, self.shell_group)
        brick = pg.sprite.spritecollideany(self.mario, self.brick_group)
        coin_box = pg.sprite.spritecollideany(self.mario, self.coin_box_group)
        powerup = pg.sprite.spritecollideany(self.mario, self.powerup_group)

        brick, coin_box = self.prevent_collision_conflict(brick, coin_box)

        if coin_box:
            self.adjust_mario_for_y_coin_box_collisions(coin_box)

        elif brick:
            self.adjust_mario_for_y_brick_collisions(brick)

        elif ground_step_or_pipe:
            self.adjust_mario_for_y_ground_pipe_collisions(ground_step_or_pipe)

        elif enemy:
            if self.mario.invincible:
                setup.SFX['kick'].play()
                enemy.kill()
                self.sprites_about_to_die_group.add(enemy)
                enemy.start_death_jump(c.RIGHT)
            else:
                self.adjust_mario_for_y_enemy_collisions(enemy)

        elif shell:
            self.adjust_mario_for_y_shell_collisions(shell)

        elif powerup:
            if powerup.name == c.STAR:
                setup.SFX['powerup'].play()
                powerup.kill()
                self.mario.invincible = True
                self.mario.invincible_start_timer = self.current_time

        self.test_if_mario_is_falling()


    def prevent_collision_conflict(self, obstacle1, obstacle2):
        """Allows collisions only for the item closest to marios centerx"""
        if obstacle1 and obstacle2:
            obstacle1_distance = self.mario.rect.centerx - obstacle1.rect.centerx
            if obstacle1_distance < 0:
                obstacle1_distance *= -1
            obstacle2_distance = self.mario.rect.centerx - obstacle2.rect.centerx
            if obstacle2_distance < 0:
                obstacle2_distance *= -1

            if obstacle1_distance < obstacle2_distance:
                obstacle2 = False
            else:
                obstacle1 = False

        return obstacle1, obstacle2


    def adjust_mario_for_y_coin_box_collisions(self, coin_box):
        """Mario collisions with coin boxes on the y-axis"""
        if self.mario.rect.y > coin_box.rect.y:
            if coin_box.state == c.RESTING:
                if coin_box.contents == c.COIN:
                    self.game_info[c.SCORE] += 200
                    coin_box.start_bump(self.moving_score_list)
                    if coin_box.contents == c.COIN:
                        self.game_info[c.COIN_TOTAL] += 1
                else:
                    coin_box.start_bump(self.moving_score_list)

            elif coin_box.state == c.OPENED:
                pass
            setup.SFX['bump'].play()
            self.mario.y_vel = 7
            self.mario.rect.y = coin_box.rect.bottom
            self.mario.state = c.FALL
        else:
            self.mario.y_vel = 0
            self.mario.rect.bottom = coin_box.rect.top
            self.mario.state = c.WALK


    def adjust_mario_for_y_brick_collisions(self, brick):
        """Mario collisions with bricks on the y-axis"""
        if self.mario.rect.y > brick.rect.y:
            if brick.state == c.RESTING:
                if self.mario.big and brick.contents is None:
                    setup.SFX['brick_smash'].play()
                    self.check_if_enemy_on_brick(brick)
                    brick.kill()
                    self.brick_pieces_group.add(
                        bricks.BrickPiece(brick.rect.x,
                                               brick.rect.y - (brick.rect.height/2),
                                               -2, -12),
                        bricks.BrickPiece(brick.rect.right,
                                               brick.rect.y - (brick.rect.height/2),
                                               2, -12),
                        bricks.BrickPiece(brick.rect.x,
                                               brick.rect.y,
                                               -2, -6),
                        bricks.BrickPiece(brick.rect.right,
                                               brick.rect.y,
                                               2, -6))
                else:
                    setup.SFX['bump'].play()
                    if brick.coin_total > 0:
                        self.game_info[c.COIN_TOTAL] += 1
                        self.game_info[c.SCORE] += 200
                    self.check_if_enemy_on_brick(brick)
                    brick.start_bump(self.moving_score_list)
            elif brick.state == c.OPENED:
                setup.SFX['bump'].play()
            self.mario.y_vel = 7
            self.mario.rect.y = brick.rect.bottom
            self.mario.state = c.FALL

        else:
            self.mario.y_vel = 0
            self.mario.rect.bottom = brick.rect.top
            self.mario.state = c.WALK


    def check_if_enemy_on_brick(self, brick):
        """Kills enemy if on a bumped or broken brick"""
        brick.rect.y -= 5

        enemy = pg.sprite.spritecollideany(brick, self.enemy_group)

        if enemy:
            setup.SFX['kick'].play()
            self.game_info[c.SCORE] += 100
            self.moving_score_list.append(
                score.Score(enemy.rect.centerx - self.viewport.x,
                            enemy.rect.y,
                            100))
            enemy.kill()
            self.sprites_about_to_die_group.add(enemy)
            if self.mario.rect.centerx > brick.rect.centerx:
                enemy.start_death_jump('right')
            else:
                enemy.start_death_jump('left')

        brick.rect.y += 5



    def adjust_mario_for_y_ground_pipe_collisions(self, collider):
        """Mario collisions with pipes on the y-axis"""
        if collider.rect.bottom > self.mario.rect.bottom:
            self.mario.y_vel = 0
            self.mario.rect.bottom = collider.rect.top
            if self.mario.state == c.END_OF_LEVEL_FALL:
                self.mario.state = c.WALKING_TO_CASTLE
            else:
                self.mario.state = c.WALK
        elif collider.rect.top < self.mario.rect.top:
            self.mario.y_vel = 7
            self.mario.rect.top = collider.rect.bottom
            self.mario.state = c.FALL


    def test_if_mario_is_falling(self):
        """Changes Mario to a FALL state if more than a pixel above a pipe,
        ground, step or box"""
        self.mario.rect.y += 1
        test_collide_group = pg.sprite.Group(self.ground_step_pipe_group,
                                                 self.brick_group,
                                                 self.coin_box_group)


        if pg.sprite.spritecollideany(self.mario, test_collide_group) is None:
            if self.mario.state != c.JUMP \
                and self.mario.state != c.DEATH_JUMP \
                and self.mario.state != c.SMALL_TO_BIG \
                and self.mario.state != c.BIG_TO_FIRE \
                and self.mario.state != c.BIG_TO_SMALL \
                and self.mario.state != c.FLAGPOLE \
                and self.mario.state != c.WALKING_TO_CASTLE \
                and self.mario.state != c.END_OF_LEVEL_FALL:
                self.mario.state = c.FALL
            elif self.mario.state == c.WALKING_TO_CASTLE or \
                self.mario.state == c.END_OF_LEVEL_FALL:
                self.mario.state = c.END_OF_LEVEL_FALL

        self.mario.rect.y -= 1


    def adjust_mario_for_y_enemy_collisions(self, enemy):
        """Mario collisions with all enemies on the y-axis"""
        if self.mario.y_vel > 0:
            setup.SFX['stomp'].play()
            self.game_info[c.SCORE] += 100
            self.moving_score_list.append(
                score.Score(enemy.rect.centerx - self.viewport.x,
                            enemy.rect.y, 100))
            enemy.state = c.JUMPED_ON
            enemy.kill()
            if enemy.name == c.GOOMBA:
                enemy.death_timer = self.current_time
                self.sprites_about_to_die_group.add(enemy)
            elif enemy.name == c.KOOPA:
                self.shell_group.add(enemy)

            self.mario.rect.bottom = enemy.rect.top
            self.mario.state = c.JUMP
            self.mario.y_vel = -7
        


    def adjust_mario_for_y_shell_collisions(self, shell):
        """Mario collisions with Koopas in their shells on the y axis"""
        if self.mario.y_vel > 0:
            self.game_info[c.SCORE] += 400
            self.moving_score_list.append(
                score.Score(self.mario.rect.centerx - self.viewport.x,
                            self.mario.rect.y, 400))
            if shell.state == c.JUMPED_ON:
                setup.SFX['kick'].play()
                shell.state = c.SHELL_SLIDE
                if self.mario.rect.centerx < shell.rect.centerx:
                    shell.direction = c.RIGHT
                    shell.rect.left = self.mario.rect.right + 5
                else:
                    shell.direction = c.LEFT
                    shell.rect.right = self.mario.rect.left - 5
            else:
                shell.state = c.JUMPED_ON


    def adjust_enemy_position(self):
        """Moves all enemies along the x, y axes and check for collisions"""
        for enemy in self.enemy_group:
            enemy.rect.x += enemy.x_vel
            self.check_enemy_x_collisions(enemy)

            enemy.rect.y += enemy.y_vel
            self.check_enemy_y_collisions(enemy)
            self.delete_if_off_screen(enemy)


    def check_enemy_x_collisions(self, enemy):
        """Enemy collisions along the x axis.  Removes enemy from enemy group
        in order to check against all other enemies then adds it back."""
        enemy.kill()

        collider = pg.sprite.spritecollideany(enemy, self.ground_step_pipe_group)
        enemy_collider = pg.sprite.spritecollideany(enemy, self.enemy_group)

        if collider:
            if enemy.direction == c.RIGHT:
                enemy.rect.right = collider.rect.left
                enemy.direction = c.LEFT
                enemy.x_vel = -2
            elif enemy.direction == c.LEFT:
                enemy.rect.left = collider.rect.right
                enemy.direction = c.RIGHT
                enemy.x_vel = 2


        elif enemy_collider:
            if enemy.direction == c.RIGHT:
                enemy.rect.right = enemy_collider.rect.left
                enemy.direction = c.LEFT
                enemy_collider.direction = c.RIGHT
                enemy.x_vel = -2
                enemy_collider.x_vel = 2
            elif enemy.direction == c.LEFT:
                enemy.rect.left = enemy_collider.rect.right
                enemy.direction = c.RIGHT
                enemy_collider.direction = c.LEFT
                enemy.x_vel = 2
                enemy_collider.x_vel = -2

        self.enemy_group.add(enemy)
        self.mario_and_enemy_group.add(self.enemy_group)


    def check_enemy_y_collisions(self, enemy):
        """Enemy collisions on the y axis"""
        collider = pg.sprite.spritecollideany(enemy, self.ground_step_pipe_group)
        brick = pg.sprite.spritecollideany(enemy, self.brick_group)
        coin_box = pg.sprite.spritecollideany(enemy, self.coin_box_group)

        if collider:
            if enemy.rect.bottom > collider.rect.bottom:
                enemy.y_vel = 7
                enemy.rect.top = collider.rect.bottom
                enemy.state = c.FALL
            elif enemy.rect.bottom < collider.rect.bottom:

                enemy.y_vel = 0
                enemy.rect.bottom = collider.rect.top
                enemy.state = c.WALK

        elif brick:
            if brick.state == c.BUMPED:
                enemy.kill()
                self.sprites_about_to_die_group.add(enemy)
                if self.mario.rect.centerx > brick.rect.centerx:
                    enemy.start_death_jump('right')
                else:
                    enemy.start_death_jump('left')

            elif enemy.rect.x > brick.rect.x:
                enemy.y_vel = 7
                enemy.rect.top = brick.rect.bottom
                enemy.state = c.FALL
            else:
                enemy.y_vel = 0
                enemy.rect.bottom = brick.rect.top
                enemy.state = c.WALK

        elif coin_box:
            if coin_box.state == c.BUMPED:
                self.game_info[c.SCORE] += 100
                self.moving_score_list.append(
                    score.Score(enemy.rect.centerx - self.viewport.x,
                                enemy.rect.y, 100))
                enemy.kill()
                self.sprites_about_to_die_group.add(enemy)
                if self.mario.rect.centerx > coin_box.rect.centerx:
                    enemy.start_death_jump('right')
                else:
                    enemy.start_death_jump('left')

            elif enemy.rect.x > coin_box.rect.x:
                enemy.y_vel = 7
                enemy.rect.top = coin_box.rect.bottom
                enemy.state = c.FALL
            else:
                enemy.y_vel = 0
                enemy.rect.bottom = coin_box.rect.top
                enemy.state = c.WALK


        else:
            enemy.rect.y += 1
            test_group = pg.sprite.Group(self.ground_step_pipe_group,
                                         self.coin_box_group,
                                         self.brick_group)
            if pg.sprite.spritecollideany(enemy, test_group) is None:
                if enemy.state != c.JUMP:
                    enemy.state = c.FALL

            enemy.rect.y -= 1


    def adjust_shell_position(self):
        """Moves any koopa in a shell along the x, y axes and checks for
        collisions"""
        for shell in self.shell_group:
            shell.rect.x += shell.x_vel
            self.check_shell_x_collisions(shell)

            shell.rect.y += shell.y_vel
            self.check_shell_y_collisions(shell)
            self.delete_if_off_screen(shell)


    def check_shell_x_collisions(self, shell):
        """Shell collisions along the x axis"""
        collider = pg.sprite.spritecollideany(shell, self.ground_step_pipe_group)
        enemy = pg.sprite.spritecollideany(shell, self.enemy_group)

        if collider:
            setup.SFX['bump'].play()
            if shell.x_vel > 0:
                shell.direction = c.LEFT
                shell.rect.right = collider.rect.left
            else:
                shell.direction = c.RIGHT
                shell.rect.left = collider.rect.right

        if enemy:
            setup.SFX['kick'].play()
            self.game_info[c.SCORE] += 100
            self.moving_score_list.append(
                score.Score(enemy.rect.right - self.viewport.x,
                            enemy.rect.y, 100))
            enemy.kill()
            self.sprites_about_to_die_group.add(enemy)
            enemy.start_death_jump(shell.direction)


    def check_shell_y_collisions(self, shell):
        """Shell collisions along the y axis"""
        collider = pg.sprite.spritecollideany(shell, self.ground_step_pipe_group)

        if collider:
            shell.y_vel = 0
            shell.rect.bottom = collider.rect.top
            shell.state = c.SHELL_SLIDE

        else:
            shell.rect.y += 1
            if pg.sprite.spritecollideany(shell, self.ground_step_pipe_group) is None:
                shell.state = c.FALL
            shell.rect.y -= 1


    def adjust_powerup_position(self):
        """Moves mushrooms, stars and fireballs along the x, y axes"""
        for powerup in self.powerup_group:
            if powerup.name == c.MUSHROOM:
                self.adjust_mushroom_position(powerup)
            elif powerup.name == c.STAR:
                self.adjust_star_position(powerup)
            elif powerup.name == c.FIREBALL:
                self.adjust_fireball_position(powerup)
            elif powerup.name == '1up_mushroom':
                self.adjust_mushroom_position(powerup)


    def adjust_mushroom_position(self, mushroom):
        """Moves mushroom along the x, y axes."""
        if mushroom.state != c.REVEAL:
            mushroom.rect.x += mushroom.x_vel
            self.check_mushroom_x_collisions(mushroom)

            mushroom.rect.y += mushroom.y_vel
            self.check_mushroom_y_collisions(mushroom)
            self.delete_if_off_screen(mushroom)


    def check_mushroom_x_collisions(self, mushroom):
        """Mushroom collisions along the x axis"""
        collider = pg.sprite.spritecollideany(mushroom, self.ground_step_pipe_group)
        brick = pg.sprite.spritecollideany(mushroom, self.brick_group)
        coin_box = pg.sprite.spritecollideany(mushroom, self.coin_box_group)

        if collider:
            self.adjust_mushroom_for_collision_x(mushroom, collider)

        elif brick:
            self.adjust_mushroom_for_collision_x(mushroom, brick)

        elif coin_box:
            self.adjust_mushroom_for_collision_x(mushroom, coin_box)


    def check_mushroom_y_collisions(self, mushroom):
        """Mushroom collisions along the y axis"""
        collider = pg.sprite.spritecollideany(mushroom, self.ground_step_pipe_group)
        brick = pg.sprite.spritecollideany(mushroom, self.brick_group)
        coin_box = pg.sprite.spritecollideany(mushroom, self.coin_box_group)

        if collider:
            self.adjust_mushroom_for_collision_y(mushroom, collider)
        elif brick:
            self.adjust_mushroom_for_collision_y(mushroom, brick)
        elif coin_box:
            self.adjust_mushroom_for_collision_y(mushroom, coin_box)
        else:
            self.check_if_falling(mushroom, self.ground_step_pipe_group)
            self.check_if_falling(mushroom, self.brick_group)
            self.check_if_falling(mushroom, self.coin_box_group)


    def adjust_mushroom_for_collision_x(self, item, collider):
        """Changes mushroom direction if collision along x axis"""
        if item.rect.x < collider.rect.x:
            item.rect.right = collider.rect.x
            item.direction = c.LEFT
        else:
            item.rect.x = collider.rect.right
            item.direction = c.RIGHT


    def adjust_mushroom_for_collision_y(self, item, collider):
        """Changes mushroom state to SLIDE after hitting ground from fall"""
        item.rect.bottom = collider.rect.y
        item.state = c.SLIDE
        item.y_vel = 0


    def adjust_star_position(self, star):
        """Moves invincible star along x, y axes and checks for collisions"""
        if star.state == c.BOUNCE:
            star.rect.x += star.x_vel
            self.check_mushroom_x_collisions(star)
            star.rect.y += star.y_vel
            self.check_star_y_collisions(star)
            star.y_vel += star.gravity
            self.delete_if_off_screen(star)


    def check_star_y_collisions(self, star):
        """Invincible star collisions along y axis"""
        collider = pg.sprite.spritecollideany(star, self.ground_step_pipe_group)
        brick = pg.sprite.spritecollideany(star, self.brick_group)
        coin_box = pg.sprite.spritecollideany(star, self.coin_box_group)

        if collider:
            self.adjust_star_for_collision_y(star, collider)
        elif brick:
            self.adjust_star_for_collision_y(star, brick)
        elif coin_box:
            self.adjust_star_for_collision_y(star, coin_box)


    def adjust_star_for_collision_y(self, star, collider):
        """Allows for a star bounce off the ground and on the bottom of a
        box"""
        if star.rect.y > collider.rect.y:
            star.rect.y = collider.rect.bottom
            star.y_vel = 0
        else:
            star.rect.bottom = collider.rect.top
            star.start_bounce(-8)


    def adjust_fireball_position(self, fireball):
        """Moves fireball along the x, y axes and checks for collisions"""
        if fireball.state == c.FLYING:
            fireball.rect.x += fireball.x_vel
            self.check_fireball_x_collisions(fireball)
            fireball.rect.y += fireball.y_vel
            self.check_fireball_y_collisions(fireball)
        elif fireball.state == c.BOUNCING:
            fireball.rect.x += fireball.x_vel
            self.check_fireball_x_collisions(fireball)
            fireball.rect.y += fireball.y_vel
            self.check_fireball_y_collisions(fireball)
            fireball.y_vel += fireball.gravity
        self.delete_if_off_screen(fireball)


    def bounce_fireball(self, fireball):
        """Simulates fireball bounce off ground"""
        fireball.y_vel = -8
        if fireball.direction == c.RIGHT:
            fireball.x_vel = 15
        else:
            fireball.x_vel = -15

        if fireball in self.powerup_group:
            fireball.state = c.BOUNCING


    def check_fireball_x_collisions(self, fireball):
        """Fireball collisions along x axis"""
        collide_group = pg.sprite.Group(self.ground_group,
                                        self.pipe_group,
                                        self.step_group,
                                        self.coin_box_group,
                                        self.brick_group)

        collider = pg.sprite.spritecollideany(fireball, collide_group)

        if collider:
            fireball.kill()
            self.sprites_about_to_die_group.add(fireball)
            fireball.explode_transition()



    def check_fireball_y_collisions(self, fireball):
        """Fireball collisions along y axis"""
        collide_group = pg.sprite.Group(self.ground_group,
                                        self.pipe_group,
                                        self.step_group,
                                        self.coin_box_group,
                                        self.brick_group)

        collider = pg.sprite.spritecollideany(fireball, collide_group)
        enemy = pg.sprite.spritecollideany(fireball, self.enemy_group)
        shell = pg.sprite.spritecollideany(fireball, self.shell_group)

        if collider and (fireball in self.powerup_group):
            fireball.rect.bottom = collider.rect.y
            self.bounce_fireball(fireball)

        elif enemy:
            self.fireball_kill(fireball, enemy)

        elif shell:
            self.fireball_kill(fireball, shell)


    def fireball_kill(self, fireball, enemy):
        """Kills enemy if hit with fireball"""
        setup.SFX['kick'].play()
        self.game_info[c.SCORE] += 100
        self.moving_score_list.append(
            score.Score(enemy.rect.centerx - self.viewport.x,
                        enemy.rect.y,100))
        fireball.kill()
        enemy.kill()
        self.sprites_about_to_die_group.add(enemy, fireball)
        enemy.start_death_jump(fireball.direction)
        fireball.explode_transition()


    def check_if_falling(self, sprite, sprite_group):
        """Checks if sprite should enter a falling state"""
        sprite.rect.y += 1

        if pg.sprite.spritecollideany(sprite, sprite_group) is None:
            if sprite.state != c.JUMP:
                sprite.state = c.FALL

        sprite.rect.y -= 1


    def delete_if_off_screen(self, enemy):
        """Removes enemy from sprite groups if 500 pixels left off the screen,
         underneath the bottom of the screen, or right of the screen if shell"""
        if enemy.rect.x < (self.viewport.x - 300):
            enemy.kill()

        elif enemy.rect.y > (self.viewport.bottom):
            enemy.kill()

        elif enemy.state == c.SHELL_SLIDE:
            if enemy.rect.x > (self.viewport.right + 500):
                enemy.kill()


    def check_flag(self):
        """Adjusts mario's state when the flag is at the bottom"""
        if (self.flag.state == c.BOTTOM_OF_POLE
            and self.mario.state == c.FLAGPOLE):
            self.mario.set_state_to_bottom_of_pole()


    def check_to_add_flag_score(self):
        """Adds flag score if at top"""
        if self.flag_score.y_vel == 0:
            self.game_info[c.SCORE] += self.flag_score_total
            self.flag_score_total = 0


    def check_for_mario_death(self):
        """Restarts the level if Mario is dead"""
        if self.mario.rect.y > c.SCREEN_HEIGHT and not self.mario.in_castle:
            self.mario.dead = True
            self.mario.x_vel = 0
            self.state = c.FROZEN
            self.game_info[c.MARIO_DEAD] = True

        if self.mario.dead:
            self.play_death_song()


    def play_death_song(self):
        if self.death_timer == 0:
            self.death_timer = self.current_time
        elif (self.current_time - self.death_timer) > 3000:
            self.set_game_info_values()
            self.done = True


    def set_game_info_values(self):
        """sets the new game values after a player's death"""
        if self.game_info[c.SCORE] > self.persist[c.TOP_SCORE]:
            self.persist[c.TOP_SCORE] = self.game_info[c.SCORE]
        if self.mario.dead:
            self.persist[c.LIVES] -= 1

        if self.persist[c.LIVES] == 0:
            self.next = c.GAME_OVER
            self.game_info[c.CAMERA_START_X] = 0
        elif self.mario.dead == False:
            if self.state == c.LEVEL2:
                self.next = c.LEVEL2
            self.game_info[c.CAMERA_START_X] = 0
        elif self.overhead_info_display.time == 0:
            self.next = c.TIME_OUT
        else:
            if self.mario.rect.x > 3670 \
                    and self.game_info[c.CAMERA_START_X] == 0:
                self.game_info[c.CAMERA_START_X] = 3440
            self.next = c.LOAD_SCREEN


    def check_if_time_out(self):
        """Check if time has run down to 0"""
        if self.overhead_info_display.time <= 0 \
                and not self.mario.dead \
                and not self.mario.in_castle:
            self.state = c.FROZEN
            self.mario.start_death_jump(self.game_info)


    def update_viewport(self):
        """Changes the view of the camera"""
        third = self.viewport.x + self.viewport.w//3
        mario_center = self.mario.rect.centerx
        mario_right = self.mario.rect.right

        if self.mario.x_vel > 0 and mario_center >= third:
            mult = 0.5 if mario_right < self.viewport.centerx else 1
            new = self.viewport.x + mult * self.mario.x_vel
            highest = self.level_rect.w - self.viewport.w
            self.viewport.x = min(highest, new)


    def update_while_in_castle(self):
        """Updates while Mario is in castle at the end of the level"""
        for score in self.moving_score_list:
            score.update(self.moving_score_list, self.game_info)
        self.overhead_info_display.update(self.game_info)

        if self.overhead_info_display.state == c.END_OF_LEVEL:
            self.state = c.FLAG_AND_FIREWORKS
            self.flag_pole_group.add(castle_flag.Flag(8045, 322))


    def update_flag_and_fireworks(self):
        """Updates the level for the fireworks and castle flag"""
        for score in self.moving_score_list:
            score.update(self.moving_score_list, self.game_info)
        self.overhead_info_display.update(self.game_info)
        self.flag_pole_group.update()

        self.end_game()


    def end_game(self):
        """End the game"""
        if self.flag_timer == 0:
            self.flag_timer = self.current_time
        elif (self.current_time - self.flag_timer) > 2000:
            self.set_game_info_values()
            self.next = c.GAME_OVER
            self.sound_manager.stop_music()
            self.done = True


    def blit_everything(self, surface):
        """Blit all sprites to the main surface"""
        self.level.blit(self.background, self.viewport, self.viewport)
        if self.flag_score:
            self.flag_score.draw(self.level)
        self.powerup_group.draw(self.level)
        self.coin_group.draw(self.level)
        self.brick_group.draw(self.level)
        self.coin_box_group.draw(self.level)
        self.sprites_about_to_die_group.draw(self.level)
        self.shell_group.draw(self.level)
        #self.check_point_group.draw(self.level)
        self.brick_pieces_group.draw(self.level)
        self.flag_pole_group.draw(self.level)
        self.elevator_group.draw(self.level)
        self.mario_and_enemy_group.draw(self.level)

        surface.blit(self.level, (0,0), self.viewport)
        self.overhead_info_display.draw(surface)
        for score in self.moving_score_list:
            score.draw(surface)


