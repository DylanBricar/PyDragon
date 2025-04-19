import sys
from pathlib import Path

import pygame

pygame.display.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.font.init()

base_path = Path(__file__).parent.absolute()
sys.path.append(str(base_path / "classes"))

from game import Game

if __name__ == '__main__':
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.USEREVENT])
    Game(850, 550).main()
