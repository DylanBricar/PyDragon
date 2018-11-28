import pygame           # Import PyGame
from libs import tmx    # Libraire TMX (bypass pour Python 2)


class Sprite:
    """ Gestion des sprites """
    @staticmethod
    def select_sprite(ligne, colonne, pixel_ligne=32, pixel_colonne=35):
        """ Selectionne une case du sprite """
        sprite_selected = pygame.image.load('ressources/sprites/characters/vegeta.png')
        return sprite_selected.subsurface(pixel_ligne * ligne, pixel_colonne * colonne, pixel_ligne, pixel_colonne)


class Player:
    """ Gestion du joueur """
    def __init__(self, tilemap, width, height):
        self.tilemap = tilemap  # Récupère la map

        self.sprite_player = Sprite.select_sprite(1, 0)  # Génère le sprite de base
        joueur_pos = self.tilemap.layers['evenements'].find('player')[0]  # Trouve le joueur depuis la map
        self.player = pygame.rect.Rect((joueur_pos.px, joueur_pos.py), self.sprite_player.get_size())  # Crée son rectangle

        self.div_x_map = width/2    # Taille de la map en longeur divisée en deux
        self.div_y_map = height/2   # Taille de la map en largeur divisée en deux

        self.y = self.div_y_map     # Utilisé pour positionner le joueur (au centre vertical par défaut)
        self.x = self.div_x_map     # Utilisé pour positionner le joueur (au centre horizontal par défaut)


class CollisionController:
    """ Gestion des collisions """
    def __init__(self, player, total_collision):
        self.total_collision = total_collision  # Liste avec toutes les collisions de la map
        self.player = player  # Globalité de la class du joueur

    def collision(self):
        """ Repère les collisions """
        for i in range(0, len(self.total_collision)):
            collision_selected = self.total_collision[i]

            if ((self.player.player.x >= collision_selected.px + collision_selected.width)          # Trop à droite
                    or (self.player.player.x + self.player.player.w <= collision_selected.px)       # Trop à gauche
                    or (self.player.player.y >= collision_selected.py + collision_selected.height)  # Trop en bas
                    or (self.player.player.y + self.player.player.h <= collision_selected.py)):     # Trop en haut
                var = False
            else:
                var = True

            if var:  # Une collision est trouvée
                return False


class Move:
    """ Déplacement du joueur """
    def __init__(self, player, pas, collision, collision_exist):
        self.player = player  # Toutes les informations de la class player
        self.pas = pas  # Déplacement qui doit être fait
        self.collision_exist = collision_exist  # Collision déjà présente
        self.collision = collision  # Liste de toutes les collisions

        # Bords de la map
        self.bordure_h = self.player.div_y_map
        self.bordure_b = self.player.tilemap.px_height - self.player.div_y_map
        self.bordure_g = self.player.div_x_map
        self.bordure_d = self.player.tilemap.px_width - self.player.div_x_map

    def move_player(self, direction):
        """ Déplace le joueur en fonction de la touche """
        if direction == 'bas':  # Touche du bas appuyée
            self.player.sprite_player = Sprite.select_sprite(1, 0)  # Selectionne le sprite associé

            # Le joueur se trouve entre les deux extrémités verticales de la map
            if self.bordure_h > self.player.player.y > self.bordure_b:
                self.player.y = self.player.div_y_map  # Le joueur est centré sur la map
            # Le joueur se trouve proche d'une des deux extrémités de la map
            elif self.player.player.y <= self.bordure_h or self.player.player.y >= self.bordure_b:
                self.player.y += self.pas  # Il se rapproche du bord
            self.player.player.y += self.pas  # Le joueur avance

        elif direction == 'haut':
            self.player.sprite_player = Sprite.select_sprite(1, 3)

            if self.player.player.y <= self.bordure_h or self.player.player.y >= self.bordure_b:
                self.player.y -= self.pas
            elif self.bordure_b > self.player.player.y > self.bordure_h:
                self.player.y = self.player.div_y_map
            self.player.player.y -= self.pas

        elif direction == 'gauche':
            self.player.sprite_player = Sprite.select_sprite(1, 1)

            if self.bordure_d >= self.player.player.x >= self.bordure_g:
                self.player.x = self.player.div_x_map
            elif self.player.player.x <= self.bordure_g or self.player.player.x >= self.bordure_d:
                self.player.x -= self.pas
            self.player.player.x -= self.pas

        elif direction == 'droit':
            self.player.sprite_player = Sprite.select_sprite(1, 2)

            if self.player.player.x < self.bordure_g or self.player.player.x > self.bordure_d:
                self.player.x += self.pas
            elif self.bordure_g > self.player.player.x > self.bordure_d:
                self.player.x = self.player.div_x_map
            self.player.player.x += self.pas

    def move_total(self, bouton_pressed):
        """ Déplacements autorisés après collision """
        positions = ['bas', 'haut', 'gauche', 'droit']  # Tableau de possibilités
        positions.remove(self.collision_exist)  # Suppression de la possibilité lié à la collision

        if CollisionController(self.player, self.collision).collision() is False:  # Vérifie s'il y a collision
            for i in range(len(positions)):  # Boucle les 3 touches restantes
                if bouton_pressed == positions[i]:  # Vérifie la touche appuyée en fonction de la boucle
                    exec('self.move_player("' + positions[i] + '")')  # Execute la fonction de déplacement associée

        if CollisionController(self.player, self.collision).collision() is not False:
            self.collision_exist = None  # Aucune collision donc remet à zéro la variable de collision

    def move_controller(self, touche_selected):
        """ Appel aux fonctions de collisions nécessaires """
        positions = ['bas', 'haut', 'gauche', 'droit']  # Tableau de possibilités

        for i in range(len(positions)):  # Boucle toutes les touches
            if touche_selected == positions[i]:  # Vérifie la touche appuyée en fonction de la boucle

                collide = CollisionController(self.player, self.collision)  # Appelle la class de collision

                # Collision repérée + variable de collision déjà définie
                if collide.collision() is False and self.collision_exist is not None:
                    self.move_total(positions[i])  # On renvoie la variable de collision et attend une action

                elif collide.collision() is False:  # Collision repérée sans variable de collision définie
                    self.collision_exist = positions[i]  # Défini la variable de collision
                    self.move_total(positions[i])  # Envoie cette nouvelle variable et attend une action

                elif self.collision_exist is None:  # La variable de collision est vide
                    exec('self.move_player("' + positions[i] + '")')  # Appelle de fonction pour déplacer le joueur


