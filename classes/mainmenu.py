import os      # Import OS
import sys     # Import SYS
import pygame  # Import PyGame

sys.path.append(os.getcwd() + "/libs")  # Ajout du chemin pour éviter les bugs Windows
import tmx  # Libraire TMX (bypass pour Python 2)

sys.path.append(os.getcwd() + "/classes")  # Ajout du chemin pour éviter les bugs Windows
from niveau import Niveau  # Import de la class Niveau


class MainMenu:
    """ Menu de lancement du jeu """

    def __init__(self, screen, clock, fps):
        """ Récupère les variables importantes """
        self.screen = screen  # Récupère le screen de la class Game
        self.fps = fps  # Récupère les fps de la class FPS
        self.clock = clock  # Récupère la limitation d'FPS de la class Game

        self.while_map_kamehouse = False  # N'appelle par défaut pas la boucle de cette route
        self.while_options = False  # N'appelle par défaut pas la boucle sur cette route

        self.while_main_menu = True  # Boucle sur le menu affiché à l'utilisateur

    def while_menu(self):
        """ Boucle sur le menu de démarrage """
        tilemap = tmx.load('ressources/maps/kamehouse/island/map.tmx', self.screen.get_size())  # Import de la map
        tilemap.set_focus(0, 0)  # Coordonnées du joueur par rapport aux bords

        while self.while_main_menu:  # Boucle infinie du menu
            for event in pygame.event.get():      # Vérifie toutes les actions du joueur
                if event.type == pygame.QUIT:     # Clique pour quitter le jeu
                    self.while_main_menu = False  # Quitte le processus python
                    Niveau.WHILE_GAME = False     # Ferme la boucle d'importation

            if pygame.key.get_pressed()[pygame.K_DOWN]:  # La touche du bas est pressée pour changer de fenêtre
                self.while_main_menu = False     # Arrête la boucle du menu
                self.while_map_kamehouse = True  # Permet de lancer la boucle sur la map choisie
                Niveau.LVL = 'while_map_kamehouse'

            self.clock.tick(self.fps)  # Restreint les FPS
            tilemap.draw(self.screen)  # Affiche le fond
            pygame.display.flip()      # Mets à jour l'affichage