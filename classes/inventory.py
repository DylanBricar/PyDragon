import os
import sys

import pygame

sys.path.append(os.getcwd() + "/classes")
from niveau import *


class Inventory:
    """ Character inventory management """

    def __init__(self, screen, font_file="ressources/fonts/BebasNeue.ttf", font_size=24):
        self.screen = screen
        self.font = pygame.font.Font(font_file, font_size)

    def show_item(self):
        """ Display player items at the top of the screen """
        y = 40
        if Niveau.INVENTORY:
            for i in range(6):
                if len(Niveau.INVENTORY) > i:
                    self.screen.blit(self.font.render("Inventaire :", 1, (0, 0, 0)), (10, 10))
                    self.screen.blit(
                        pygame.image.load('ressources/images/items/' + Niveau.INVENTORY[i] + '.png').convert_alpha(),
                        (35, y))
                    y = y + 44
