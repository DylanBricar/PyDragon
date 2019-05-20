import os      # Import OS
import sys     # Import SYS

sys.path.append(os.getcwd() + "/classes")  # Ajout du chemin pour éviter les bugs Windows
from collisioncontroller import CollisionController  # Import de la class CollisionController


class Move:
    """ Déplacement du joueur """

    COLLIDED = False  # Entre en collision (permet de stopper le sprite)

    def __init__(self, player, pas, collision):
        self.player = player  # Toutes les informations de la class player
        self.pas = pas  # Déplacement qui doit être fait
        self.collision = collision  # Liste de toutes les collisions

        # Bords de la map
        self.bord_haut = self.player.div_y_map
        self.bord_bas = self.player.tilemap.px_height - self.player.div_y_map
        self.bord_gauche = self.player.div_x_map
        self.bord_droit = self.player.tilemap.px_width - self.player.div_x_map

    def move_player(self, old_position, direction, touche):
        """ Déplace le joueur en fonction de la touche """
        self.player.player.move_ip(direction)  # Déplace le joueur en y ajoutant la direction donnée
        collide = CollisionController(self.player, self.collision)  # Appelle la class de collision

        if collide.collision():  # Si collision, on restaure la position de départ
            self.player.player = old_position
            Move.COLLIDED = True  # Change la variable permettant de stopper le sprite
        else:
            Move.COLLIDED = False  # Change la variable permettant d'animer le sprite
            # Aucune collision de trouvée : on ajuste le rendu de l'écran
            if touche == 'Left':
                if self.bord_droit >= self.player.player.x >= self.bord_gauche:
                    self.player.x = self.player.div_x_map  # Le joueur est centré sur la map
                # Le joueur se trouve proche d'une des deux extrémités de la map
                elif self.player.player.x <= self.bord_gauche or self.player.player.x >= self.bord_droit:
                    self.player.x -= self.pas  # Le joueur se rapproche du bord
            elif touche == 'Right':
                if self.player.player.x < self.bord_gauche or self.player.player.x > self.bord_droit:
                    self.player.x += self.pas
                elif self.bord_gauche > self.player.player.x > self.bord_droit:
                    self.player.x = self.player.div_x_map
            elif touche == 'Up':
                if self.player.player.y <= self.bord_haut or self.player.player.y >= self.bord_bas:
                    self.player.y -= self.pas
                elif self.bord_bas > self.player.player.y > self.bord_haut:
                    self.player.y = self.player.div_y_map
            elif touche == 'Down':
                if self.bord_haut > self.player.player.y > self.bord_bas:
                    self.player.y = self.player.div_y_map
                elif self.player.player.y <= self.bord_haut or self.player.player.y >= self.bord_bas:
                    self.player.y += self.pas
