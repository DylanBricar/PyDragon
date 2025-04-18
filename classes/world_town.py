def __init__(self, screen, new_map, path_number):
    """ Initialisation de l'environnement de ville """
    self.screen = screen          # Écran principal
    self.map = new_map            # Map à utiliser
    self.path_number = path_number # Numéro du chemin

def while_town(self, son=None):
    """ Boucle principale de la ville """
    # Initialisation
    pygame.display.set_caption("PyDragon Ball Z - Ville " + str(self.path_number))
    self.player = Player(self.map, 4, 11)    # Initialisation du joueur
    self.escape_menu = EscapeMenu(self.screen, son)        # Menu d'échappement
    self.escape_menu_active = False          # État du menu
    running = True 