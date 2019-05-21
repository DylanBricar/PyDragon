class Niveau:
    """ Ensemble des informations sur la carte """

    LVL = 'while_main_menu'  # Niveau par défaut
    WHILE_GAME = True        # Boucle de jeu
    COORDONNEE = []          # Sauvegarde de la position du joueur dans la map Kamehouse
    COORDONNEE_TOWN = []     # Sauvegarde de la position du joueur dans la map WorldTown
    DIALOGUE = False         # Boolen en cas de dialogue
    MISSION_01 = 0           # Regarde si la mission_01 est en cours [0 - 100%]
    PAGE = 1                 # Page par défaut en cas d'un dialogue
    INVENTORY = []           # Inventaire du personnage
