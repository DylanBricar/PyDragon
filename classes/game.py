import sys
from pathlib import Path

import pygame

base_path = Path(__file__).parent.absolute()
sys.path.append(str(base_path))
sys.path.append(str(base_path / "maps"))

from mainmenu import MainMenu
from niveau import Niveau

from kamehouse import Kamehouse
from kamehousein import KamehouseIn
from worldtown import WorldTown
from worldtownin import WorldTownIn


class Game:
    """ Game variables and map management """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.favicon = 'ressources/favicon.png'
        self.fps = 24
        self.move_speed = 8.0
        self.sound = None

    def main(self):
        """ Game launch """
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('PyDragon v0.5')
        pygame.display.set_icon(pygame.image.load(self.favicon))

        try:
            self.sound = pygame.mixer.Sound("ressources/sounds/DBZFighter.wav")
            self.sound.set_volume(0.3)
        except pygame.error:
            print("Warning: Unable to load or play sound")
            self.sound = None

        clock = pygame.time.Clock()

        try:
            sound_dir = Path('ressources/images')
            sound_dir.mkdir(parents=True, exist_ok=True)

            sound_on_path = sound_dir / 'sound_on.png'
            sound_off_path = sound_dir / 'sound_off.png'

            if not sound_on_path.exists() or not sound_off_path.exists():
                sound_on = pygame.Surface((30, 30), pygame.SRCALPHA)
                sound_off = pygame.Surface((30, 30), pygame.SRCALPHA)

                pygame.draw.circle(sound_on, (255, 255, 255), (15, 15), 10)
                pygame.draw.circle(sound_on, (0, 0, 0), (15, 15), 8)
                pygame.draw.circle(sound_on, (255, 255, 255), (15, 15), 5)

                pygame.draw.circle(sound_off, (255, 255, 255), (15, 15), 10)
                pygame.draw.circle(sound_off, (0, 0, 0), (15, 15), 8)
                pygame.draw.line(sound_off, (255, 0, 0), (5, 5), (25, 25), 3)

                pygame.image.save(sound_on, str(sound_on_path))
                pygame.image.save(sound_off, str(sound_off_path))
        except Exception as e:
            print(f"Error creating sound icons: {e}")

        while Niveau.WHILE_GAME:
            if Niveau.LVL == 'while_main_menu':
                main_menu = MainMenu(screen, clock, self.fps, self.sound)
                main_menu.while_menu()
            elif Niveau.LVL == 'while_map_kamehouse':
                map_kamehouse = Kamehouse(self.width, self.height, screen, clock, self.fps, self.move_speed)
                map_kamehouse.while_kamehouse(self.sound)
            elif Niveau.LVL == 'while_map_kamehouse_in':
                map_kamehouse_in = KamehouseIn(self.width, self.height, screen, clock, self.fps, self.move_speed)
                map_kamehouse_in.while_kamehouse_in(self.sound)
            elif Niveau.LVL == 'while_map_town':
                map_world = WorldTown(self.width, self.height, screen, clock, self.fps, self.move_speed)
                map_world.while_town(self.sound)
            elif Niveau.LVL == 'while_map_town_in':
                map_world = WorldTownIn(self.width, self.height, screen, clock, self.fps, self.move_speed)
                map_world.while_town_in(self.sound)

        pygame.quit()
