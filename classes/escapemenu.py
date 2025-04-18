from pathlib import Path

import pygame
import pygame.gfxdraw

import settings


class EscapeMenu:
    """ Escape menu (Escape key) allowing to change sprite """

    def __init__(self, screen, son=None):
        """ Initialization of the escape menu """
        self.screen = screen
        self.sound = son

        self.menu_active = False
        self.menu_font = pygame.font.Font(None, 32)
        self.menu_width = 350
        self.menu_height = 450
        self.menu_x = screen.get_width() // 2 - self.menu_width // 2
        self.menu_y = screen.get_height() // 2 - self.menu_height // 2
        self.menu_spacing = 80

        self.button_height = 60
        self.button_width = 275
        self.button_font = pygame.font.Font("ressources/fonts/BebasNeue.ttf", 26)

        self.menu_options = [
            "Goku",
            "Super Saiyan",
            "Vegeta",
            "Retour au jeu"
        ]

        sound_dir = Path('ressources/images')
        self.sound_on_img = pygame.image.load(str(sound_dir / 'sound_on.png')).convert_alpha()
        self.sound_off_img = pygame.image.load(str(sound_dir / 'sound_off.png')).convert_alpha()

        self.icon_size = 30
        self.sound_on_img = pygame.transform.scale(self.sound_on_img, (self.icon_size, self.icon_size))
        self.sound_off_img = pygame.transform.scale(self.sound_off_img, (self.icon_size, self.icon_size))

        self.sound_icon_x = self.menu_width - 50
        self.sound_icon_y = 30

        self.button_hover = [False] * len(self.menu_options)
        self.sound_hover = False

        self.sound_on = settings.SOUND_ENABLED

    def toggle(self):
        """ Activates or deactivates the escape menu """
        self.menu_active = not self.menu_active

        self.sound_on = settings.SOUND_ENABLED
        return self.menu_active

    def toggle_music(self):
        """ Activates or deactivates the music """
        if self.sound:
            if settings.SOUND_ENABLED:
                pygame.mixer.stop()
                self.sound_on = False
                settings.SOUND_ENABLED = False
            else:
                pygame.mixer.stop()
                self.sound.set_volume(0.3)
                self.sound.play(-1)
                self.sound_on = True
                settings.SOUND_ENABLED = True
        return self.sound

    def draw(self):
        """ Display of the escape menu """
        if not self.menu_active:
            return False
        self.sound_on = settings.SOUND_ENABLED
        menu_surface = pygame.Surface((self.menu_width, self.menu_height), pygame.SRCALPHA)
        border_radius = 15
        pygame.draw.rect(menu_surface, (255, 255, 255, 180), (0, 0, self.menu_width, self.menu_height),
                         border_radius=border_radius)

        title_font = pygame.font.Font("ressources/fonts/BebasNeue.ttf", 40)
        title_text = title_font.render("Menu", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(self.menu_width // 2, 35))

        pygame.draw.line(menu_surface, (0, 128, 255, 200),
                         (title_rect.left - 20, title_rect.bottom + 5),
                         (title_rect.right + 20, title_rect.bottom + 5),
                         3)

        menu_surface.blit(title_text, title_rect)

        sound_icon_rect = pygame.Rect(
            self.sound_icon_x,
            self.sound_icon_y,
            self.icon_size,
            self.icon_size
        )

        if self.sound_on:
            menu_surface.blit(self.sound_on_img, sound_icon_rect)
        else:
            menu_surface.blit(self.sound_off_img, sound_icon_rect)

        for i, option in enumerate(self.menu_options):
            button_y = 100 + i * self.menu_spacing

            button_rect = pygame.rect.Rect(
                (self.menu_width - self.button_width) // 2,
                button_y,
                self.button_width,
                self.button_height
            )

            shadow = pygame.rect.Rect(
                ((self.menu_width - self.button_width) // 2) + 8,
                button_y + 5,
                self.button_width + 5,
                self.button_height + 5
            )

            button_color = (0, 128, 255, 255) if self.button_hover[i] else (51, 153, 255, 255)
            shadow_color = (0, 0, 204, 255)

            pygame.draw.rect(menu_surface, shadow_color, shadow, border_radius=10)
            pygame.draw.rect(menu_surface, button_color, button_rect, border_radius=10)

            button_text = self.button_font.render(option, True, (255, 255, 255))
            text_rect = button_text.get_rect(center=button_rect.center)
            menu_surface.blit(button_text, text_rect)

        self.screen.blit(menu_surface, (self.menu_x, self.menu_y))

        return True

    def update_hover_state(self):
        """ Updates the hover state according to the mouse position """
        mouse_pos = pygame.mouse.get_pos()

        relative_mouse_pos = (mouse_pos[0] - self.menu_x, mouse_pos[1] - self.menu_y)

        self.button_hover = [False] * len(self.menu_options)
        self.sound_hover = False

        sound_icon_rect = pygame.Rect(
            self.sound_icon_x,
            self.sound_icon_y,
            self.icon_size,
            self.icon_size
        )

        if sound_icon_rect.collidepoint(relative_mouse_pos):
            self.sound_hover = True
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            return

        for i in range(len(self.menu_options)):
            button_y = 100 + i * self.menu_spacing
            button_rect = pygame.Rect(
                (self.menu_width - self.button_width) // 2,
                button_y,
                self.button_width,
                self.button_height
            )

            if button_rect.collidepoint(relative_mouse_pos):
                self.button_hover[i] = True
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                return

        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def handle_event(self, event):
        """ Event handling for the escape menu """
        if not self.menu_active:
            return None

        self.update_hover_state()

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            relative_mouse_pos = (mouse_pos[0] - self.menu_x, mouse_pos[1] - self.menu_y)

            sound_icon_rect = pygame.Rect(
                self.sound_icon_x,
                self.sound_icon_y,
                self.icon_size,
                self.icon_size
            )

            if sound_icon_rect.collidepoint(relative_mouse_pos):
                if self.sound:
                    self.toggle_music()
                return None

            for i in range(len(self.menu_options)):
                button_y = 100 + i * self.menu_spacing
                button_rect = pygame.Rect(
                    (self.menu_width - self.button_width) // 2,
                    button_y,
                    self.button_width,
                    self.button_height
                )

                if button_rect.collidepoint(relative_mouse_pos):
                    if self.menu_options[i] == "Retour au jeu":
                        self.toggle()
                        return None
                    else:
                        selected_character = i
                        self.toggle()
                        return selected_character

        return None
