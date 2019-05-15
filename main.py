import os      # Import OS
import sys     # Import SYS

import pygame  # Import PyGame

sys.path.append(os.getcwd() + "/libs")  # Ajout du chemin pour Windows
import tmx     # Libraire TMX (bypass pour Python 2)


class Sprite:
    def __init__(self):
        self.sprite_selected = pygame.image.load('ressources/sprites/characters/goku.png').convert_alpha()
        # Direction => Marche 1 | Marche 2 | Arret
        self.direction = {'Down': [[0, 0], [2, 0], [1, 0]], 'Up': [[0, 3], [2, 3], [1, 3]],
                          'Left': [[0, 1], [2, 1], [1, 1]], 'Right': [[0, 2], [2, 2], [1, 2]]}
        self.current_position = 1  # Direction de marche par défaut

    def select_sprite(self, ligne, colonne, pixel_ligne=32, pixel_colonne=35):
        """ Selectionne une case du sprite """
        return self.sprite_selected.subsurface(pixel_ligne * ligne, pixel_colonne * colonne, pixel_ligne, pixel_colonne)

    def animateSprite(self, move, old_pos_sprite):
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

        return new_img_sprite # Retourne le nouveau Sprite


class Player:
    """ Gestion du joueur """
    def __init__(self, tilemap, width, height, img_perso):
        self.tilemap = tilemap  # Récupère la map

        self.sprite_player = img_perso.select_sprite(1, 0)  # Génère le sprite de base
        joueur_pos = self.tilemap.layers['evenements'].find('player')[0]  # Trouve le joueur depuis la map
        self.player = pygame.rect.Rect((joueur_pos.px, joueur_pos.py), self.sprite_player.get_size())  # Crée son rectangle

        self.div_x_map = width/2   # Taille de la map en longueur divisée en deux
        self.div_y_map = height/2  # Taille de la map en largeur divisée en deux
        self.y = self.div_y_map    # Utilisé pour positionner le joueur (au centre vertical par défaut)
        self.x = self.div_x_map    # Utilisé pour positionner le joueur (au centre horizontal par défaut)


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
            # Aucune collision de trouvée : on ajuste le rendu de l'écran
            if touche == 'Left':
                if self.bord_droit >= self.player.player.x >= self.bord_gauche:
                    self.player.x = self.player.div_x_map  # Le joueur est centré sur la map
                # Le joueur se trouve proche d'une des deux extrémités de la map
                elif self.player.player.x <= self.bord_gauche or self.player.player.x >= self.bord_droit:
                    self.player.x -= self.pas  # Le joueur se rapproche du bord
            elif touche == 'Right':
                if self.player.player.x < self.bord_gauche or self.player.player.x > self.bord_droit:
                    self.player.x += self.pas
                elif self.bord_gauche > self.player.player.x > self.bord_droit:
                    self.player.x = self.player.div_x_map
            elif touche == 'Up':
                if self.player.player.y <= self.bord_haut or self.player.player.y >= self.bord_bas:
                    self.player.y -= self.pas
                elif self.bord_bas > self.player.player.y > self.bord_haut:
                    self.player.y = self.player.div_y_map
            elif touche == 'Down':
                if self.bord_haut > self.player.player.y > self.bord_bas:
                    self.player.y = self.player.div_y_map
                elif self.player.player.y <= self.bord_haut or self.player.player.y >= self.bord_bas:
                    self.player.y += self.pas



