import pygame
from libs import tmx

# Taille de la fenêtre
WIDTH = 1200
HEIGHT = 800

# X,Y par défaut (au centre de l'écran)
x = WIDTH / 2
y = HEIGHT / 2

# FPS + PAS
FPS = 60
PAS = 180.0


def select_sprite(ligne, colonne, pixel_ligne=32, pixel_colonne=35):
    """Selection d'une case du sprite"""
    sprite_selected = pygame.image.load('ressources/sprites/characters/goku.png')
    return sprite_selected.subsurface(pixel_ligne * ligne, pixel_colonne * colonne, pixel_ligne, pixel_colonne)


def collision(player, list_collision):
    """Retourne 'false' s'il y a une collision repérée"""
    for i in range(0, len(list_collision) - 1):
        collision_selected = list_collision[i]

        if ((player.x >= collision_selected.px + collision_selected.width)  # Trop à droite
                or (player.x + player.w <= collision_selected.px)  # Trop à gauche
                or (player.y >= collision_selected.py + collision_selected.height)  # Trop en bas
                or (player.y + player.h <= collision_selected.py)):  # Trop en haut
            var = False
        else:
            var = True

        if var:
            return False


def move(player, run, direction, collision_total):
    """Déplace le joueur vers la direction donnée"""
    global y
    global x
    global sprite_player

    bordure_h = 0 + HEIGHT / 2
    bordure_b = tilemap.px_height - HEIGHT / 2
    bordure_g = 0 + WIDTH / 2
    bordure_d = tilemap.px_width - WIDTH / 2

    if direction == 'bas':
        sprite_player = select_sprite(1, 0)

        if bordure_h > player.y > bordure_b:
            y = HEIGHT / 2
        elif player.y <= bordure_h or player.y >= bordure_b:
            y += run
        player.y += run

    elif direction == 'haut':
        sprite_player = select_sprite(1, 3)

        if player.y <= bordure_h or player.y >= bordure_b:
            y -= run
        elif bordure_b > player.y > bordure_h:
            y = HEIGHT / 2
        player.y -= run

    elif direction == 'gauche':
        sprite_player = select_sprite(1, 1)

        if bordure_d >= player.x >= bordure_g:
            x = WIDTH / 2
        elif player.x <= bordure_g or player.x >= bordure_d:
            x -= run
        player.x -= run

    elif direction == 'droit':
        sprite_player = select_sprite(1, 2)

        if collision(player, collision_total) is False:
            print("Collision à droite")
        else:
            if player.x < bordure_g or player.x > bordure_d:
                x += run
            elif bordure_g > player.x > bordure_d:
                x = WIDTH / 2
            player.x += run


def main():
    """Appel aux fonctions pour lancer le jeu"""
    global y
    global x
    global sprite_player
    global tilemap

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    tilemap = tmx.load('ressources/maps/kamehouse/map.tmx', screen.get_size())

    sprite_player = select_sprite(1, 0)
    player_pos = tilemap.layers['evenements'].find('player')[0]
    player = pygame.rect.Rect((player_pos.px, player_pos.py), sprite_player.get_size())

    # Collision de la carte
    collision_total = tilemap.layers['evenements'].find('collision')

    clock = pygame.time.Clock()

    while 1:
        delta_ms = clock.tick(FPS)
        run = int(PAS * (delta_ms / 1000.0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            move(player, run, 'droit', collision_total)

        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            move(player, run, 'gauche', collision_total)

        elif pygame.key.get_pressed()[pygame.K_UP]:
            move(player, run, 'haut', collision_total)

        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            move(player, run, 'bas', collision_total)

        tilemap.set_focus(player.x, player.y)   # Joueur au centre de l'écran
        tilemap.draw(screen)                    # Affiche le fond
        screen.blit(sprite_player, (x, y))      # Affiche le joueur sur le fond
        pygame.display.flip()                   # Affiche le jeu et ses composantes


# Lance le jeu
if __name__ == '__main__':
    main()