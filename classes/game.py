import os      # Import OS
import sys     # Import SYS
import pygame  # Import PyGame
from pathlib import Path  # Import Path pour une meilleure gestion des chemins

# Ajout des chemins absolus pour éviter les problèmes d'importation
base_path = Path(__file__).parent.absolute()
sys.path.append(str(base_path))
sys.path.append(str(base_path / "maps"))

from mainmenu import MainMenu  # Import de la class MainMenu
from niveau import Niveau      # Import de la class Niveau
import settings  # Import du module settings

# Import des maps
from kamehouse import Kamehouse      # Import de la class Kamehouse
from kamehousein import KamehouseIn  # Import de la class KamehouseIn
from worldtown import WorldTown      # Import de la class WorldTown
from worldtownin import WorldTownIn  # Import de la class WorldTownIn


class Game:
    """ Gestion des variables et import des différentes map du jeu """

    def __init__(self, width, height):
        self.width = width      # Largeur de la fenêtre de jeu
        self.height = height    # Hauteur de la fenêtre du jeu
        self.favicon = 'ressources/favicon.png'  # Chemin du favicon
        self.fps = 24  # FPS limités
        self.avancer = 8.0  # Échelle de déplacement
        self.son = None  # Sera initialisé dans la méthode main

    def main(self):
        """ Lancement du jeu """
        pygame.init()  # Lance de Pygame
        screen = pygame.display.set_mode((self.width, self.height))  # Crée la fenêtre
        pygame.display.set_caption('PyDragon v0.5')  # Donne un nom à la fenêtre (mise à jour version)
        pygame.display.set_icon(pygame.image.load(self.favicon))  # Favicon du jeu
        
        # Utilisation de mixer avec gestion d'exceptions pour une meilleure compatibilité
        try:
            self.son = pygame.mixer.Sound("ressources/sounds/DBZFighter.wav")  # Défini le son du jeu
            self.son.set_volume(0.3)  # Permet de diminuer le son par défaut du jeu
        except pygame.error:
            print("Attention: Impossible de charger ou jouer le son")
            self.son = None

        clock = pygame.time.Clock()  # Calcule le temps de départ pour les FPS

        # Création des images pour les icônes sonores
        try:
            # Créer un répertoire pour les images s'il n'existe pas
            sound_dir = Path('ressources/images')
            sound_dir.mkdir(parents=True, exist_ok=True)

            # Vérifier si les icônes existent déjà
            sound_on_path = sound_dir / 'sound_on.png'
            sound_off_path = sound_dir / 'sound_off.png'

            if not sound_on_path.exists() or not sound_off_path.exists():
                # Créer des icônes sonores simples
                sound_on = pygame.Surface((30, 30), pygame.SRCALPHA)
                sound_off = pygame.Surface((30, 30), pygame.SRCALPHA)
                
                # Dessiner un cercle pour l'icône son activé
                pygame.draw.circle(sound_on, (255, 255, 255), (15, 15), 10)
                pygame.draw.circle(sound_on, (0, 0, 0), (15, 15), 8)
                pygame.draw.circle(sound_on, (255, 255, 255), (15, 15), 5)
                
                # Dessiner un cercle barré pour l'icône son désactivé
                pygame.draw.circle(sound_off, (255, 255, 255), (15, 15), 10)
                pygame.draw.circle(sound_off, (0, 0, 0), (15, 15), 8)
                pygame.draw.line(sound_off, (255, 0, 0), (5, 5), (25, 25), 3)
                
                # Sauvegarder les icônes
                pygame.image.save(sound_on, str(sound_on_path))
                pygame.image.save(sound_off, str(sound_off_path))
        except Exception as e:
            print(f"Erreur lors de la création des icônes de son: {e}")

        while Niveau.WHILE_GAME:  # Boucle principale qui sert aux importations de maps
            if Niveau.LVL == 'while_main_menu':  # Nom défini qui orchestre tous les imports liés
                main_menu = MainMenu(screen, clock, self.fps, self.son)  # Instancie la class qui affiche le menu de départ
                main_menu.while_menu()  # Boucle sur le menu
            elif Niveau.LVL == 'while_map_kamehouse':
                map_kamehouse = Kamehouse(self.width, self.height, screen, clock, self.fps, self.avancer)
                map_kamehouse.while_kamehouse(self.son)  # Boucle sur la map avec référence au son
            elif Niveau.LVL == 'while_map_kamehouse_in':
                map_kamehouse_in = KamehouseIn(self.width, self.height, screen, clock, self.fps, self.avancer)
                map_kamehouse_in.while_kamehouse_in(self.son)  # Boucle sur la map avec référence au son
            elif Niveau.LVL == 'while_map_town':
                map_world = WorldTown(self.width, self.height, screen, clock, self.fps, self.avancer)
                map_world.while_town(self.son)  # Boucle sur la map avec référence au son
            elif Niveau.LVL == 'while_map_town_in':
                map_world = WorldTownIn(self.width, self.height, screen, clock, self.fps, self.avancer)
                map_world.while_town_in(self.son)  # Boucle sur la map avec référence au son

        pygame.quit()  # Arrête le processus de PyGame
