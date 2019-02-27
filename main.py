import pygame  # Import PyGame
import sys     # Import SYS
import os      # Import OS
sys.path.append(os.getcwd() + "/libs") # Ajout du chemin pour Windows
import tmx     # Libraire TMX (bypass pour Python 2)


class Sprite:
    def __init__(self):
        self.sprite_selected = pygame.image.load('ressources/sprites/characters/vegeta.png').convert_alpha()

    def select_sprite(self, ligne, colonne, pixel_ligne=32, pixel_colonne=35):
        """ Selectionne une case du sprite """
        return self.sprite_selected.subsurface(pixel_ligne * ligne, pixel_colonne * colonne, pixel_ligne, pixel_colonne)


class Player:
    """ Gestion du joueur """
    def __init__(self, tilemap, width, height, img_perso):
        self.tilemap = tilemap  # Récupère la map

        self.sprite_player = img_perso.select_sprite(1, 0)  # Génère le sprite de base
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
        # Retourne False ou True si une collision a été ou non trouvée
        return any(((self.player.player.x < collision_selected.px + collision_selected.width)       # Trop à droite
                    and (self.player.player.x + self.player.player.w > collision_selected.px)       # Trop à gauche
                    and (self.player.player.y < collision_selected.py + collision_selected.height)  # Trop en bas
                    and (self.player.player.y + self.player.player.h > collision_selected.py))      # Trop en haut
                   for collision_selected in self.total_collision)  # Boucle les collisions


class Move:
    """ Déplacement du joueur """
    def __init__(self, player, pas, collision):
        self.player = player  # Toutes les informations de la class player
        self.pas = pas  # Déplacement qui doit être fait
        self.collision = collision  # Liste de toutes les collisions

        # Bords de la map
        self.bord_haut = self.player.div_y_map
        self.bord_bas = self.player.tilemap.px_height - self.player.div_y_map
        self.bord_gauche = self.player.div_x_map
        self.bord_droit = self.player.tilemap.px_width - self.player.div_x_map

    def move_player(self, old_position, direction, touche):
        """ Déplace le joueur en fonction de la touche """
        self.player.player.move_ip(direction)  # Déplace le joueur en y ajoutant la direction donnée
        collide = CollisionController(self.player, self.collision)  # Appelle la class de collision

        if collide.collision():
            # Si collision, on restaure la position de départ
            self.player.player = old_position
        else:
            # Aucune collison de trouvée : on ajuste le rendu de l'écran
            if touche == 'gauche':
                if self.bord_droit >= self.player.player.x >= self.bord_gauche:
                    self.player.x = self.player.div_x_map  # Le joueur est centré sur la map
                # Le joueur se trouve proche d'une des deux extrémités de la map
                elif self.player.player.x <= self.bord_gauche or self.player.player.x >= self.bord_droit:
                    self.player.x -= self.pas  # Le joueur se rapproche du bord
            elif touche == 'droit':
                if self.player.player.x < self.bord_gauche or self.player.player.x > self.bord_droit:
                    self.player.x += self.pas
                elif self.bord_gauche > self.player.player.x > self.bord_droit:
                    self.player.x = self.player.div_x_map
            elif touche == 'haut':
                if self.player.player.y <= self.bord_haut or self.player.player.y >= self.bord_bas:
                    self.player.y -= self.pas
                elif self.bord_bas > self.player.player.y > self.bord_haut:
                    self.player.y = self.player.div_y_map
            elif touche == 'bas':
                if self.bord_haut > self.player.player.y > self.bord_bas:
                    self.player.y = self.player.div_y_map
                elif self.player.player.y <= self.bord_haut or self.player.player.y >= self.bord_bas:
                    self.player.y += self.pas


class Game:
    """ Gestion des imports du jeu """
    def __init__(self, width, height):
        self.width = width      # Largeur de la fenêtre de jeu
        self.height = height    # Hauteur de la fenêtre du jeu
        self.map = 'ressources/maps/kamehouse/map.tmx'  # Chemin de la map
        self.favicon = 'ressources/favicon.png'  # Chemin du favicon
        self.fps = 24  # FPS demandés
        self.avancer = 8.0  # Échelle de déplacement

    def main(self):
        """ Lancement du jeu """
        pygame.init()  # Lance de Pygame
        screen = pygame.display.set_mode((self.width, self.height))  # Crée la fenêtre
        pygame.display.set_caption('PyDragon v0.1')  # Donne un nom à la fenêtre
        pygame.display.set_icon(pygame.image.load(self.favicon))  # Favicon du jeu
        tilemap = tmx.load(self.map, screen.get_size())  # Import de la map
        collision_total = tilemap.layers['evenements'].find('collision')  # Récupère toutes les collisions

        img_perso = Sprite()  # Défini la classe s'occupant des images des personnages
        player = Player(tilemap, self.width, self.height, img_perso)  # Appelle la class du joueur
        deplacer = Move(player, self.avancer, collision_total)  # Appelle la class de déplacement
        clock = pygame.time.Clock()  # Calcule le temps de départ pour les FPS

        running = True
        while running:  # Boucle infinie du jeu
            for event in pygame.event.get():    # Vérifie toutes les actions du joueur
                if event.type == pygame.QUIT:   # Clique pour quitter le jeu
                    running = False             # Quitte le processus python

            if pygame.key.get_pressed()[pygame.K_DOWN]:
                deplacer.move_player(player.player.copy(), [0, self.avancer], 'bas')
                player.sprite_player = img_perso.select_sprite(1, 0)

            elif pygame.key.get_pressed()[pygame.K_UP]:
                deplacer.move_player(player.player.copy(), [0, -self.avancer], 'haut')
                player.sprite_player = img_perso.select_sprite(1, 3)

            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                deplacer.move_player(player.player.copy(), [-self.avancer, 0], 'gauche')
                player.sprite_player = img_perso.select_sprite(1, 1)

            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                deplacer.move_player(player.player.copy(), [self.avancer, 0], 'droit')
                player.sprite_player = img_perso.select_sprite(1, 2)

            clock.tick(self.fps)  # Restreint les FPS
            tilemap.set_focus(player.player.x, player.player.y)  # Coordonnées du joueur par rapport aux bords
            tilemap.draw(screen)  # Affiche le fond
            screen.blit(player.sprite_player, (player.x, player.y))  # Affiche le joueur sur le fond
            pygame.display.flip()  # Met à jour l'écran

        pygame.quit()

if __name__ == '__main__':
    Game(750, 450).main()  # Lance la boucle du jeu avec la taille choisie