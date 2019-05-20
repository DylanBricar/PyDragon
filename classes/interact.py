import pygame


class Interact:
    """ Gestion des interactions entre les personnages """

    def __init__(self, screen, font_police="ressources/fonts/BebasNeue.ttf", font_size=24):
        self.screen = screen  # Récupère l'écran sur lequel il faut dessiner
        self.font = pygame.font.Font(font_police, font_size)

    def show_box(self, text, avatar):
        """ Affiche la boite de message ainsi que la personne qui dit le message """
        dialogue_bg = pygame.image.load('ressources/images/dialogue.png').convert_alpha()  # Récupère le canvas
        self.screen.blit(dialogue_bg, (0, 0))  # Affiche le canvas

        avatar_img = pygame.image.load('ressources/images/avatars/avatar_' + avatar + '.png').convert_alpha()  # Récupère l'avatar
        self.screen.blit(avatar_img, (0, 231))  # Affiche l'avatar

        y = 390  # Distance d'écriture
        for i in range(len(text)):  # Parcours toutes les lignes de texte
            self.screen.blit(self.font.render(text[i], 1, (0, 0, 0)), (60, y))  # Affiche chacune des lignes
            y = y+25  # Ajoute 25px comme saut de ligne