class Game:
    """ Gestion des imports du jeu """
    def __init__(self, width, height):
        self.width = width      # Largeur de la fenêtre de jeu
        self.height = height    # Hauteur de la fenêtre du jeu
        self.favicon = 'ressources/favicon.png'  # Chemin du favicon
        self.fps = 24  # FPS demandés
        self.avancer = 8.0  # Échelle de déplacement

    def main(self):
        """ Lancement du jeu """
        pygame.init()  # Lance de Pygame
        screen = pygame.display.set_mode((self.width, self.height))  # Crée la fenêtre
        pygame.display.set_caption('PyDragon v0.1')  # Donne un nom à la fenêtre
        pygame.display.set_icon(pygame.image.load(self.favicon))  # Favicon du jeu
        clock = pygame.time.Clock()  # Calcule le temps de départ pour les FPS

        main_menu = MainMenu(screen, clock, self.fps)  # Instancie la class qui affiche récupère le menu
        main_menu.while_menu()  # Boucle sur le menu via la fonction dans la class
        map_got = main_menu.get_running('while_map_kamehouse')  # Récupère la valeur de get_running afin de savoir comment réagir
        if map_got == 'while_map_kamehouse':  # Le joueur a choisi de jouer sur la map kamehouse
            map_kamehouse = Kamehouse(self.width, self.height, screen, clock, self.fps, self.avancer)  # Instancie
            map_kamehouse.while_kamehouse()  # Boucle sur la map
            map_got = map_kamehouse.get_running('while_map_kamehouse_in')  # Récupère la nouvelle direction
            if map_got == 'while_map_kamehouse_in':  # Le joueur a choisi de jouer sur la map kamehouse_in
                map_kamehouse_in = KamehouseIn(self.width, self.height, screen, clock, self.fps, self.avancer)  # Instancie
                map_kamehouse_in.while_kamehouse_in()  # Boucle sur la map
                map_got = map_kamehouse_in.get_running('while_map_kamehouse')  # Récupère la nouvelle direction
                if map_got == 'while_map_kamehouse':  # Le joueur a choisi de jouer sur la map kamehouse
                    map_kamehouse = Kamehouse(self.width, self.height, screen, clock, self.fps, self.avancer)  # Instancie
                    map_kamehouse.while_kamehouse()  # Boucle sur la map
                    map_got = map_kamehouse.get_running('while_map_kamehouse_in')  # Récupère la nouvelle direction

        pygame.quit()


class Kamehouse:
    """ Affiche la map Kamehouse """
    def __init__(self, width, height, screen, clock, fps, avancer):
        """ Récupère les variables importantes """
        self.width = width
        self.height = height
        self.screen = screen
        self.fps = fps
        self.clock = clock
        self.avancer = avancer

        self.while_map_kamehouse_in = False  # N'appelle par défaut pas la boucle de cette route

        self.while_map_kamehouse = True  # Boucle sur le menu affiché à l'utilisateur

    def get_running(self, var_name):
        """ Retourne la variable de la map appelée pour boucler sur cette dernière """
        if var_name == 'while_map_kamehouse_in' and self.while_map_kamehouse_in:
            return var_name

    def while_kamehouse(self):
        """ Boucle sur la map Kamehouse """
        tilemap = tmx.load('ressources/maps/kamehouse/island/map.tmx', self.screen.get_size())  # Import de la map
        collision_total = tilemap.layers['evenements'].find('collision')  # Récupère toutes les collisions
        exit_lvl = tilemap.layers['evenements'].find('exit')  # Récupère toutes les collisions pour quitter le niveau

        move = None  # Aucun déplacement n'est demandé par défaut
        old_pos_sprite = 'Down' # Position par défaut du personnage (vers le bas)
        img_perso = Sprite()  # Défini la classe s'occupant des images des personnages
        player = Player(tilemap, self.width, self.height, img_perso)  # Appelle la class du joueur
        deplacer = Move(player, self.avancer, collision_total)  # Appelle la class de déplacement
        pygame.time.set_timer(pygame.USEREVENT, 300)  # Temps de mise à jour des Sprites (300 ms)

        while self.while_map_kamehouse:  # Boucle infinie du jeu

            collide_exit = CollisionController(player, exit_lvl)  # Appelle la class de collision pour quitter le niveau
            if collide_exit.collision():  # Si la collision avec la porte a lieu
                self.while_map_kamehouse = False  # Arrête la boucle de la map Kamehouse
                self.while_map_kamehouse_in = True  # Permet de lancer la boucle de la map Kamehouse_in

            for event in pygame.event.get():  # Vérifie toutes les actions du joueur
                if event.type == pygame.QUIT:  # Clique pour quitter le jeu
                    self.while_map_kamehouse = False  # Quitte le processus python
                elif event.type == pygame.USEREVENT:  # Déplacement du joueur
                    player.sprite_player = img_perso.animateSprite(move, old_pos_sprite)

            if pygame.key.get_pressed()[pygame.K_DOWN]:
                # Premier déplacement du personnage : il n'y a pas encore de mouvement ou la touche ne correspond pas
                direction_deplacement = 'Down'  # Variable de modification rapide
                if move is None or move != direction_deplacement:
                    player.sprite_player = img_perso.select_sprite(1, 0)  # Mise à jour première du Sprite
                    move = direction_deplacement  # Actualisation de la variable déplacement
                old_pos_sprite = direction_deplacement  # Ancienne position du joueur pour quand il s'arrêtera
                deplacer.move_player(player.player.copy(), [0, self.avancer], direction_deplacement)  # Déplacement

            elif pygame.key.get_pressed()[pygame.K_UP]:
                direction_deplacement = 'Up'
                if move is None or move != direction_deplacement:
                    player.sprite_player = img_perso.select_sprite(1, 3)
                    move = direction_deplacement
                old_pos_sprite = direction_deplacement
                deplacer.move_player(player.player.copy(), [0, -self.avancer], direction_deplacement)

            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                direction_deplacement = 'Left'
                if move is None or move != direction_deplacement:
                    player.sprite_player = img_perso.select_sprite(1, 1)
                    move = direction_deplacement
                old_pos_sprite = direction_deplacement
                deplacer.move_player(player.player.copy(), [-self.avancer, 0], direction_deplacement)

            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                direction_deplacement = 'Right'
                if move is None or move != direction_deplacement:
                    player.sprite_player = img_perso.select_sprite(1, 2)
                    move = direction_deplacement
                old_pos_sprite = direction_deplacement
                deplacer.move_player(player.player.copy(), [self.avancer, 0], direction_deplacement)
            else:
                move = None  # Arrêt de déplacement du personnage

            self.clock.tick(self.fps)  # Restreint les FPS
            tilemap.set_focus(player.player.x, player.player.y)  # Coordonnées du joueur par rapport aux bords
            tilemap.draw(self.screen)  # Affiche le fond
            self.screen.blit(player.sprite_player, (player.x, player.y))  # Affiche le joueur sur le fond
            pygame.display.flip()  # Met à jour l'écran


