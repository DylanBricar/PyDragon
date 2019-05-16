import pygame  # Import PyGame


class Player:
    """ Gestion du joueur """

    def __init__(self, tilemap, width, height, img_perso, old_pos_sprite):
        self.tilemap = tilemap  # Récupère la map

        # Récupère la position du joueur pour afficher le sprite par défaut
        if old_pos_sprite == 'up':
            self.sprite_player = img_perso.select_sprite(1, 3)  # Génère le sprite de base
        elif old_pos_sprite == 'left':
            self.sprite_player = img_perso.select_sprite(1, 1)  # Génère le sprite de base
        elif old_pos_sprite == 'right':
            self.sprite_player = img_perso.select_sprite(1, 2)  # Génère le sprite de base
        else:
            self.sprite_player = img_perso.select_sprite(1, 0)  # Génère le sprite de base

        joueur_pos = self.tilemap.layers['evenements'].find('player')[0]  # Trouve le joueur depuis la map
        self.player = pygame.rect.Rect((joueur_pos.px, joueur_pos.py), self.sprite_player.get_size())  # Crée son rectangle

        self.div_x_map = width/2   # Taille de la map en longueur divisée en deux
        self.div_y_map = height/2  # Taille de la map en largeur divisée en deux
        self.y = self.div_y_map    # Utilisé pour positionner le joueur (au centre vertical par défaut)
        self.x = self.div_x_map    # Utilisé pour positionner le joueur (au centre horizontal par défaut)
