class CollisionController:
    """ Gestion des collisions """

    def __init__(self, player, total_collision):
        self.total_collision = total_collision  # Liste avec toutes les collisions de la map
        self.player = player  # Globalité de la class du joueur

    def collision(self):
        """ Repère les collisions """
        # Retourne False ou True si une collision a été ou non trouvée
        return any(((self.player.player.x < collision_selected.px + collision_selected.width)       # Trop à droite
                    and (self.player.player.x + self.player.player.w > collision_selected.px)       # Trop à gauche
                    and (self.player.player.y < collision_selected.py + collision_selected.height)  # Trop en bas
                    and (self.player.player.y + self.player.player.h > collision_selected.py))      # Trop en haut
                   for collision_selected in self.total_collision)  # Boucle les collisions