class KamehouseIn:
    """ Affiche la map Kamehouse """
    def __init__(self, width, height, screen, clock, fps, avancer):
        """ Récupère les variables importantes """
        self.width = width
        self.height = height
        self.screen = screen
        self.fps = fps
        self.clock = clock
        self.avancer = avancer

        self.while_map_kamehouse = False  # N'appelle par défaut pas la boucle de cette route

        self.while_map_kamehouse_in = True  # Boucle sur le menu affiché à l'utilisateur

    def get_running(self, var_name):
        """ Retourne la variable de la map appelée pour boucler sur cette dernière """
        if var_name == 'while_map_kamehouse' and self.while_map_kamehouse:
            return var_name

    def while_kamehouse_in(self):
        """ Boucle sur la map Kamehouse """
        tilemap = tmx.load('ressources/maps/kamehouse/house/map.tmx', self.screen.get_size())  # Import de la map
        collision_total = tilemap.layers['evenements'].find('collision')  # Récupère toutes les collisions
        exit_lvl = tilemap.layers['evenements'].find('exit')  # Récupère toutes les collisions pour quitter le niveau

        move = None  # Aucun déplacement n'est demandé par défaut
        old_pos_sprite = 'Down' # Position par défaut du personnage (vers le bas)
        img_perso = Sprite()  # Défini la classe s'occupant des images des personnages
        player = Player(tilemap, self.width, self.height, img_perso)  # Appelle la class du joueur
        deplacer = Move(player, self.avancer, collision_total)  # Appelle la class de déplacement
        pygame.time.set_timer(pygame.USEREVENT, 300)  # Temps de mise à jour des Sprites (300 ms)

        while self.while_map_kamehouse_in:  # Boucle infinie du jeu

            collide_exit = CollisionController(player, exit_lvl)  # Appelle la class de collision pour quitter le niveau
            if collide_exit.collision():  # Si la collision avec la porte a lieu
                self.while_map_kamehouse_in = False  # Arrête la boucle de la map Kamehouse
                self.while_map_kamehouse = True  # Permet de lancer la boucle de la map Kamehouse

            for event in pygame.event.get():  # Vérifie toutes les actions du joueur
                if event.type == pygame.QUIT:  # Clique pour quitter le jeu
                    self.while_map_kamehouse_in = False  # Quitte le processus python
                elif event.type == pygame.USEREVENT:  # Déplacement du joueur
                    player.sprite_player = img_perso.animateSprite(move, old_pos_sprite)

            if pygame.key.get_pressed()[pygame.K_DOWN]:
                # Premier déplacement du personnage : il n'y a pas encore de mouvement ou la touche ne correspond pas
                direction_deplacement = 'Down'  # Variable de modification rapide
                if move is None or move != direction_deplacement:
                    player.sprite_player = img_perso.select_sprite(1, 0)  # Mise à jour première du Sprite
                    move = direction_deplacement  # Actualisation de la variable déplacement
                old_pos_sprite = direction_deplacement  # Ancienne position du joueur pour quand il s'arrêtera
                deplacer.move_player(player.player.copy(), [0, self.avancer], direction_deplacement)  # Déplacement

            elif pygame.key.get_pressed()[pygame.K_UP]:
                direction_deplacement = 'Up'
                if move is None or move != direction_deplacement:
                    player.sprite_player = img_perso.select_sprite(1, 3)
                    move = direction_deplacement
                old_pos_sprite = direction_deplacement
                deplacer.move_player(player.player.copy(), [0, -self.avancer], direction_deplacement)

            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                direction_deplacement = 'Left'
                if move is None or move != direction_deplacement:
                    player.sprite_player = img_perso.select_sprite(1, 1)
                    move = direction_deplacement
                old_pos_sprite = direction_deplacement
                deplacer.move_player(player.player.copy(), [-self.avancer, 0], direction_deplacement)

            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                direction_deplacement = 'Right'
                if move is None or move != direction_deplacement:
                    player.sprite_player = img_perso.select_sprite(1, 2)
                    move = direction_deplacement
                old_pos_sprite = direction_deplacement
                deplacer.move_player(player.player.copy(), [self.avancer, 0], direction_deplacement)
            else:
                move = None  # Arrêt de déplacement du personnage

            self.clock.tick(self.fps)  # Restreint les FPS
            tilemap.set_focus(player.player.x, player.player.y)  # Coordonnées du joueur par rapport aux bords
            tilemap.draw(self.screen)  # Affiche le fond
            self.screen.blit(player.sprite_player, (player.x, player.y))  # Affiche le joueur sur le fond
            pygame.display.flip()  # Met à jour l'écran