class Game:
    """ Gestion des imports du jeu """
    def __init__(self, width, height):
        self.width = width      # Largeur de la fenêtre de jeu
        self.height = height    # Hauteur de la fenêtre du jeu
        self.map = 'ressources/maps/kamehouse/map.tmx'  # Chemin de la map
        self.favicon = 'ressources/favicon.png'  # Chemin du favicon
        self.fps = 30  # FPS demandés
        self.avancer = 15.0  # Échelle de déplacement
        self.collision_exist = None  # Définition de la variable de collision vide

    def main(self):
        """ Lancement du jeu """
        pygame.init()  # Lance de Pygame
        screen = pygame.display.set_mode((self.width, self.height))  # Crée la fenêtre
        pygame.display.set_caption('PyDragon v0.1')  # Donne un nom à la fenêtre
        pygame.display.set_icon(pygame.image.load(self.favicon))  # Favicon du jeu
        tilemap = tmx.load(self.map, screen.get_size())  # Import de la map
        collision_total = tilemap.layers['evenements'].find('collision')  # Récupère toutes les collisions

        player = Player(tilemap, self.width, self.height)  # Appelle la class du joueur
        deplacer = Move(player, self.avancer, collision_total, self.collision_exist)  # Appelle la class de déplacement
        clock = pygame.time.Clock()  # Calcule le temps de départ pour les FPS

        while 1:  # Boucle infinie du jeu
            for event in pygame.event.get():    # Vérifie toutes les actions du joueur
                if event.type == pygame.QUIT:   # Clique pour quitter le jeu
                    pygame.quit()   # Quitte le jeu
                    exit()          # Quitte le processus python

            if pygame.key.get_pressed()[pygame.K_DOWN]:  # Touche " bas " appuyée
                deplacer.move_controller('bas')  # Appelle la fonction de vérification (collision, avancer, ...)

            elif pygame.key.get_pressed()[pygame.K_UP]:
                deplacer.move_controller('haut')

            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                deplacer.move_controller('gauche')

            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                deplacer.move_controller('droit')

            clock.tick(self.fps)  # Restreint les FPS
            tilemap.set_focus(player.player.x, player.player.y)  # Coordonnées du joueur par rapport aux bords
            tilemap.draw(screen)  # Affiche le fond
            screen.blit(player.sprite_player, (player.x, player.y))  # Affiche le joueur sur le fond
            pygame.display.flip()  # Met à jour l'écran


Game(1200, 800).main()  # Lance la boucle du jeu avec la taille choisie
