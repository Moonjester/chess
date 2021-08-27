import pygame
from math import floor
from board import Board
import pieces as chespie
import constants as con


pygame.init()


def main():
    game_run = True
    clock = pygame.time.Clock()
    board = Board()
    board.draw_squares(con.SCREEN)

# ----------------------------- Main Function --------------------------- #

    pieces_on_board = pygame.sprite.Group()

    w_pieces_coord = {
        'pawn_1': 0, 'pawn_2': 1, 'pawn_3': 2, 'pawn_4': 3, 'pawn_5': 4,
        'pawn_6': 5, 'pawn_7': 6, 'pawn_8': 7, 'castle_l': 0,
        'castle_r': 7, 'knight_r': 6, 'knight_l': 1, 'bishop_r': 2,
        'bishop_l': 5, 'queen': 3, 'king': 4
        }
    b_pieces_coord = {
        'pawn_1': 0, 'pawn_2': 1, 'pawn_3': 2, 'pawn_4': 3, 'pawn_5': 4,
        'pawn_6': 5, 'pawn_7': 6, 'pawn_8': 7, 'castle_l': 0,
        'castle_r': 7, 'knight_r': 6, 'knight_l': 1, 'bishop_r': 2,
        'bishop_l': 5, 'queen': 3, 'king': 4
        }

    for pieces, xycoords in con.PIECE_POS.items():

        square = xycoords * con.S_SIZE
        w_row = con.S_SIZE * 7
        w_pawns = con.S_SIZE * 6
        b_row = 0
        b_pawns = con.S_SIZE

        if 'pawn' in pieces:
            b_pieces_coord[pieces] = chespie.Pawn(square, b_pawns, 'black')
            w_pieces_coord[pieces] = chespie.Pawn(square, w_pawns, 'white')

        if 'castle' in pieces:
            b_pieces_coord[pieces] = chespie.Castle(square, b_row, 'black')
            w_pieces_coord[pieces] = chespie.Castle(square, w_row, 'white')

        if 'knight' in pieces:
            b_pieces_coord[pieces] = chespie.Knight(square, b_row, 'black')
            w_pieces_coord[pieces] = chespie.Knight(square, w_row, 'white')

        if 'bishop' in pieces:
            b_pieces_coord[pieces] = chespie.Bishop(square, b_row, 'black')
            w_pieces_coord[pieces] = chespie.Bishop(square, w_row, 'white')

        if 'queen' in pieces:
            b_pieces_coord[pieces] = chespie.Queen(square, b_row, 'black')
            w_pieces_coord[pieces] = chespie.Queen(square, w_row, 'white')

        if 'king' in pieces:
            b_pieces_coord[pieces] = chespie.King(square, b_row, 'black')
            w_pieces_coord[pieces] = chespie.King(square, w_row, 'white')

        pieces_on_board.add(w_pieces_coord[pieces])
        pieces_on_board.add(b_pieces_coord[pieces])

    num = 0
    selected_coords = []
    # toplay = 'white'
    selected = False
    selected_piece = pygame.sprite.GroupSingle()

    while game_run:
        clock.tick(con.FPS)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_loc = pygame.mouse.get_pos()
                currx, curry = mouse_loc
                originx, originy = mouse_loc
                originx = round(floor(originx - 50), -2)
                originy = round(floor(originy - 50), -2)
                originxy = originx, originy

                for pieces in pieces_on_board:
                    collide = pieces.piece_rect.collidepoint(currx, curry)

                    rules = [collide,
                             not selected]

                    # checks if you selected a square with a piece on
                    if all(rules):
                        selected = True
                        selected_piece.add(pieces)
                        selected_coords.append(originxy)
                        pieces.obstructed(pieces_on_board)
                        pieces.calc_valid(selected_coords[0])

                        print('collided', num)

                new_coords = (originxy) not in selected_coords

                if selected and new_coords:
                    print('uncollided', originxy)

                    for select in selected_piece:
                        select.isvalid(originxy, selected_coords[0])

                    select.take_piece(selected_piece, pieces_on_board)

                    selected = False
                    selected_coords.clear()

            if event.type == pygame.QUIT:
                game_run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_run = False

        pygame.display.update()


main()
