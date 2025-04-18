import pygame


class Player:
    """ Player management """

    def __init__(self, tilemap, width, height, img_character, old_pos_sprite):
        self.tilemap = tilemap

        if old_pos_sprite == 'up':
            self.sprite_player = img_character.select_sprite(1, 3)
        elif old_pos_sprite == 'left':
            self.sprite_player = img_character.select_sprite(1, 1)
        elif old_pos_sprite == 'right':
            self.sprite_player = img_character.select_sprite(1, 2)
        else:
            self.sprite_player = img_character.select_sprite(1, 0)

        player_pos = self.tilemap.layers['evenements'].find('player')[0]
        self.player = pygame.rect.Rect((player_pos.px, player_pos.py), self.sprite_player.get_size())

        self.half_width = width / 2
        self.half_height = height / 2
        self.y = self.half_height
        self.x = self.half_width
