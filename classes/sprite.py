import pygame  # Import PyGame


class Sprite:
    """ Gestion des sprites et de ses animations """

    def __init__(self):
        self.sprite_selected = pygame.image.load('ressources/sprites/characters/goku.png').convert_alpha()
        # Direction => Marche 1 | Marche 2 | Arret
        self.direction = {'Down': [[0, 0], [2, 0], [1, 0]], 'Up': [[0, 3], [2, 3], [1, 3]],
                          'Left': [[0, 1], [2, 1], [1, 1]], 'Right': [[0, 2], [2, 2], [1, 2]]}
        self.current_position = 1  # Direction de marche par défaut

    def select_sprite(self, ligne, colonne, pixel_ligne=32, pixel_colonne=35):
        """ Selectionne une case du sprite """
        return self.sprite_selected.subsurface(pixel_ligne * ligne, pixel_colonne * colonne, pixel_ligne, pixel_colonne)

    def animate_sprite(self, move, old_pos_sprite):
        """ Animation de marche du personnage """
        # Sprite par défaut
        new_img_sprite = self.select_sprite(self.direction[old_pos_sprite][2][0], self.direction[old_pos_sprite][2][1])

        # Cas où le déplacement n'est pas demandé
        if move is not None:
            for i in {'Down', 'Up', 'Left', 'Right'}:  # Liste des possibilités de déplacement
                if move == i:
                    if self.current_position == 1:  # Premier Sprite de marche
                        new_img_sprite = self.select_sprite(self.direction[i][0][0], self.direction[i][0][1])
                        self.current_position = 2  # Met à jour la valeur de marche
                    elif self.current_position == 2:  # Deuxième Sprite de marche
                        self.current_position = 1  # Met à jour la valeur de marche
                        new_img_sprite = self.select_sprite(self.direction[i][1][0], self.direction[i][1][1])

        return new_img_sprite  # Retourne le nouveau Sprite
