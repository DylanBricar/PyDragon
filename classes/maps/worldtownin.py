import os      # Import OS
import sys     # Import SYS
from math import ceil  # Import ceil

sys.path.append(os.getcwd() + "/libs")  # Ajout du chemin pour éviter les bugs Windows
import tmx  # Libraire TMX (bypass pour Python 2)

sys.path.append(os.getcwd() + "/classes")  # Ajout du chemin pour éviter les bugs Windows
from player import *  # Import de la class Player et des composantes liées
from sprite import *  # Import de la class Sprite et des composantes liées
from move import *    # Import de la class Move et des composantes liées
from niveau import *  # Import de la class Niveau et des composantes liées
from interact import *  # Import de la class Interact et des composantes liées
from inventory import *  # Import de la class Inventory et des composantes liées

sys.path.append(os.getcwd() + "/ressources")  # Ajout du chemin pour éviter les bugs Windows
from missions import *  # Import des variables de textes des missions


class WorldTownIn:
    """ Gestion liée à l'extérieur de la map WorldTownIn """

    def __init__(self, width, height, screen, clock, fps, avancer):
        """ Récupère les variables importantes depuis la class Game """
        self.width = width
        self.height = height
        self.screen = screen
        self.fps = fps
        self.clock = clock
        self.avancer = avancer

        self.while_map_town = False  # N'appelle par défaut pas la boucle de cette route

        self.while_map_town_in = True  # Boucle sur la carte à afficher à l'utilisateur

    def while_town_in(self):
        """ Boucle sur la map WorldTownIn """
        tilemap = tmx.load('ressources/maps/worldtown/house/map.tmx', self.screen.get_size())  # Import de la map
        collision_total = tilemap.layers['evenements'].find('collision')  # Récupère toutes les collisions
        collision_person = tilemap.layers['evenements'].find('collision_person')  # Récupère les collisions avec le personnage
        exit_lvl = tilemap.layers['evenements'].find('exit')  # Quitte la maison

        move = None  # Aucun déplacement n'est demandé par défaut
        old_pos_sprite = 'Down'  # Position par défaut du personnage (vers le bas)
        img_perso = Sprite()  # Défini la classe s'occupant des images des personnages
        player = Player(tilemap, self.width, self.height, img_perso, old_pos_sprite)  # Appelle la class du joueur
        deplacer = Move(player, self.avancer, collision_total)  # Appelle la class de déplacement
        dialogue = Interact(self.screen)  # Défini la classe de dialogue
        inventory = Inventory(self.screen)  # Défini la classe de l'inventaire
        pygame.time.set_timer(pygame.USEREVENT, 300)  # Temps de mise à jour des Sprites (300 ms)

        while self.while_map_town_in:  # Boucle infinie du jeu
            collide_exit = CollisionController(player, exit_lvl)  # Class de collision pour quitter le niveau
            collide_person = CollisionController(player, collision_person)  # Class de collision pour parler avec le personnage
            if collide_exit.collision():  # Si la collision avec la porte a lieu
                self.while_map_town_in = False  # Arrête la boucle de la map Kamehouse
                self.while_map_town = True  # Permet de lancer la boucle de la map Kamehouse_in
                Niveau.LVL = 'while_map_town'  # Nouvelle map appellée

            for event in pygame.event.get():  # Vérifie toutes les actions du joueur
                if event.type == pygame.QUIT:  # Clique pour quitter le jeu
                    self.while_map_town_in = False  # Quitte le processus python
                    Niveau.WHILE_GAME = False  # Ferme la boucle d'importation
                elif event.type == pygame.USEREVENT:  # Déplacement du joueur
                    player.sprite_player = img_perso.animate_sprite(move, old_pos_sprite)  # Anime le joueur
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and collide_person.collision() and not Niveau.DIALOGUE:
                    # Si la touche espace est préssée, qu'il y a une collision et qu'il n'y a pas de boite de dialogue
                        Niveau.DIALOGUE = True  # On défini la variable pour l'afficher
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and Niveau.DIALOGUE:
                    # Si la touche espace est préssée et qu'il n'y a une boite de dialogue affichée
                    if Niveau.MISSION_01 == 0:
                        calcul = ceil(len(txt_mission01_02) / 4)  # Calcul le nombre de page en fonction du dialogue
                    elif Niveau.MISSION_01 == 50:
                        calcul = ceil(len(txt_mission01_05) / 4)  # Calcul le nombre de page en fonction du dialogue
                    elif Niveau.MISSION_01 == 100:
                        calcul = ceil(len(txt_mission01_06) / 4)  # Calcul le nombre de page en fonction du dialogue

                    if Niveau.PAGE == calcul:  # Nombre de page maximum des dialogues est atteint
                        Niveau.DIALOGUE = False  # On ferme la boite de dialogue
                        Niveau.PAGE = 1  # Redéfini la page à 1

                        if Niveau.MISSION_01 == 0:  # Si la mission est à 0%
                            Niveau.MISSION_01 = 50  # Évolue l'état de la mission 1 à 50% achevée
                            Niveau.INVENTORY.append('boulecristal')  # Ajoute l'objet obtenu
                    else:  # Pas encore toutes les pages sont lues
                        Niveau.PAGE = Niveau.PAGE + 1  # Ajoute +1 aux pages

            if not Niveau.DIALOGUE:  # Aucune boite de dialogue n'est affichée
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
            else:  # Une boite de dialogue est affichée
                move = None  # Arrêt de déplacement du personnage

            self.clock.tick(self.fps)  # Restreint les FPS
            tilemap.set_focus(player.player.x, player.player.y)  # Coordonnées du joueur par rapport aux bords
            tilemap.draw(self.screen)  # Affiche le fond
            self.screen.blit(player.sprite_player, (player.x, player.y))  # Affiche le joueur sur le fond

            if Niveau.DIALOGUE:  # Si la variable de dialogue est définie
                if Niveau.MISSION_01 == 0:  # La mission n'a pas encore commencée
                    dialogue.show_box(txt_mission01_02)  # Affiche le dialogue pour la mission 1
                elif Niveau.MISSION_01 == 50:
                    dialogue.show_box(txt_mission01_05)  # Affiche le dialogue pour la mission 1
                elif Niveau.MISSION_01 == 100:
                    dialogue.show_box(txt_mission01_06)  # Affiche le dialogue pour la mission 1

            if Niveau.INVENTORY:  # Si l'inventaire n'est pas vide
                inventory.show_item()  # Affiche l'inventaire du joueur

            pygame.display.flip()  # Met à jour l'écran
