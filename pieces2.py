import pygame
import os, sys
from constants import *
from math import floor

#-------------------------------- Main Parent Class -------------------------------#

class Piece(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc, colour, piece_type):
        pygame.sprite.Sprite.__init__(self)
        self.pieces = []
        self.piece_type = piece_type
        self.xloc = xloc
        self.yloc = yloc
        self.xyloc = (self.xloc, self.yloc)
        self.colour = colour
        self.img = None
        self.select_piece = None
        self.rect = None
        self.valid_moves = []

        for items in IMAGE_COL:
            self.pieces.append(f'images2/{items}')

#----------------------------------- Image Display --------------------------------#

        for piece in self.pieces:

            piece_match = self.piece_type in piece
            piece_colour = self.colour in piece

            if piece_match and piece_colour:
                self.img = pygame.image.load(piece)
                self.img = pygame.transform.scale(self.img, (S_SIZE, S_SIZE))
                self.piece_rect = pygame.rect.Rect(self.xyloc, (S_SIZE, S_SIZE))

        SCREEN.blit(self.img, self.xyloc)

#----------------------------------- Update Function ------------------------------#

    def update(self, newxy, init_posxy):
        self.xloc, self.yloc = newxy
        self.init_posx, self.init_posy = init_posxy

        self.piece_rect = pygame.rect.Rect((self.xloc, self.yloc),
         (S_SIZE, S_SIZE))

        self.clear_square((self.xloc, self.yloc), 'cover')
        self.clear_square((self.init_posx, self.init_posy), 'cover')

        SCREEN.blit(self.img, (self.xloc, self.yloc))

#----------------------------------- Clear Square ---------------------------------#

    def clear_square(self, posxy, square_type):
        x, y = posxy
        self.x_new_coords = self.xloc // S_SIZE
        self.y_new_coords = self.yloc // S_SIZE
        self.drawxy = (self.x_new_coords, self.y_new_coords)

        if square_type is 'highlight':
            if self.drawxy in LIGHT_SQUARES:
                pygame.draw.rect(SCREEN, L_GREEN, [x, y, S_SIZE, S_SIZE], 1)
            else:
                pygame.draw.rect(SCREEN, D_GREEN, [x, y, S_SIZE, S_SIZE], 1)

        if square_type is 'cover':
            if self.drawxy in LIGHT_SQUARES:
                pygame.draw.rect(SCREEN, L_GREEN, (x, y, S_SIZE, S_SIZE))
            else:
                pygame.draw.rect(SCREEN, D_GREEN, (x, y, S_SIZE, S_SIZE))

# -------------------------------- Validator Function ----------------------------- #

    def isvalid(self, newxy, init_posxy):
        self.init_posx, self.init_posy = init_posxy
        self.newxy = newxy

        for squares in self.valid_moves:
            self.clear_square(squares, 'highlight')

        if self.newxy in self.valid_moves:
            self.update(newxy, init_posxy)
        else:
            print('invalid move')

# --------------------------------- Child Classes -------------------------------- #

class Pawn(Piece):
    def __init__(self, x, y, incolour):
        super(Pawn, self).__init__(x, y, incolour, piece_type = 'pawn')

    def show_valid(self, init_posxy):
        self.init_posx, self.init_posy = init_posxy


class Bishop(Piece):
    def __init__(self, x, y, incolour):
        super(Bishop, self).__init__(x, y, incolour, piece_type = 'bishop')

    def show_valid(self, init_posxy):
        self.init_posx, self.init_posy = init_posxy

        for coords in SQUARE_COORD:
            x, y = coords
            diff_x = abs(x - self.init_posx)
            diff_y = abs(y - self.init_posy)

            valid_move_rules = [
                x != self.init_posx,
                y != self.init_posy,
                diff_x == diff_y
                ]

            if all(valid_move_rules):
                pygame.draw.rect(SCREEN, RED, (x, y, S_SIZE, S_SIZE), 1)
                self.valid_moves.append((x, y))


class Castle(Piece):
    def __init__(self, x, y, incolour):
        super(Castle, self).__init__(x, y, incolour, piece_type = 'castle')


class Queen(Piece):
    def __init__(self, x, y, incolour):
        super(Queen, self).__init__(x, y, incolour, piece_type = 'queen')


class Knight(Piece):
    def __init__(self, x, y, incolour):
        super(Knight, self).__init__(x, y, incolour, piece_type = 'knight')


class King(Piece):
    def __init__(self, x, y, incolour):
        super(King, self).__init__(x, y, incolour, piece_type = 'king')
