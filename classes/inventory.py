import os      # Import OS
import sys     # Import SYS
import pygame  # Import PyGame

sys.path.append(os.getcwd() + "/classes")  # Ajout du chemin pour éviter les bugs Windows
from niveau import *  # Import de la class Niveau et des composantes liées


class Inventory:
    """ Gestion de l'inventaire du personnage """

    def __init__(self, screen, font_police="ressources/fonts/BebasNeue.ttf", font_size=24):
        self.screen = screen  # Récupère l'écran sur lequel il faut dessiner
        self.font = pygame.font.Font(font_police, font_size)

    def show_item(self):
        """ Affiche les items du joueur en haut de l'écran """
        y = 40
        if Niveau.INVENTORY:  # Dans le cas où l'inventaire n'est pas vide
            for i in range(6):
                if len(Niveau.INVENTORY) > i:
                    self.screen.blit(self.font.render("Inventaire :", 1, (0, 0, 0)), (10, 10))  # Affiche le texte de l'inventaire
                    self.screen.blit(pygame.image.load('ressources/images/items/' + Niveau.INVENTORY[i] + '.png').convert_alpha(), (35, y))
                    y = y+44
