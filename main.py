exec(open("/Users/Naruhiko/PycharmProjects/PyDragon/libs/import.py").read()) # Add tmx to path (ignore this)

import pygame
from libs import tmx

# Configurations
WIDTH = 1200
HEIGHT = 700

PAS = 12
BASE_X = WIDTH/2
BASE_Y = HEIGHT/2

x = BASE_X
y = BASE_Y

# Accès aux images lié aux personnages
def selectSpirite(ligne, colonne, pixel_ligne = 32, pixel_colonne = 35):
    tileset = pygame.image.load('/Users/Naruhiko/PycharmProjects/PyDragon/ressources/sprites/characters/goku.png')
    return tileset.subsurface(pixel_ligne*ligne,pixel_colonne*colonne,pixel_ligne,pixel_colonne)

# Génère les collisions
def collision(player, list_collision):
    # Tous les événements avec l'argument " collision "
    for i in range(0, len(list_collision)-1):
        collision = list_collision[i]

        # Structure des données par rapport aux rectangles entourant les éléments :
        # horizontal : px gauche, px droit, px gauche-décalé
        # vertical : px bas, px haut, px bas-décalé
        rect_collision = [[collision.px, collision.px + collision.width, collision.px - collision.width], [collision.py, collision.py + collision.height, collision.py - collision.height]]
        # horizontal : px gauche, px droit (centre de l'image), px gauche-décalé (centre de l'image)
        # vertical : px bas, px haut
        rect_player = [[player.x, player.x + (player.width/2), player.x - (player.width/2)],[player.y, player.y + player.height]]

        # Joueur touche l'élément en X (venant par la droite) et Y (haut et bas)
        if rect_collision[0][2] < rect_player[0][1] < rect_collision[0][0] and rect_collision[1][0] < rect_player[1][1] < rect_collision[1][1]:
            return True
        # Joueur touche l'élément en X (venant par la gauche) et Y (haut et bas)
        elif rect_collision[0][0] < rect_player[0][1] < rect_collision[0][1] and rect_collision[1][0] < rect_player[1][1] < rect_collision[1][1]:
            return True


pygame.init() # Lance le jeu

screen = pygame.display.set_mode((WIDTH,HEIGHT)) # Défini la taille de l'écran

# Selection de la map + image du personnage
tilemap = tmx.load('/Users/Naruhiko/PycharmProjects/PyDragon/ressources/maps/kamehouse/map.tmx', screen.get_size())
image = selectSpirite(1,0)

# Element player avec son contour
start_cell = tilemap.layers['evenements'].find('player')[0]
rect = pygame.rect.Rect((start_cell.px, start_cell.py), image.get_size())

# Collision de la carte
all_collision = tilemap.layers['evenements'].find('collision')

# Element des contours
bord_gauche = tilemap.layers['evenements'].find('bord_gauche')[0]
bordure_g = bord_gauche.px+x

bord_droit = tilemap.layers['evenements'].find('bord_droit')[0]
bordure_d = bord_droit.px-x

bord_haut = tilemap.layers['evenements'].find('bord_haut')[0]
bordure_h = -bord_droit.py+y

bord_bas = tilemap.layers['evenements'].find('bord_bas')[0]
bordure_b = bord_droit.px-y

# Boucle du jeu
while 1:
    # Si la croix est cliquée
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # Bouton resté appuyé
    key = pygame.key.get_pressed()
    if key[pygame.K_RIGHT]:
        # Selection de l'image en fonction du déplacement
        image = selectSpirite(1, 2)
        # Collision avec un objet ?
        if collision(rect, all_collision):
            print('Collision')
        else:
            # Joueur proche d'une bordure
            if rect.x <= bordure_g or rect.x >= bordure_d:
                # Stop le suivi du joueur
                x += PAS
            # Joueur loin des bordures
            elif bordure_g <= rect.x <= bordure_d:
                # L'écran suit le joueur
                x = BASE_X
            # Le joueur avance
            rect.x += PAS

    elif key[pygame.K_LEFT]:
        image = selectSpirite(1, 1)
        if rect.x <= bordure_g or rect.x >= bordure_d:
            x -= PAS
        elif bordure_d >= rect.x >= bordure_g:
            x = BASE_X
        rect.x -= PAS

    elif key[pygame.K_UP]:
        image = selectSpirite(1, 3)
        if rect.y <= bordure_h or rect.y >= bordure_b:
            y -= PAS
        elif bordure_b >= rect.y >= bordure_h:
            y = BASE_Y
        rect.y -= PAS

    elif key[pygame.K_DOWN]:
        image = selectSpirite(1, 0)
        if rect.y <= bordure_h or rect.y >= bordure_b:
            y += PAS
        elif bordure_b >= rect.y >= bordure_h:
            y = BASE_Y
        rect.y += PAS

    tilemap.set_focus(rect[0], rect[1]) # Positionne le centre de l'écran
    tilemap.draw(screen) # Affiche le background
    screen.blit(image, (x, y)) # Supperpose les images
    pygame.display.flip() # Affiche le jeu et ses composantes