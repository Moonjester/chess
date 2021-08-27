import pygame
from board import Board
from pieces2 import *
from constants import *


pygame.init()


def main():
    game_run = True
    clock = pygame.time.Clock()
    board = Board()
    board.draw_squares(SCREEN)

# ---------------------------------- Main Function ------------------------------- #

    pieces_on_board = pygame.sprite.Group()

    w_pieces_coord = {
        'pawn_1' : 0, 'pawn_2' : 1, 'pawn_3' : 2, 'pawn_4' : 3, 'pawn_5' : 4,
        'pawn_6' : 5, 'pawn_7' : 6, 'pawn_8' : 7, 'castle_l' : 0,
        'castle_r' : 7, 'knight_r' : 6, 'knight_l' : 1, 'bishop_r' : 2,
        'bishop_l' : 5, 'queen' : 3, 'king' : 4
        }

    b_pieces_coord = {
        'pawn_1' : 0, 'pawn_2' : 1, 'pawn_3' : 2, 'pawn_4' : 3, 'pawn_5' : 4,
        'pawn_6' : 5, 'pawn_7' : 6, 'pawn_8' : 7, 'castle_l' : 0,
        'castle_r' : 7, 'knight_r' : 6, 'knight_l' : 1, 'bishop_r' : 2,
        'bishop_l' : 5, 'queen' : 3, 'king' : 4
        }

    for pieces, coords in b_pieces_coord.items():

        scaled_xy = coords * S_SIZE

        if 'pawn' in pieces:
            b_pieces_coord[pieces] = Pawn(scaled_xy, S_SIZE, 'black')
            w_pieces_coord[pieces] = Pawn(scaled_xy, S_SIZE * 6, 'white')

        if 'castle' in pieces:
            b_pieces_coord[pieces] = Castle(scaled_xy, 0, 'black')
            w_pieces_coord[pieces] = Castle(scaled_xy, S_SIZE * 7, 'white')

        if 'knight' in pieces:
            b_pieces_coord[pieces] = Knight(scaled_xy, 0, 'black')
            w_pieces_coord[pieces] = Knight(scaled_xy, S_SIZE * 7, 'white')

        if 'bishop' in pieces:
            b_pieces_coord[pieces] = Bishop(scaled_xy, 0, 'black')
            w_pieces_coord[pieces] = Bishop(scaled_xy, S_SIZE * 7, 'white')

        if 'queen' in pieces:
            b_pieces_coord[pieces] = Queen(scaled_xy, 0, 'black')
            w_pieces_coord[pieces] = Queen(scaled_xy, S_SIZE * 7, 'white')

        if 'king' in pieces:
            b_pieces_coord[pieces] = King(scaled_xy, 0, 'black')
            w_pieces_coord[pieces] = King(scaled_xy, S_SIZE * 7, 'white')

        pieces_on_board.add(w_pieces_coord[pieces])
        pieces_on_board.add(b_pieces_coord[pieces])

    num = 0
    selected_coords = []
    selected = False
    double_clicked = len(selected_coords) == 2
    selected_piece = pygame.sprite.GroupSingle()

#-------------------------------- While Loop -----------------------------------#

    while game_run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_loc = pygame.mouse.get_pos()
                currx, curry = mouse_loc
                originx, originy = mouse_loc
                originx = round(floor(originx - 50), -2)
                originy = round(floor(originy - 50), -2)

                for pieces in pieces_on_board:
                    collide = pieces.piece_rect.collidepoint(currx, curry)

                    # checks if you selected a square with a piece on

                    if collide and not selected:
                        selected = True
                        selected_piece.add(pieces)
                        num += 1
                        selected_coords.append((originx, originy))
                        pieces.show_valid(selected_coords[0])

                        print(pieces)
                        print('collided', num, selected_coords[0])

                # checks that you have not selected the same square
                # and counts it as a move

                new_coords = (originx, originy) not in selected_coords

                if selected and new_coords:
                    print('uncollided', originx, originy)

                    for pieces in selected_piece:
                        pieces.isvalid((originx, originy), selected_coords[0])

                    selected_piece.empty()
                    selected = False
                    selected_coords.clear()

            if event.type == pygame.QUIT:
                game_run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_run = False

# -------------------------------- Update ---------------------------------- #

        pygame.display.update()

main()
