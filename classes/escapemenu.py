import pygame
import pygame.gfxdraw
from pathlib import Path

import settings  # Import du module settings


class EscapeMenu:
    """ Menu d'échappement (touche Echap) permettant de changer de sprite """

    def __init__(self, screen, son=None):
        """ Initialisation du menu d'échappement """
        self.screen = screen        # Récupère le screen principal
        self.son = son              # Référence au son du jeu
        
        # Paramètres du menu
        self.menu_active = False
        self.menu_font = pygame.font.Font(None, 32)
        self.menu_width = 350
        self.menu_height = 450  # Hauteur augmentée pour plus d'espace
        self.menu_x = screen.get_width() // 2 - self.menu_width // 2
        self.menu_y = screen.get_height() // 2 - self.menu_height // 2
        self.menu_spacing = 80  # Espacement entre les boutons
        
        # Boutons du menu (même style que le menu principal)
        self.button_height = 60
        self.button_width = 275
        self.button_font = pygame.font.Font("ressources/fonts/BebasNeue.ttf", 26)
        
        # Options du menu (sans l'option musique qui sera remplacée par une icône)
        self.menu_options = [
            "Goku",
            "Super Saiyan",
            "Vegeta",
            "Retour au jeu"
        ]
        
        # Chargement des icônes son
        sound_dir = Path('ressources/images')
        self.sound_on_img = pygame.image.load(str(sound_dir / 'sound_on.png')).convert_alpha()
        self.sound_off_img = pygame.image.load(str(sound_dir / 'sound_off.png')).convert_alpha()
        
        # Redimensionner les icônes si nécessaire
        self.icon_size = 30
        self.sound_on_img = pygame.transform.scale(self.sound_on_img, (self.icon_size, self.icon_size))
        self.sound_off_img = pygame.transform.scale(self.sound_off_img, (self.icon_size, self.icon_size))
        
        # Position de l'icône son
        self.sound_icon_x = self.menu_width - 50
        self.sound_icon_y = 30
        
        # État de survol des boutons
        self.button_hover = [False] * len(self.menu_options)
        self.sound_hover = False
        
        # État du son - utiliser la variable du module settings
        self.sound_on = settings.SOUND_ENABLED

    def toggle(self):
        """ Active ou désactive le menu d'échappement """
        self.menu_active = not self.menu_active
        # Met à jour l'état du son en fonction de la variable du module
        self.sound_on = settings.SOUND_ENABLED
        return self.menu_active

    def toggle_music(self):
        """ Active ou désactive la musique """
        if self.son:
            if settings.SOUND_ENABLED:
                pygame.mixer.stop()  # Arrête la musique
                self.sound_on = False
                settings.SOUND_ENABLED = False
            else:
                # Arrêter tous les sons avant de relancer celui-ci pour éviter les superpositions
                pygame.mixer.stop()
                # Réinitialiser le volume et jouer le son
                self.son.set_volume(0.3)
                self.son.play(-1)  # Joue la musique en boucle
                self.sound_on = True
                settings.SOUND_ENABLED = True
        return self.son

    def draw(self):
        """ Affichage du menu d'échappement """
        if not self.menu_active:
            return False
            
        # Met à jour l'état du son en fonction de la variable du module
        self.sound_on = settings.SOUND_ENABLED
            
        # Création d'une surface avec canal alpha pour la transparence
        menu_surface = pygame.Surface((self.menu_width, self.menu_height), pygame.SRCALPHA)
        
        # Fond semi-transparent avec bords arrondis
        border_radius = 15
        pygame.draw.rect(menu_surface, (255, 255, 255, 180), (0, 0, self.menu_width, self.menu_height), border_radius=border_radius)
        
        # Titre du menu stylisé
        title_font = pygame.font.Font("ressources/fonts/BebasNeue.ttf", 40)
        title_text = title_font.render("Menu", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(self.menu_width // 2, 35))
        
        # Ajout d'un effet de soulignement pour le titre
        pygame.draw.line(menu_surface, (0, 128, 255, 200), 
                        (title_rect.left - 20, title_rect.bottom + 5), 
                        (title_rect.right + 20, title_rect.bottom + 5), 
                        3)
        
        menu_surface.blit(title_text, title_rect)
        
        # Dessiner l'icône son
        sound_icon_rect = pygame.Rect(
            self.sound_icon_x,
            self.sound_icon_y,
            self.icon_size,
            self.icon_size
        )
        
        # Afficher l'icône appropriée selon l'état réel du son
        if self.sound_on:
            menu_surface.blit(self.sound_on_img, sound_icon_rect)
        else:
            menu_surface.blit(self.sound_off_img, sound_icon_rect)
        
        # Dessiner les boutons dans le style du menu principal
        for i, option in enumerate(self.menu_options):
            button_y = 100 + i * self.menu_spacing
            
            # Rectangle du bouton et son ombre (comme dans mainmenu.py)
            button_rect = pygame.rect.Rect(
                (self.menu_width - self.button_width) // 2,
                button_y,
                self.button_width,
                self.button_height
            )
            
            ombre = pygame.rect.Rect(
                ((self.menu_width - self.button_width) // 2) + 8,
                button_y + 5,
                self.button_width + 5,
                self.button_height + 5
            )
            
            # Couleur du bouton en fonction du survol
            button_color = (0, 128, 255, 255) if self.button_hover[i] else (51, 153, 255, 255)
            ombre_color = (0, 0, 204, 255)
            
            # Dessiner l'ombre et le bouton avec des bords arrondis
            pygame.draw.rect(menu_surface, ombre_color, ombre, border_radius=10)
            pygame.draw.rect(menu_surface, button_color, button_rect, border_radius=10)
            
            # Texte du bouton
            button_text = self.button_font.render(option, True, (255, 255, 255))
            text_rect = button_text.get_rect(center=button_rect.center)
            menu_surface.blit(button_text, text_rect)
        
        # Afficher le menu à l'écran
        self.screen.blit(menu_surface, (self.menu_x, self.menu_y))
        
        return True
    
    def update_hover_state(self):
        """ Met à jour l'état de survol en fonction de la position de la souris """
        mouse_pos = pygame.mouse.get_pos()
        
        # Convertir les coordonnées de la souris par rapport à la surface du menu
        relative_mouse_pos = (mouse_pos[0] - self.menu_x, mouse_pos[1] - self.menu_y)
        
        # Réinitialiser tous les états de survol
        self.button_hover = [False] * len(self.menu_options)
        self.sound_hover = False
        
        # Vérifier le survol de l'icône son
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
        
        # Vérifier les collisions avec chaque bouton
        for i in range(len(self.menu_options)):
            button_y = 100 + i * self.menu_spacing
            button_rect = pygame.Rect(
                (self.menu_width - self.button_width) // 2,
                button_y,
                self.button_width,
                self.button_height
            )
            
            # Vérifier si la souris est sur ce bouton
            if button_rect.collidepoint(relative_mouse_pos):
                self.button_hover[i] = True
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                return
        
        # Si on arrive ici, pas de survol détecté
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
    def handle_event(self, event):
        """ Gestion des événements pour le menu d'échappement """
        if not self.menu_active:
            return None
            
        # Mettre à jour l'état de survol
        self.update_hover_state()
            
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            # Convertir les coordonnées de la souris par rapport à la surface du menu
            relative_mouse_pos = (mouse_pos[0] - self.menu_x, mouse_pos[1] - self.menu_y)
            
            # Vérifier si l'icône son a été cliquée
            sound_icon_rect = pygame.Rect(
                self.sound_icon_x,
                self.sound_icon_y,
                self.icon_size,
                self.icon_size
            )
            
            if sound_icon_rect.collidepoint(relative_mouse_pos):
                if self.son:
                    self.toggle_music()
                return None
            
            # Vérification du clic sur les options
            for i in range(len(self.menu_options)):
                button_y = 100 + i * self.menu_spacing
                button_rect = pygame.Rect(
                    (self.menu_width - self.button_width) // 2,
                    button_y,
                    self.button_width,
                    self.button_height
                )
                
                if button_rect.collidepoint(relative_mouse_pos):
                    # Si l'option est une transformation (0, 1, 2), fermer le menu
                    if i == 0 or i == 1 or i == 2:
                        result = i
                        self.menu_active = False  # Fermer le menu après avoir choisi une transformation
                        return result
                    elif i == 3:  # Retour au jeu
                        self.menu_active = False  # Fermer le menu
                        return None
                
        return None 