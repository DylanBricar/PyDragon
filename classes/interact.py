import os
import sys

import pygame

sys.path.append(os.getcwd() + "/classes")
from niveau import *


class Interact:
    """ Management of interactions between characters """

    def __init__(self, screen, font_file="ressources/fonts/BebasNeue.ttf", font_size=24):
        self.screen = screen
        self.font = pygame.font.Font(font_file, font_size)

    def show_box(self, text):
        """ Displays the message box and the person saying the message """
        dialogue_bg = pygame.image.load('ressources/images/dialogue.png').convert_alpha()
        self.screen.blit(dialogue_bg, (0, 0))

        y = 390
        for i in range((Niveau.PAGE * 4) - 4, Niveau.PAGE * 4):
            if len(text) > i:
                split_text = text[i].split(" | ")

                if len(split_text) == 2:
                    avatar_img = pygame.image.load(
                        'ressources/images/avatars/avatar_' + text[i].split(" | ")[1] + '.png').convert_alpha()
                    self.screen.blit(avatar_img, (0, 231))

                self.screen.blit(self.font.render(split_text[0], 1, (0, 0, 0)), (60, y))
                y = y + 25
