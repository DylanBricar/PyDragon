import os
import sys

sys.path.append(os.getcwd() + "/libs")
import tmx

sys.path.append(os.getcwd() + "/classes")
from player import *
from sprite import *
from move import *
from niveau import *
from inventory import *
from escapemenu import *
from settings import *


class WorldTown:
    """ Management related to the exterior of the WorldTown map """

    def __init__(self, width, height, screen, clock, fps, move_speed):
        """ Gets important variables from the Game class """
        self.width = width
        self.height = height
        self.screen = screen
        self.fps = fps
        self.clock = clock
        self.move_speed = move_speed
        self.sound = None
        self.while_map_town = True
        self.while_map_kamehouse = False
        self.while_map_town_in = False

        if SHOW_FPS:
            self.fps_font = pygame.font.SysFont('Arial', 16)

    def while_town(self, sound=None):
        """ Loop on the WorldTown map """
        self.sound = sound
        tilemap = tmx.load('ressources/maps/worldtown/world/map.tmx', self.screen.get_size())
        collision_total = tilemap.layers['evenements'].find('collision')

        exit_lvl = tilemap.layers['evenements'].find('exit')
        goto_kamehouse = tilemap.layers['evenements'].find('exit_gotokamehouse')

        move_direction = None
        old_pos_sprite = 'Down'
        character_img = Sprite()

        if Niveau.SPRITE_TYPE != 0:
            character_img.change_sprite(Niveau.SPRITE_TYPE)

        player = Player(tilemap, self.width, self.height, character_img, old_pos_sprite)
        movement = Move(player, self.move_speed, collision_total)
        inventory = Inventory(self.screen)
        escape_menu = EscapeMenu(self.screen, self.sound)
        pygame.time.set_timer(pygame.USEREVENT, 300)

        if Niveau.COORDINATES_TOWN:
            player.player.x = Niveau.COORDINATES_TOWN[0]
            player.player.y = Niveau.COORDINATES_TOWN[1]

        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        while self.while_map_town:
            collide_exit = CollisionController(player, exit_lvl)
            if collide_exit.collision():
                self.while_map_town = False
                self.while_map_town_in = True
                Niveau.LVL = 'while_map_town_in'
                Niveau.COORDINATES_TOWN = [1250, 1700]

            collide_goto_world = CollisionController(player, goto_kamehouse)
            if collide_goto_world.collision():
                self.while_map_town = False
                self.while_map_kamehouse = True
                Niveau.LVL = 'while_map_kamehouse'
                Niveau.COORDINATES_TOWN = []

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.while_map_town = False
                    Niveau.WHILE_GAME = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    escape_menu.toggle()
                elif event.type == pygame.USEREVENT:
                    player.sprite_player = character_img.animate_sprite(move_direction, old_pos_sprite)

                sprite_choice = escape_menu.handle_event(event)
                if sprite_choice is not None:
                    character_img.change_sprite(sprite_choice)
                    player.sprite_player = character_img.select_sprite(1, 0)

                    Niveau.SPRITE_TYPE = sprite_choice

            if escape_menu.menu_active:
                escape_menu.update_hover_state()

            if not escape_menu.menu_active:
                sprint_multiplier = 3.0 if pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[
                    pygame.K_RSHIFT] else 1.0

                speed = self.move_speed * sprint_multiplier * SPEED_ADJUSTMENT

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

            if Niveau.INVENTORY:
                inventory.show_item()

            escape_menu.draw()

            pygame.display.flip()
