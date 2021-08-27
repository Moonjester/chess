import pygame
import constants as con


class Board:
    def draw_squares(self, screen):
        l_green = con.L_GREEN
        d_green = con.D_GREEN
        size = con.S_SIZE

        screen.fill(d_green)

        for row in range(con.ROW):
            for col in range(row % 2, con.ROW, 2):
                square_surface = (row * size, col * size, size, size)

                pygame.draw.rect(screen, l_green, square_surface)
                con.LIGHT_SQUARES.append((row, col))

            for col in range(con.COLUMN):
                con.SQUARE_COORD.append((row * size, col * size))
