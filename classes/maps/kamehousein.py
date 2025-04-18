import os
import sys
from math import ceil

sys.path.append(os.getcwd() + "/libs")
import tmx

sys.path.append(os.getcwd() + "/classes")
from player import *
from sprite import *
from move import *
from niveau import *
from interact import *
from inventory import *
from escapemenu import *

sys.path.append(os.getcwd() + "/ressources")
from missions import *


class KamehouseIn:
    """ Management related to the interior of the Kamehouse map """

    def __init__(self, width, height, screen, clock, fps, move_speed):
        """ Gets important variables from the Game class """
        self.width = width
        self.height = height
        self.screen = screen
        self.fps = fps
        self.clock = clock
        self.move_speed = move_speed
        self.sound = None

        self.while_map_kamehouse = False

        self.while_map_kamehouse_in = True

    def while_kamehouse_in(self, sound=None):
        """ Loop on the KamehouseIn map """
        self.sound = sound
        tilemap = tmx.load('ressources/maps/kamehouse/house/map.tmx', self.screen.get_size())
        collision_total = tilemap.layers['evenements'].find('collision')
        exit_lvl = tilemap.layers['evenements'].find('exit')
        collision_tortue = tilemap.layers['evenements'].find('collision_tortue')

        move_direction = None
        old_pos_sprite = 'Up'
        character_img = Sprite()

        if Niveau.SPRITE_TYPE != 0:
            character_img.change_sprite(Niveau.SPRITE_TYPE)

        player = Player(tilemap, self.width, self.height, character_img, old_pos_sprite)
        movement = Move(player, self.move_speed, collision_total)
        dialogue = Interact(self.screen)
        inventory = Inventory(self.screen)
        escape_menu = EscapeMenu(self.screen, self.sound)
        pygame.time.set_timer(pygame.USEREVENT, 300)

        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        while self.while_map_kamehouse_in:
            collide_exit = CollisionController(player, exit_lvl)
            collide_tortue = CollisionController(player, collision_tortue)

            if collide_exit.collision():
                self.while_map_kamehouse_in = False
                self.while_map_kamehouse = True
                Niveau.LVL = 'while_map_kamehouse'

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.while_map_kamehouse_in = False
                    Niveau.WHILE_GAME = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    escape_menu.toggle()
                elif event.type == pygame.USEREVENT:
                    player.sprite_player = character_img.animate_sprite(move_direction, old_pos_sprite)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and collide_tortue.collision() and not Niveau.DIALOGUE:

                    Niveau.DIALOGUE = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and Niveau.DIALOGUE:

                    if Niveau.MISSION_01 == 0:
                        calcul = ceil(len(txt_mission01_01) / 4)
                    elif Niveau.MISSION_01 == 50:
                        calcul = ceil(len(txt_mission01_03) / 4)
                    elif Niveau.MISSION_01 == 100:
                        calcul = ceil(len(txt_mission01_04) / 4)

                    if Niveau.PAGE == calcul:
                        Niveau.DIALOGUE = False
                        Niveau.PAGE = 1

                        if Niveau.MISSION_01 == 50:
                            Niveau.MISSION_01 = 100
                            Niveau.INVENTORY.remove('boulecristal')
                    else:
                        Niveau.PAGE = Niveau.PAGE + 1

                sprite_choice = escape_menu.handle_event(event)
                if sprite_choice is not None:
                    character_img.change_sprite(sprite_choice)
                    player.sprite_player = character_img.select_sprite(1, 0)

                    Niveau.SPRITE_TYPE = sprite_choice

            if escape_menu.menu_active:
                escape_menu.update_hover_state()

            if not Niveau.DIALOGUE and not escape_menu.menu_active:

                sprint_multiplier = 3.0 if pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[
                    pygame.K_RSHIFT] else 1.0
                speed = self.move_speed * sprint_multiplier

                if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:

                    movement_direction = 'Down'
                    if move_direction is None or move_direction != movement_direction:
                        player.sprite_player = character_img.select_sprite(1, 0)
                        move_direction = movement_direction
                    if Move.COLLIDED: move_direction = None
                    old_pos_sprite = movement_direction
                    movement.move_player(player.player.copy(), [0, speed], movement_direction)

                elif pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_z]:
                    movement_direction = 'Up'
                    if move_direction is None or move_direction != movement_direction:
                        player.sprite_player = character_img.select_sprite(1, 3)
                        move_direction = movement_direction
                    if Move.COLLIDED: move_direction = None
                    old_pos_sprite = movement_direction
                    movement.move_player(player.player.copy(), [0, -speed], movement_direction)

                elif pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_q]:
                    movement_direction = 'Left'
                    if move_direction is None or move_direction != movement_direction:
                        player.sprite_player = character_img.select_sprite(1, 1)
                        move_direction = movement_direction
                    if Move.COLLIDED: move_direction = None
                    old_pos_sprite = movement_direction
                    movement.move_player(player.player.copy(), [-speed, 0], movement_direction)

                elif pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
                    movement_direction = 'Right'
                    if move_direction is None or move_direction != movement_direction:
                        player.sprite_player = character_img.select_sprite(1, 2)
                        move_direction = movement_direction
                    if Move.COLLIDED: move_direction = None
                    old_pos_sprite = movement_direction
                    movement.move_player(player.player.copy(), [speed, 0], movement_direction)
                else:
                    move_direction = None
            else:
                move_direction = None

            self.clock.tick(self.fps)
            tilemap.set_focus(player.player.x, player.player.y)
            tilemap.draw(self.screen)
            self.screen.blit(player.sprite_player, (player.x, player.y))

            if Niveau.DIALOGUE:
                if Niveau.MISSION_01 == 0:
                    dialogue.show_box(txt_mission01_01)
                elif Niveau.MISSION_01 == 50:
                    dialogue.show_box(txt_mission01_03)
                elif Niveau.MISSION_01 == 100:
                    dialogue.show_box(txt_mission01_04)

            if Niveau.INVENTORY:
                inventory.show_item()

            escape_menu.draw()

            pygame.display.flip()
