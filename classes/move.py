import sys
from pathlib import Path

base_path = Path(__file__).parent.absolute()
sys.path.append(str(base_path))

from collisioncontroller import CollisionController


class Move:
    """ Player movement """

    COLLIDED = False

    def __init__(self, player, step, collision):
        self.player = player
        self.step = step
        self.collision = collision

        self.top_border = self.player.half_height
        self.bottom_border = self.player.tilemap.px_height - self.player.half_height
        self.left_border = self.player.half_width
        self.right_border = self.player.tilemap.px_width - self.player.half_width

    def move_player(self, old_position, direction, key):
        """ Move player based on key pressed """
        self.player.player.move_ip(direction)
        collide = CollisionController(self.player, self.collision)

        if collide.collision():
            self.player.player = old_position
            Move.COLLIDED = True
        else:
            Move.COLLIDED = False
            if key == 'Left':
                if self.right_border >= self.player.player.x >= self.left_border:
                    self.player.x = self.player.half_width
                elif self.player.player.x <= self.left_border or self.player.player.x >= self.right_border:
                    self.player.x -= self.step
            elif key == 'Right':
                if self.player.player.x < self.left_border or self.player.player.x > self.right_border:
                    self.player.x += self.step
                elif self.left_border > self.player.player.x > self.right_border:
                    self.player.x = self.player.half_width
            elif key == 'Up':
                if self.player.player.y <= self.top_border or self.player.player.y >= self.bottom_border:
                    self.player.y -= self.step
                elif self.bottom_border > self.player.player.y > self.top_border:
                    self.player.y = self.player.half_height
            elif key == 'Down':
                if self.top_border > self.player.player.y > self.bottom_border:
                    self.player.y = self.player.half_height
                elif self.player.player.y <= self.top_border or self.player.player.y >= self.bottom_border:
                    self.player.y += self.step
