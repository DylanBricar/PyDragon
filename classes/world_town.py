def __init__(self, screen, new_map, path_number):
    """ Town environment initialization """
    self.screen = screen
    self.map = new_map
    self.path_number = path_number


def while_town(self, sound=None):
    """ Main town loop """
    pygame.display.set_caption("PyDragon Ball Z - Ville " + str(self.path_number))
    self.player = Player(self.map, 4, 11)
    self.escape_menu = EscapeMenu(self.screen, sound)
    self.escape_menu_active = False
    running = True
