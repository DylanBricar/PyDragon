import os      # Import OS
import sys     # Import SYS

sys.path.append(os.getcwd() + "/libs")  # Ajout du chemin pour éviter les bugs Windows
import tmx  # Libraire TMX (bypass pour Python 2)

sys.path.append(os.getcwd() + "/classes")  # Ajout du chemin pour éviter les bugs Windows
from player import *  # Import de la class Player et des composantes liées
from sprite import *  # Import de la class Sprite et des composantes liées
from move import *    # Import de la class Move et des composantes liées
from niveau import *  # Import de la class Niveau et des composantes liées
from worldtown import *  # Import de la class Niveau et des composantes liées
from inventory import *  # Import de la class Inventory et des composantes liées


class Kamehouse:
    """ Gestion liée à l'extérieur de la map Kamehouse """

    def __init__(self, width, height, screen, clock, fps, avancer):
        """ Récupère les variables importantes depuis la class Game """
        self.width = width
        self.height = height
        self.screen = screen
        self.fps = fps
        self.clock = clock
        self.avancer = avancer

        self.while_map_kamehouse_in = False  # N'appelle par défaut pas la boucle de cette route
        self.while_map_town = False  # N'appelle par défaut pas la boucle de cette route

        self.while_map_kamehouse = True  # Boucle sur le menu affiché à l'utilisateur

    def while_kamehouse(self):
        """ Boucle sur la map Kamehouse """
        tilemap = tmx.load('ressources/maps/kamehouse/island/map.tmx', self.screen.get_size())  # Import de la map
        collision_total = tilemap.layers['evenements'].find('collision')  # Récupère toutes les collisions

        # Récupère toutes les collisions pour quitter le niveau
        exit_lvl = tilemap.layers['evenements'].find('exit')  # Intérieur de la maison
        goto_world = tilemap.layers['evenements'].find('exit_gotown')  # Vers la ville

        move = None  # Aucun déplacement n'est demandé par défaut
        old_pos_sprite = 'Down'  # Position par défaut du personnage (vers le bas)
        img_perso = Sprite()  # Défini la classe s'occupant des images des personnages
        player = Player(tilemap, self.width, self.height, img_perso, old_pos_sprite)  # Appelle la class du joueur
        deplacer = Move(player, self.avancer, collision_total)  # Appelle la class de déplacement
        inventory = Inventory(self.screen)  # Défini la classe de l'inventaire
        pygame.time.set_timer(pygame.USEREVENT, 300)  # Temps de mise à jour des Sprites (300 ms)

        if Niveau.COORDONNEE:  # S'il y a des données enregistrées (= sort de la maison)
            player.player.x = Niveau.COORDONNEE[0]  # On défini les nouvelles coordonnées en X
            player.player.y = Niveau.COORDONNEE[1]  # On défini les nouvelles coordonnées en Y

        while self.while_map_kamehouse:  # Boucle infinie du jeu
            collide_exit = CollisionController(player, exit_lvl)  # Appelle la class de collision pour quitter le niveau
            if collide_exit.collision():  # Si la collision avec la porte a lieu
                self.while_map_kamehouse = False  # Arrête la boucle de la map Kamehouse
                self.while_map_kamehouse_in = True  # Permet de lancer la boucle de la map Kamehouse_in
                Niveau.LVL = 'while_map_kamehouse_in'  # Nouvelle map appellée
                Niveau.COORDONNEE = [848, 1120]  # Localisation d'apparaission après être sorti de la maison

            collide_goto_world = CollisionController(player, goto_world)  # Appelle la class de collision pour quitter le niveau
            if collide_goto_world.collision():  # Si la collision avec la porte a lieu
                self.while_map_kamehouse = False  # Arrête la boucle de la map Kamehouse
                self.while_map_town = True  # Permet de lancer la boucle de la map Kamehouse_in
                Niveau.LVL = 'while_map_town'  # Nouvelle map appellée
                Niveau.COORDONNEE = [1205, 1215]  # Localisation d'apparaission après téléporation

            for event in pygame.event.get():  # Vérifie toutes les actions du joueur
                if event.type == pygame.QUIT:  # Clique pour quitter le jeu
                    self.while_map_kamehouse = False  # Quitte le processus python
                    Niveau.WHILE_GAME = False  # Ferme la boucle d'importation
                elif event.type == pygame.USEREVENT:  # Déplacement du joueur
                    player.sprite_player = img_perso.animate_sprite(move, old_pos_sprite)

            if pygame.key.get_pressed()[pygame.K_DOWN]:
                # Premier déplacement du personnage : il n'y a pas encore de mouvement ou la touche ne correspond pas
                direction_deplacement = 'Down'  # Variable de modification rapide
                if move is None or move != direction_deplacement:
                    player.sprite_player = img_perso.select_sprite(1, 0)  # Mise à jour première du Sprite
                    move = direction_deplacement  # Actualisation de la variable déplacement
                if Move.COLLIDED: move = None  # Empêche le déplacement du Sprite s'il y a une collision
                old_pos_sprite = direction_deplacement  # Ancienne position du joueur pour quand il s'arrêtera
                deplacer.move_player(player.player.copy(), [0, self.avancer], direction_deplacement)  # Déplacement

            elif pygame.key.get_pressed()[pygame.K_UP]:
                direction_deplacement = 'Up'
                if move is None or move != direction_deplacement:
                    player.sprite_player = img_perso.select_sprite(1, 3)
                    move = direction_deplacement
                if Move.COLLIDED: move = None  # Empêche le déplacement du Sprite s'il y a une collision
                old_pos_sprite = direction_deplacement
                deplacer.move_player(player.player.copy(), [0, -self.avancer], direction_deplacement)

            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                direction_deplacement = 'Left'
                if move is None or move != direction_deplacement:
                    player.sprite_player = img_perso.select_sprite(1, 1)
                    move = direction_deplacement
                if Move.COLLIDED: move = None  # Empêche le déplacement du Sprite s'il y a une collision
                old_pos_sprite = direction_deplacement
                deplacer.move_player(player.player.copy(), [-self.avancer, 0], direction_deplacement)

            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                direction_deplacement = 'Right'
                if move is None or move != direction_deplacement:
                    player.sprite_player = img_perso.select_sprite(1, 2)
                    move = direction_deplacement
                if Move.COLLIDED: move = None  # Empêche le déplacement du Sprite s'il y a une collision
                old_pos_sprite = direction_deplacement
                deplacer.move_player(player.player.copy(), [self.avancer, 0], direction_deplacement)
            else:
                move = None  # Arrêt de déplacement du personnage

            self.clock.tick(self.fps)  # Restreint les FPS
            tilemap.set_focus(player.player.x, player.player.y)  # Coordonnées du joueur par rapport aux bords
            tilemap.draw(self.screen)  # Affiche le fond
            self.screen.blit(player.sprite_player, (player.x, player.y))  # Affiche le joueur sur le fond

            if Niveau.INVENTORY:  # Si l'inventaire n'est pas vide
                inventory.show_item()  # Affiche l'inventaire du joueur

            pygame.display.flip()  # Met à jour l'écran
