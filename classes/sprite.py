import pygame  # Import PyGame


class Sprite:
    """ Gestion des sprites et de ses animations """

    # Variable de classe pour contrôler les logs de débogage
    DEBUG_LOGGING = False
    # Variable pour contrôler les avertissements de limites de sprite
    SHOW_BOUNDARY_WARNINGS = False

    def __init__(self):
        self.sprite_type = 0  # Type de sprite (0: Goku normal, 1: Goku transformé, 2: Vegeta)
        try:
            self.sprite_selected = pygame.image.load('ressources/sprites/characters/goku.png').convert_alpha()
            sprite_width = self.sprite_selected.get_width()
            sprite_height = self.sprite_selected.get_height()
            if Sprite.DEBUG_LOGGING:
                print(f"Sprite de Goku chargé: dimensions {sprite_width}x{sprite_height} pixels")
            
            # On va forcer l'utilisation d'un offset fixe pour Super Saiyan car nous savons que
            # les 3 premières colonnes sont Goku normal et les 3 suivantes sont Super Saiyan
            self.goku_transformed_offset_x = 3 * 32  # Décalage pour accéder à Goku transformé
            
            if Sprite.DEBUG_LOGGING:
                print("Info: Offset pour Goku transformé défini à", self.goku_transformed_offset_x)
        except Exception as e:
            print(f"Erreur lors du chargement du sprite de Goku: {e}")
            # Créer un sprite par défaut en cas d'erreur
            self.sprite_selected = pygame.Surface((96, 140))
            self.sprite_selected.fill((255, 0, 0))
            self.goku_transformed_offset_x = 0
        
        # Direction => Marche 1 | Marche 2 | Arret
        self.direction = {'Down': [[0, 0], [2, 0], [1, 0]], 'Up': [[0, 3], [2, 3], [1, 3]],
                          'Left': [[0, 1], [2, 1], [1, 1]], 'Right': [[0, 2], [2, 2], [1, 2]]}
        self.current_position = 1  # Direction de marche par défaut
        # Variable pour limiter l'affichage des messages de débogage
        self.last_debug_message = ""
        # Compter les erreurs pour ne pas les répéter sans cesse
        self.error_count = 0

    def change_sprite(self, sprite_type):
        """ Change le sprite du personnage """
        self.sprite_type = sprite_type
        
        if sprite_type == 0:  # Goku normal
            try:
                self.sprite_selected = pygame.image.load('ressources/sprites/characters/goku.png').convert_alpha()
                if Sprite.DEBUG_LOGGING:
                    print(f"Sprite de Goku normal chargé: dimensions {self.sprite_selected.get_width()}x{self.sprite_selected.get_height()} pixels")
                # Réinitialiser le décalage
                self.goku_transformed_offset_x = 0
            except Exception as e:
                print(f"Erreur lors du chargement du sprite de Goku normal: {e}")
        elif sprite_type == 1:  # Goku transformé
            try:
                # Pour Goku transformé, nous utilisons le même fichier mais la partie droite
                self.sprite_selected = pygame.image.load('ressources/sprites/characters/goku.png').convert_alpha()
                if Sprite.DEBUG_LOGGING:
                    sprite_width = self.sprite_selected.get_width()
                    sprite_height = self.sprite_selected.get_height()
                    print(f"Sprite de Goku transformé: dimensions {sprite_width}x{sprite_height} pixels")
                
                # Forcer l'utilisation d'un offset fixe pour Super Saiyan
                self.goku_transformed_offset_x = 3 * 32
                if Sprite.DEBUG_LOGGING:
                    print(f"Offset pour Super Saiyan défini à {self.goku_transformed_offset_x}")
            except Exception as e:
                print(f"Erreur lors du chargement du sprite de Goku transformé: {e}")
                self.sprite_type = 0
                self.goku_transformed_offset_x = 0
        elif sprite_type == 2:  # Vegeta
            try:
                self.sprite_selected = pygame.image.load('ressources/sprites/characters/vegeta.png').convert_alpha()
                if Sprite.DEBUG_LOGGING:
                    print(f"Sprite de Vegeta chargé: dimensions {self.sprite_selected.get_width()}x{self.sprite_selected.get_height()} pixels")
                # Pas de décalage nécessaire pour Vegeta
                self.goku_transformed_offset_x = 0
            except Exception as e:
                print(f"Erreur lors du chargement du sprite de Vegeta: {e}")
        
        # Réinitialiser le compteur d'erreurs lors d'un changement de sprite
        self.error_count = 0        
        return self.sprite_type

    def select_sprite(self, ligne, colonne, pixel_ligne=32, pixel_colonne=35):
        """ Selectionne une case du sprite """
        # Calculer les coordonnées en fonction du type de sprite
        if self.sprite_type == 1:  # Goku transformé - utiliser le décalage horizontal
            x = self.goku_transformed_offset_x + (pixel_ligne * ligne)
        else:
            x = pixel_ligne * ligne
            
        y = pixel_colonne * colonne
            
        # Vérifier que les coordonnées sont valides
        sprite_width = self.sprite_selected.get_width()
        sprite_height = self.sprite_selected.get_height()
        
        # Créer un message de débogage
        debug_msg = f"type={self.sprite_type}, coords=({x}, {y})"
        
        # Afficher les coordonnées pour débogage uniquement si nécessaire et pas répétitif
        if Sprite.DEBUG_LOGGING and ligne == 1 and colonne == 0 and debug_msg != self.last_debug_message:
            print(f"Sélection de sprite: {debug_msg}, taille_sprite=({sprite_width}, {sprite_height})")
            self.last_debug_message = debug_msg
        
        # Vérifier et ajuster les coordonnées pour éviter les dépassements
        if x + pixel_ligne > sprite_width:
            x = sprite_width - pixel_ligne
            if Sprite.SHOW_BOUNDARY_WARNINGS and self.error_count % 50 == 0:
                print(f"Ajustement X: ({x}, {y}), limites: ({sprite_width}, {sprite_height})")
            self.error_count += 1
        
        if y + pixel_colonne > sprite_height:
            y = sprite_height - pixel_colonne
            if Sprite.SHOW_BOUNDARY_WARNINGS and self.error_count % 50 == 0:
                print(f"Ajustement Y: ({x}, {y}), limites: ({sprite_width}, {sprite_height})")
            self.error_count += 1
        
        try:
            return self.sprite_selected.subsurface(x, y, pixel_ligne, pixel_colonne)
        except ValueError as e:
            # En cas d'erreur, revenir à Goku normal et réessayer
            if self.error_count % 50 == 0:  # Limiter les messages d'erreur
                print(f"Erreur lors de la sélection du sprite: {e}. Retour à Goku normal.")
            self.error_count += 1
            self.sprite_type = 0
            self.goku_transformed_offset_x = 0
            x = pixel_ligne * ligne
            y = pixel_colonne * colonne
            
            # S'assurer que les coordonnées sont valides
            x = min(x, sprite_width - pixel_ligne)
            y = min(y, sprite_height - pixel_colonne)
            
            return self.sprite_selected.subsurface(x, y, pixel_ligne, pixel_colonne)

    def animate_sprite(self, move, old_pos_sprite):
        """ Animation de marche du personnage """
        # Sprite par défaut
        new_img_sprite = self.select_sprite(self.direction[old_pos_sprite][2][0], self.direction[old_pos_sprite][2][1])

        # Cas où le déplacement n'est pas demandé
        if move is not None:
            for i in {'Down', 'Up', 'Left', 'Right'}:  # Liste des possibilités de déplacement
                if move == i:
                    if self.current_position == 1:  # Premier Sprite de marche
                        new_img_sprite = self.select_sprite(self.direction[i][0][0], self.direction[i][0][1])
                        self.current_position = 2  # Met à jour la valeur de marche
                    elif self.current_position == 2:  # Deuxième Sprite de marche
                        self.current_position = 1  # Met à jour la valeur de marche
                        new_img_sprite = self.select_sprite(self.direction[i][1][0], self.direction[i][1][1])

        return new_img_sprite  # Retourne le nouveau Sprite
