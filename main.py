import os   # Import OS
import sys  # Import SYS
from pathlib import Path  # Import Path pour une meilleure gestion des chemins

# Ajout des chemins absolus pour éviter les problèmes d'importation
base_path = Path(__file__).parent.absolute()
sys.path.append(str(base_path / "classes"))

from game import Game  # Import de la class Game

if __name__ == '__main__':
    Game(850, 550).main()  # Lance la boucle du jeu avec la taille choisie
