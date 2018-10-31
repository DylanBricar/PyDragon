exec(open("/Users/Naruhiko/PycharmProjects/PyDragon/libs/import.py").read()) # Add tmx to path (ignore this)

import pygame
from libs import tmx

WIDTH = 1200
HEIGHT = 700

PAS = 12
BASE_X = WIDTH/2
BASE_Y = HEIGHT/2

x = BASE_X
y = BASE_Y

pygame.init()

def selectSpirite(ligne, colonne, pixel_ligne = 32, pixel_colonne = 35):
    tileset = pygame.image.load('/Users/Naruhiko/PycharmProjects/PyDragon/ressources/sprites/characters/goku.png')
    return tileset.subsurface(pixel_ligne*ligne,pixel_colonne*colonne,pixel_ligne,pixel_colonne)

screen = pygame.display.set_mode((WIDTH,HEIGHT))

tilemap = tmx.load('/Users/Naruhiko/PycharmProjects/PyDragon/ressources/maps/kamehouse/map.tmx', screen.get_size())

image = selectSpirite(1,0)

start_cell = tilemap.layers['evenements'].find('player')[0]
rect = pygame.rect.Rect((start_cell.px, start_cell.py), image.get_size())

bord_gauche = tilemap.layers['evenements'].find('bord_gauche')[0]
bordure_g = bord_gauche.px+x

bord_droit = tilemap.layers['evenements'].find('bord_droit')[0]
bordure_d = bord_droit.px-x

bord_haut = tilemap.layers['evenements'].find('bord_haut')[0]
bordure_h = -bord_droit.py+y

bord_bas = tilemap.layers['evenements'].find('bord_bas')[0]
bordure_b = bord_droit.px-y

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    key = pygame.key.get_pressed()
    if key[pygame.K_RIGHT]:
        image = selectSpirite(1, 2)
        if rect.x <= bordure_g or rect.x >= bordure_d:
            x += PAS
        elif bordure_g <= rect.x <= bordure_d:
            x = BASE_X
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

    tilemap.set_focus(rect[0], rect[1])

    tilemap.draw(screen)

    screen.blit(image, (x, y))

    pygame.display.flip()