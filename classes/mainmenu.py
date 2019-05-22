import os      # Import OS
import sys     # Import SYS
import pygame  # Import PyGame
import pygame.gfxdraw

sys.path.append(os.getcwd() + "/classes")  # Ajout du chemin pour éviter les bugs Windows
from niveau import Niveau  # Import de la class Niveau


class MainMenu:
    """ Menu de lancement du jeu """

    def __init__(self, screen, clock, fps, son):
        """ Récupère les variables importantes """
        self.screen = screen  # Récupère le screen de la class Game
        self.fps = fps  # Récupère les fps de la class FPS
        self.clock = clock  # Récupère la limitation d'FPS de la class Game
        self.son = son  # Récupère le son du jeu

        self.son_menu = pygame.mixer.Sound("ressources/sounds/Menu.wav")  # Défini le son du menu
        self.son_menu.play(loops=-1, maxtime=0, fade_ms=0)  # Lance la boucle de son à l'infini
        self.son_menu.set_volume(0.3)  # Permet de diminuer le son par défaut du jeu

        self.while_map_kamehouse = False  # N'appelle par défaut pas la boucle de cette route
        self.while_options = False  # N'appelle par défaut pas la boucle sur cette route

        self.while_main_menu = True  # Boucle sur le menu affiché à l'utilisateur

    def while_menu(self):
        """ Boucle sur le menu de démarrage """
        self.screen.blit(pygame.image.load('ressources/images/background_menu.png').convert_alpha(), (0, 0))  # Récupère le fond du menu

        font = pygame.font.Font("ressources/fonts/BebasNeue.ttf", 26)  # Défini la police d'écriture du menu
        volume = 'OFF'  # Permet de gérer l'activation ou non du volume

        rect_global = pygame.rect.Rect(80, 180, 328, 185)  # Défini le rectangle du bouton
        pygame.gfxdraw.box(self.screen, rect_global, (255, 255, 255, 220))  # Défini le rectangle son_rect sans survol

        lancer_rect = pygame.rect.Rect(100, 200, 275, 60)  # Défini le rectangle du bouton
        ombre_lancer = pygame.rect.Rect(108, 205, 280, 65)  # Défini le rectangle du bouton
        pygame.gfxdraw.box(self.screen, ombre_lancer, (0, 0, 204, 255))  # Défini le rectangle de l'ombre_lancer sans survol
        lancer_text = font.render('Lancer le jeu', 1, (255, 255, 255))  # Défini le texte du bouton

        son_rect = pygame.rect.Rect(100, 275, 275, 60)  # Défini le rectangle du bouton
        ombre_musique = pygame.rect.Rect(108, 280, 280, 65)  # Défini le rectangle de l'ombre_musique
        pygame.gfxdraw.box(self.screen, ombre_musique, (0, 0, 204, 255))  # Défini le rectangle ombre_musique sans survol

        while self.while_main_menu:  # Boucle infinie du menu
            pygame.gfxdraw.box(self.screen, lancer_rect, (51, 153, 255, 255))  # Défini le rectangle lancer_rect sans survol
            pygame.gfxdraw.box(self.screen, son_rect, (51, 153, 255, 255))  # Défini le rectangle son_rect sans survol

            for event in pygame.event.get():      # Vérifie toutes les actions du joueur
                if event.type == pygame.QUIT:     # Clique pour quitter le jeu
                    self.while_main_menu = False  # Quitte le processus python
                    Niveau.WHILE_GAME = False     # Ferme la boucle d'importation

                if son_rect.collidepoint(pygame.mouse.get_pos()):  # Touche le bouton de son
                    survol = 'son'  # Survol le bouton lié au son
                    if event.type == pygame.MOUSEBUTTONUP: # Clique gauche avec la souris
                        if volume == 'ON':  # Cas où le son veut être à ON
                            self.son.set_volume(0.3)  # Permet de diminuer le son par défaut du jeu
                            self.son_menu.set_volume(0.3)  # Permet de diminuer le son par défaut du jeu
                            volume = 'OFF'  # Défini la prochaine action avec le son à OFF
                        else:  # Le son veut être désactivé
                            self.son.set_volume(0.0)  # Permet de diminuer le son par défaut du jeu
                            self.son_menu.set_volume(0.0)
                            volume = 'ON'  # Défini la prochaine action avec le son à ON
                elif lancer_rect.collidepoint(pygame.mouse.get_pos()):  # Touche le bouton de lancement
                    survol = 'lancer'  # Survol le bouton lié au lancement du jeu
                    if event.type == pygame.MOUSEBUTTONUP:  # Clique gauche avec la souris
                        self.son_menu.stop()  # Arrête la musique du menu
                        self.son.play(loops=-1, maxtime=0, fade_ms=0)  # Lance la boucle de son à l'infini
                        self.while_main_menu = False  # Arrête la boucle du menu
                        self.while_map_kamehouse = True  # Permet de lancer la boucle sur la map choisie
                        Niveau.LVL = 'while_map_kamehouse'  # Permet de lancer la nouvelle carte
                else:  # Aucun survol
                    survol = None

            if survol == 'son':  # Bouton survolé est le "son"
                pygame.gfxdraw.box(self.screen, son_rect,  (0, 128, 255, 255))  # Défini la couleur du rectangle son_rect survolé
            elif survol == 'lancer':  # Bouton survolé est le "lancement"
                pygame.gfxdraw.box(self.screen, lancer_rect,  (0, 128, 255, 255))  # Défini la couleur du rectangle lancer_rect survolé

            if volume == 'ON':  # Volume souhaité est à ON
                son_text = font.render('Activer la musique', 1, (255, 255, 255))  # Défini le texte du bouton
                son_coord = (155, 290)  # Coordonnée de l'affichage du texte
            else:  # Le prochain clique désactivera la musique
                son_text = font.render('Désactiver la musique', 1, (255, 255, 255))  # Défini le texte du bouton
                son_coord = (145, 290)  # Coordonnée de l'affichage du texte

            self.screen.blit(lancer_text, (180, 215))  # Affiche le texte sur le bouton lancer_rect
            self.screen.blit(son_text, son_coord)  # Affiche le texte sur le bouton son_rect
            self.clock.tick(self.fps)  # Restreint les FPS
            pygame.display.flip()      # Mets à jour l'affichage
