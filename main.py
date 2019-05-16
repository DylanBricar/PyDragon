import os   # Import OS
import sys  # Import SYS

sys.path.append(os.getcwd() + "/classes")  # Ajout du chemin pour éviter les bugs Windows
from game import Game  # Import de la class Game

if __name__ == '__main__':
    Game(850, 550).main()  # Lance la boucle du jeu avec la taille choisie
