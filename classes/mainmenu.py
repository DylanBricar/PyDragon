import sys
from pathlib import Path

import pygame
import pygame.gfxdraw

base_path = Path(__file__).parent.absolute()
sys.path.append(str(base_path))

from niveau import Niveau
import settings


class MainMenu:
    """ Game launch menu """

    def __init__(self, screen, clock, fps, sound):
        """ Get important variables """
        self.screen = screen
        self.fps = fps
        self.clock = clock
        self.sound = sound
        self.hovered_button = None

        try:
            self.menu_sound = pygame.mixer.Sound("ressources/sounds/Menu.wav")
            self.menu_sound.play(loops=-1)
            self.menu_sound.set_volume(0.3)
        except pygame.error:
            print("Warning: Unable to load or play menu sound")
            self.menu_sound = None

        self.while_map_kamehouse = False
        self.while_options = False

        self.while_main_menu = True

    def while_menu(self):
        """ Loop for the start menu """
        self.screen.blit(pygame.image.load('ressources/images/background_menu.png').convert_alpha(), (0, 0))

        font = pygame.font.Font("ressources/fonts/BebasNeue.ttf", 26)

        volume = 'ON' if not settings.SOUND_ENABLED else 'OFF'

        rect_global = pygame.rect.Rect(80, 180, 328, 185)
        pygame.gfxdraw.box(self.screen, rect_global, (255, 255, 255, 220))

        start_rect = pygame.rect.Rect(100, 200, 275, 60)
        start_shadow = pygame.rect.Rect(108, 205, 280, 65)
        pygame.gfxdraw.box(self.screen, start_shadow, (0, 0, 204, 255))
        start_text = font.render('Lancer le jeu', 1, (255, 255, 255))

        sound_rect = pygame.rect.Rect(100, 275, 275, 60)
        music_shadow = pygame.rect.Rect(108, 280, 280, 65)
        pygame.gfxdraw.box(self.screen, music_shadow, (0, 0, 204, 255))

        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        while self.while_main_menu:

            start_color = (0, 128, 255, 255) if self.hovered_button == "start" else (51, 153, 255, 255)
            sound_color = (0, 128, 255, 255) if self.hovered_button == "sound" else (51, 153, 255, 255)

            pygame.gfxdraw.box(self.screen, start_rect, start_color)
            pygame.gfxdraw.box(self.screen, sound_rect, sound_color)

            mouse_pos = pygame.mouse.get_pos()

            if start_rect.collidepoint(mouse_pos):
                self.hovered_button = "start"
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif sound_rect.collidepoint(mouse_pos):
                self.hovered_button = "sound"
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                self.hovered_button = None
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.while_main_menu = False
                    Niveau.WHILE_GAME = False

                if sound_rect.collidepoint(pygame.mouse.get_pos()):
                    hover = 'sound'
                    if event.type == pygame.MOUSEBUTTONUP:
                        if volume == 'ON':

                            if self.sound:
                                self.sound.set_volume(0.3)
                            if self.menu_sound:
                                self.menu_sound.set_volume(0.3)
                            volume = 'OFF'
                            settings.SOUND_ENABLED = True
                        else:
                            if self.sound:
                                self.sound.set_volume(0.0)
                            if self.menu_sound:
                                self.menu_sound.set_volume(0.0)
                            volume = 'ON'
                            settings.SOUND_ENABLED = False
                elif start_rect.collidepoint(pygame.mouse.get_pos()):
                    hover = 'start'
                    if event.type == pygame.MOUSEBUTTONUP:
                        if self.menu_sound:
                            self.menu_sound.stop()
                        if self.sound:
                            self.sound.play(loops=-1)
                        self.while_main_menu = False
                        self.while_map_kamehouse = True
                        Niveau.LVL = 'while_map_kamehouse'
                else:
                    hover = None

            if volume == 'ON':
                sound_text = font.render('Activer la musique', 1, (255, 255, 255))
                sound_coord = (155, 290)
            else:
                sound_text = font.render('Désactiver la musique', 1, (255, 255, 255))
                sound_coord = (145, 290)

            self.screen.blit(start_text, (180, 215))
            self.screen.blit(sound_text, sound_coord)
            self.clock.tick(self.fps)
            pygame.display.flip()