class MainMenu:
    """ Menu de lancement du jeu """

    def __init__(self, screen, clock, fps):
        """ Récupère les variables importantes """
        self.screen = screen
        self.fps = fps
        self.clock = clock

        self.while_map_kamehouse = False  # N'appelle par défaut pas la boucle de cette route
        self.while_options = False  # N'appelle par défaut pas la boucle sur cette route

        self.while_main_menu = True  # Boucle sur le menu affiché à l'utilisateur

    def get_running(self, var_name):
        """ Retourne la variable de la map appelée pour boucler sur cette dernière """
        if var_name == 'while_map_kamehouse' and self.while_map_kamehouse:
            return var_name

    def while_menu(self):
        """ Boucle sur le menu """
        tilemap = tmx.load('ressources/maps/kamehouse/island/map.tmx', self.screen.get_size())  # Import de la map
        tilemap.set_focus(0, 0)  # Coordonnées du joueur par rapport aux bords

        while self.while_main_menu:  # Boucle infinie du menu

            for event in pygame.event.get():  # Vérifie toutes les actions du joueur
                if event.type == pygame.QUIT:  # Clique pour quitter le jeu
                    self.while_main_menu = False  # Quitte le processus python

            if pygame.key.get_pressed()[pygame.K_DOWN]:
                # La touche du bas est préssée pour changer de fenêtre
                self.while_main_menu = False  # Arrête la boucle du menu
                self.while_map_kamehouse = True  # Permet de lancer la boucle du jeu

            self.clock.tick(self.fps)  # Restreint les FPS
            tilemap.draw(self.screen)  # Affiche le fond
            pygame.display.flip()  # Met à jour l'écran


if __name__ == '__main__':
    Game(750, 450).main()  # Lance la boucle du jeu avec la taille choisie