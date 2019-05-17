import pygame
from niveau import *

class Interact:
    """ Gestion des interactions """

    def __init__(self, screen, text):
        self.screen = screen
        self.text = text

        for event in pygame.event.get():  # Vérifie toutes les actions du joueur
            if event.type == pygame.QUIT:  # Clique pour quitter le jeu
                self.while_map_kamehouse_in = False  # Quitte le processus python
                Niveau.WHILE_GAME = False  # Ferme la boucle d'importation
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                Niveau.DIALOGUE = False

        if Niveau.DIALOGUE:
            font = pygame.font.Font("ressources/BebasNeue.ttf", 24)

            dialogue_bg = pygame.image.load('ressources/dialogue.png').convert_alpha()
            screen.blit(dialogue_bg, (0, 0))

            y = 390
            for i in range(len(self.text)):
                screen.blit(font.render(self.text[i], 1, (0, 0, 0)), (60, y))
                y = y+25

