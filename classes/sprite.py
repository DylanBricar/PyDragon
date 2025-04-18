import pygame


class Sprite:
    """ Sprite and animation management """

    DEBUG_LOGGING = False

    SHOW_BOUNDARY_WARNINGS = False

    def __init__(self):
        self.sprite_type = 0
        try:
            self.sprite_selected = pygame.image.load('ressources/sprites/characters/goku.png').convert_alpha()
            sprite_width = self.sprite_selected.get_width()
            sprite_height = self.sprite_selected.get_height()
            if Sprite.DEBUG_LOGGING:
                print(f"Goku sprite loaded: dimensions {sprite_width}x{sprite_height} pixels")

            self.goku_transformed_offset_x = 3 * 32

            if Sprite.DEBUG_LOGGING:
                print("Info: Transformed Goku offset set to", self.goku_transformed_offset_x)
        except Exception as e:
            print(f"Error loading Goku sprite: {e}")

            self.sprite_selected = pygame.Surface((96, 140))
            self.sprite_selected.fill((255, 0, 0))
            self.goku_transformed_offset_x = 0

        self.direction = {'Down': [[0, 0], [2, 0], [1, 0]], 'Up': [[0, 3], [2, 3], [1, 3]],
                          'Left': [[0, 1], [2, 1], [1, 1]], 'Right': [[0, 2], [2, 2], [1, 2]]}
        self.current_position = 1

        self.last_debug_message = ""

        self.error_count = 0

    def change_sprite(self, sprite_type):
        """ Change character sprite """
        self.sprite_type = sprite_type

        if sprite_type == 0:
            try:
                self.sprite_selected = pygame.image.load('ressources/sprites/characters/goku.png').convert_alpha()
                if Sprite.DEBUG_LOGGING:
                    print(
                        f"Normal Goku sprite loaded: dimensions {self.sprite_selected.get_width()}x{self.sprite_selected.get_height()} pixels")

                self.goku_transformed_offset_x = 0
            except Exception as e:
                print(f"Error loading normal Goku sprite: {e}")
        elif sprite_type == 1:
            try:

                self.sprite_selected = pygame.image.load('ressources/sprites/characters/goku.png').convert_alpha()
                if Sprite.DEBUG_LOGGING:
                    sprite_width = self.sprite_selected.get_width()
                    sprite_height = self.sprite_selected.get_height()
                    print(f"Transformed Goku sprite: dimensions {sprite_width}x{sprite_height} pixels")

                self.goku_transformed_offset_x = 3 * 32
                if Sprite.DEBUG_LOGGING:
                    print(f"Super Saiyan offset set to {self.goku_transformed_offset_x}")
            except Exception as e:
                print(f"Error loading transformed Goku sprite: {e}")
                self.sprite_type = 0
                self.goku_transformed_offset_x = 0
        elif sprite_type == 2:
            try:
                self.sprite_selected = pygame.image.load('ressources/sprites/characters/vegeta.png').convert_alpha()
                if Sprite.DEBUG_LOGGING:
                    print(
                        f"Vegeta sprite loaded: dimensions {self.sprite_selected.get_width()}x{self.sprite_selected.get_height()} pixels")

                self.goku_transformed_offset_x = 0
            except Exception as e:
                print(f"Error loading Vegeta sprite: {e}")

        self.error_count = 0
        return self.sprite_type

    def select_sprite(self, line, column, pixel_line=32, pixel_column=35):
        """ Select a sprite frame """

        if self.sprite_type == 1:
            x = self.goku_transformed_offset_x + (pixel_line * line)
        else:
            x = pixel_line * line

        y = pixel_column * column

        sprite_width = self.sprite_selected.get_width()
        sprite_height = self.sprite_selected.get_height()

        debug_msg = f"type={self.sprite_type}, coords=({x}, {y})"

        if Sprite.DEBUG_LOGGING and line == 1 and column == 0 and debug_msg != self.last_debug_message:
            print(f"Sprite selection: {debug_msg}, sprite_size=({sprite_width}, {sprite_height})")
            self.last_debug_message = debug_msg

        if x + pixel_line > sprite_width:
            x = sprite_width - pixel_line
            if Sprite.SHOW_BOUNDARY_WARNINGS and self.error_count % 50 == 0:
                print(f"X adjustment: ({x}, {y}), limits: ({sprite_width}, {sprite_height})")
            self.error_count += 1

        if y + pixel_column > sprite_height:
            y = sprite_height - pixel_column
            if Sprite.SHOW_BOUNDARY_WARNINGS and self.error_count % 50 == 0:
                print(f"Y adjustment: ({x}, {y}), limits: ({sprite_width}, {sprite_height})")
            self.error_count += 1

        try:
            return self.sprite_selected.subsurface(x, y, pixel_line, pixel_column)
        except ValueError as e:

            if self.error_count % 50 == 0:
                print(f"Error selecting sprite: {e}. Reverting to normal Goku.")
            self.error_count += 1
            self.sprite_type = 0
            self.goku_transformed_offset_x = 0
            x = pixel_line * line
            y = pixel_column * column

            x = min(x, sprite_width - pixel_line)
            y = min(y, sprite_height - pixel_column)

            return self.sprite_selected.subsurface(x, y, pixel_line, pixel_column)

    def animate_sprite(self, move, old_pos_sprite):
        """ Character walking animation """

        new_img_sprite = self.select_sprite(self.direction[old_pos_sprite][2][0], self.direction[old_pos_sprite][2][1])

        if move is not None:
            for i in {'Down', 'Up', 'Left', 'Right'}:
                if move == i:
                    if self.current_position == 1:
                        new_img_sprite = self.select_sprite(self.direction[i][0][0], self.direction[i][0][1])
                        self.current_position = 2
                    elif self.current_position == 2:
                        self.current_position = 1
                        new_img_sprite = self.select_sprite(self.direction[i][1][0], self.direction[i][1][1])

        return new_img_sprite
