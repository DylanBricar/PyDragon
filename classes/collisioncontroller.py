class CollisionController:
    """ Collision management """

    def __init__(self, player, total_collision):
        self.total_collision = total_collision
        self.player = player

    def collision(self):
        """ Detects collisions """
        return any(((self.player.player.x < collision_selected.px + collision_selected.width)
                    and (self.player.player.x + self.player.player.w > collision_selected.px)
                    and (self.player.player.y < collision_selected.py + collision_selected.height)
                    and (self.player.player.y + self.player.player.h > collision_selected.py))
                   for collision_selected in self.total_collision)
