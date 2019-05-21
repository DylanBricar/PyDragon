import os      # Import OS
import sys     # Import SYS
import pygame  # Import PyGame

sys.path.append(os.getcwd() + "/classes")  # Ajout du chemin pour éviter les bugs Windows
from niveau import *  # Import de la class Niveau et des composantes liées


class Interact:
    """ Gestion des interactions entre les personnages """

    def __init__(self, screen, font_police="ressources/fonts/BebasNeue.ttf", font_size=24):
        self.screen = screen  # Récupère l'écran sur lequel il faut dessiner
        self.font = pygame.font.Font(font_police, font_size)

    def show_box(self, text):
        """ Affiche la boite de message ainsi que la personne qui dit le message """

        dialogue_bg = pygame.image.load('ressources/images/dialogue.png').convert_alpha()  # Récupère le canvas
        self.screen.blit(dialogue_bg, (0, 0))  # Affiche le canvas

        y = 390  # Distance d'écriture
        for i in range((Niveau.PAGE*4)-4, Niveau.PAGE*4):  # Parcours toutes les lignes de text par 4
            if len(text) > i:  # Si on ne recherche pas des données innexistantes dans le tableau
                cuted = text[i].split(" | ")  # Coupe le texte pour récupérer la personne qui parle

                if len(cuted) == 2:  # S'il existe une information sur la personne qui parle
                    # Récupère l'avatar et affiche l'avatar
                    avatar_img = pygame.image.load('ressources/images/avatars/avatar_' + text[i].split(" | ")[1] + '.png').convert_alpha()
                    self.screen.blit(avatar_img, (0, 231))

                self.screen.blit(self.font.render(cuted[0], 1, (0, 0, 0)), (60, y))  # Affiche chacune des lignes de texte
                y = y+25  # Ajoute 25px comme saut de ligne
