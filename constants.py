import pygame
import os

L_GREEN = (247, 255, 231)
D_GREEN = (130, 165, 103)
RED = (255, 0, 0)
ROW = COLUMN = 8
S_SIZE = 100
WIDTH = HEIGHT = 800
FPS = 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
IMAGE_COL = os.listdir('images2/')
SQUARE_COORD = []
LIGHT_SQUARES = []
PIECE_POS = {
        'pawn_1': 0, 'pawn_2': 1, 'pawn_3': 2, 'pawn_4': 3, 'pawn_5': 4,
        'pawn_6': 5, 'pawn_7': 6, 'pawn_8': 7, 'castle_l': 0,
        'castle_r': 7, 'knight_r': 6, 'knight_l': 1, 'bishop_r': 2,
        'bishop_l': 5, 'queen': 3, 'king': 4
        }
