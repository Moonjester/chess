import pygame
import constants as con


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
        self.valid_moves = []
        self.temp_val = []
        self.sqr_size = (con.S_SIZE, con.S_SIZE)
        self.obstructed_squares = []
        self.b_obstructed_squares = []
        self.w_obstructed_squares = []

        for items in con.IMAGE_COL:
            self.pieces.append(f'images2/{items}')

        for piece in self.pieces:
            piece_match = self.piece_type in piece
            piece_colour = self.colour in piece

            if piece_match and piece_colour:
                self.img = pygame.image.load(piece)
                self.img = pygame.transform.scale(self.img, self.sqr_size)
                self.piece_rect = pygame.rect.Rect(self.xyloc, self.sqr_size)

        con.SCREEN.blit(self.img, self.xyloc)

    def update(self, newxy, init_posxy):
        self.newxy = newxy
        self.init_posxy = init_posxy
        self.piece_rect = pygame.rect.Rect(self.newxy, self.sqr_size)

        self.clear_square(self.newxy, 'cover')
        self.clear_square(self.init_posxy, 'cover')

        con.SCREEN.blit(self.img, self.newxy)

    def clear_square(self, posxy, square_type):
        x, y = posxy
        self.x_new_coords = x // con.S_SIZE
        self.y_new_coords = y // con.S_SIZE
        self.drawxy = (self.x_new_coords, self.y_new_coords)
        self.square_dim = (x, y, con.S_SIZE, con.S_SIZE)

        if square_type == 'highlight':
            if self.drawxy in con.LIGHT_SQUARES:
                pygame.draw.rect(con.SCREEN, con.L_GREEN, self.square_dim, 1)
            else:
                pygame.draw.rect(con.SCREEN, con.D_GREEN, self.square_dim, 1)

        if square_type == 'cover':
            if self.drawxy in con.LIGHT_SQUARES:
                pygame.draw.rect(con.SCREEN, con.L_GREEN, self.square_dim)
            else:
                pygame.draw.rect(con.SCREEN, con.D_GREEN, self.square_dim)

    def isvalid(self, newxy, init_posxy):
        self.init_posxy = init_posxy
        self.newxy = newxy

        for squares in self.valid_moves:
            self.clear_square(squares, 'highlight')

        if self.newxy in self.valid_moves:
            self.update(self.newxy, self.init_posxy)

        else:
            print('invalid move')

        self.temp_val.clear()
        self.valid_moves.clear()

    def take_piece(self, selected_piece, pieces_on_board):
        self.selected_piece = selected_piece
        self.pieces_on_board = pieces_on_board

        for pieces in self.pieces_on_board:

            take_rules = [self.piece_rect.colliderect(pieces.piece_rect),
                          pieces not in selected_piece]

            if all(take_rules):
                pieces.kill()

        self.obstructed_squares.clear()
        self.w_obstructed_squares.clear()
        self.b_obstructed_squares.clear()

    def obstructed(self, pieces_on_board):
        for pieces in pieces_on_board:
            self.obstructed_squares.append(pieces.piece_rect.topleft)

            if pieces.colour == 'black':
                self.b_obstructed_squares.append(pieces.piece_rect.topleft)
            if pieces.colour == 'white':
                self.w_obstructed_squares.append(pieces.piece_rect.topleft)

    def highlight_square(self, moves):
        for xycoords in self.w_obstructed_squares:
            if self.colour == 'white' and xycoords in moves:
                moves = [(x, y) for (x, y) in moves if (x, y) != xycoords]

        for xycoords in self.b_obstructed_squares:
            if self.colour == 'black' and xycoords in moves:
                moves = [(x, y) for (x, y) in moves if (x, y) != xycoords]

        for move in moves:
            self.x, self.y = move
            self.square_dim = (self.x, self.y, con.S_SIZE, con.S_SIZE)

            pygame.draw.rect(con.SCREEN, con.RED, self.square_dim, 1)
            self.valid_moves.append(move)

    def filterval_diag(self, moves, initpos_xy):
        self.x, self.y = initpos_xy
        self.init_posxy = initpos_xy

        norwes = [(x, y) for (x, y) in moves if self.x >= x and self.y >= y]
        noreas = [(x, y) for (x, y) in moves if self.x <= x and self.y >= y]
        soueas = [(x, y) for (x, y) in moves if self.x <= x and self.y <= y]
        souwes = [(x, y) for (x, y) in moves if self.x >= x and self.y <= y]

        for xycoords in self.obstructed_squares:
            xcoord, ycoord = xycoords
            diffx = self.init_posx - xcoord
            diffy = self.init_posy - ycoord

            if xycoords in moves:
                in_norwes = diffx > 0 and diffy > 0
                in_souwes = diffx < 0 and diffy < 0
                in_noreas = diffx < 0 and diffy > 0
                in_soueas = diffx > 0 and diffy < 0

                if in_norwes:
                    norwes = [(x, y) for (x, y) in norwes
                              if x >= xcoord and y >= ycoord]
                if in_soueas:
                    soueas = [(x, y) for (x, y) in soueas
                              if x <= xcoord and y <= ycoord]
                if in_noreas:
                    noreas = [(x, y) for (x, y) in noreas
                              if x <= xcoord and y >= ycoord]
                if in_souwes:
                    souwes = [(x, y) for (x, y) in souwes
                              if x >= xcoord and y <= ycoord]

        moves = noreas + souwes + soueas + norwes

        self.highlight_square(moves)

    def filterval_cross(self, moves, initpos_xy):
        self.x, self.y = initpos_xy
        self.init_posxy = initpos_xy

        for xycoords in self.obstructed_squares:
            xcoord, ycoord = xycoords
            diffx = self.init_posx - xcoord
            diffy = self.init_posy - ycoord

            if xycoords in moves:
                in_north = diffx == 0 and diffy < 0
                in_south = diffx == 0 and diffy > 0
                in_east = diffy == 0 and diffx < 0
                in_west = diffy == 0 and diffx > 0

                if in_south:
                    moves = [(x, y) for (x, y) in moves if y >= ycoord]
                if in_north:
                    moves = [(x, y) for (x, y) in moves if y <= ycoord]
                if in_east:
                    moves = [(x, y) for (x, y) in moves if x <= xcoord]
                if in_west:
                    moves = [(x, y) for (x, y) in moves if x >= xcoord]

        self.highlight_square(moves)


class Pawn(Piece):
    def __init__(self, x, y, incolour):
        super(Pawn, self).__init__(x, y, incolour, piece_type='pawn')

    def calc_valid(self, init_posxy):
        self.init_posx, self.init_posy = init_posxy
        self.init_posxy = init_posxy

        for coords in con.SQUARE_COORD:
            self.x, self.y = coords
            diff_y = self.init_posy - self.y
            diff_x = self.init_posx - self.x

            move_rules = [abs(diff_x) <= 100,
                          self.colourmove(diff_y),
                          self.startmove(diff_x, diff_y)]

            if all(move_rules):
                self.temp_val.append(coords)

        self.filterpawn(self.temp_val, init_posxy)

    def colourmove(self, diff_y):
        if self.colour == 'black':
            new_rule = diff_y < 0
        if self.colour == 'white':
            new_rule = diff_y > 0

        return new_rule

    def startmove(self, diff_x, diff_y):
        diff_x = abs(diff_x)
        diff_y = abs(diff_y)

        if self.colour == 'black' and self.init_posy == 100:
            new_rule = diff_y < 200 or (diff_y == 200 and diff_x == 0)
        elif self.colour == 'white' and self.init_posy == 600:
            new_rule = diff_y < 200 or (diff_y == 200 and diff_x == 0)
        else:
            new_rule = diff_y == 100

        return new_rule

    def filterpawn(self, moves, init_posxy):
        self.x, self.y = init_posxy
        self.init_posxy = init_posxy
        obs_sqrs = self.obstructed_squares

        norwes, souwes, soueas, noreas, middle = ([] for i in range(5))

        for (x, y) in moves:
            in_norwes = self.x > x and self.y >= y and (x, y) in obs_sqrs
            in_noreas = self.x < x and self.y >= y and (x, y) in obs_sqrs
            in_soueas = self.x < x and self.y <= y and (x, y) in obs_sqrs
            in_souwes = self.x > x and self.y <= y and (x, y) in obs_sqrs
            in_middle = self.x - x == 0 and (x, y) not in obs_sqrs

            if in_norwes:
                norwes.append((x, y))
            if in_soueas:
                soueas.append((x, y))
            if in_noreas:
                noreas.append((x, y))
            if in_souwes:
                souwes.append((x, y))
            if in_middle:
                middle.append((x, y))

        moves = soueas + souwes + norwes + noreas + middle

        self.highlight_square(moves)

    def pawnpromote(self):
        if self.colour == 'black' and self.init_posy == 800:
            pass
        if self.colour == 'white' and self.init_posy == 0:
            pass


class Bishop(Piece):
    def __init__(self, x, y, incolour):
        super(Bishop, self).__init__(x, y, incolour, piece_type='bishop')

    def calc_valid(self, init_posxy):
        self.init_posx, self.init_posy = init_posxy
        self.init_posxy = init_posxy
        self.obstructed_squares.remove(self.init_posxy)

        for coords in con.SQUARE_COORD:
            self.x, self.y = coords
            true_diff_x = self.init_posx - self.x
            true_diff_y = self.init_posy - self.y
            diff_x = abs(true_diff_x)
            diff_y = abs(true_diff_y)

            move_rules = [diff_x == diff_y]

            if all(move_rules):
                self.temp_val.append(coords)

        self.filterval_diag(self.temp_val, self.init_posxy)


class Castle(Piece):
    def __init__(self, x, y, incolour):
        super(Castle, self).__init__(x, y, incolour, piece_type='castle')

    def calc_valid(self, init_posxy):
        self.init_posx, self.init_posy = init_posxy
        self.init_posxy = init_posxy

        for coords in con.SQUARE_COORD:
            self.x, self.y = coords
            true_diff_x = self.init_posx - self.x
            true_diff_y = self.init_posy - self.y
            diff_x = abs(true_diff_x)
            diff_y = abs(true_diff_y)

            move_rules = [diff_x == 0,
                          diff_y == 0]

            if any(move_rules):
                self.temp_val.append(coords)

        self.filterval_cross(self.temp_val, self.init_posxy)


class Queen(Piece):
    def __init__(self, x, y, incolour):
        super(Queen, self).__init__(x, y, incolour, piece_type='queen')

    def calc_valid(self, init_posxy):
        self.init_posx, self.init_posy = init_posxy
        self.init_posxy = init_posxy
        self.obstructed_squares.remove(self.init_posxy)
        self.temp_cross = []
        self.temp_diag = []

        for coords in con.SQUARE_COORD:
            x, y = coords
            diff_x = abs(x - self.init_posx)
            diff_y = abs(y - self.init_posy)

            move_rules1 = [diff_x == 0,
                           diff_y == 0]

            move_rules2 = [diff_x == diff_y]

            if any(move_rules1):
                self.temp_cross.append(coords)

            if all(move_rules2):
                self.temp_diag.append(coords)

        self.filterval_diag(self.temp_diag, init_posxy)
        self.filterval_cross(self.temp_cross, init_posxy)


class Knight(Piece):
    def __init__(self, x, y, incolour):
        super(Knight, self).__init__(x, y, incolour, piece_type='knight')

    def calc_valid(self, init_posxy):
        self.init_posx, self.init_posy = init_posxy
        self.init_posxy = init_posxy
        self.obstructed_squares.remove(self.init_posxy)

        for coords in con.SQUARE_COORD:
            self.x, self.y = coords
            diff_x = abs(self.x - self.init_posx)
            diff_y = abs(self.y - self.init_posy)

            valid_move_rules = [(diff_x + diff_y) == 300,
                                diff_x != 0,
                                diff_y != 0]

            if all(valid_move_rules):
                self.temp_val.append((self.x, self.y))

        self.highlight_square(self.temp_val)


class King(Piece):
    def __init__(self, x, y, incolour):
        super(King, self).__init__(x, y, incolour, piece_type='king')

    def calc_valid(self, init_posxy):
        self.init_posx, self.init_posy = init_posxy
        self.init_posxy = init_posxy
        self.obstructed_squares.remove(self.init_posxy)

        for coords in con.SQUARE_COORD:
            self.x, self.y = coords
            diff_x = self.x - self.init_posx
            diff_y = self.y - self.init_posy

            valid_move_rules = [abs(diff_x) <= 100,
                                abs(diff_y) <= 100]

            if all(valid_move_rules):
                self.temp_val.append((self.x, self.y))

        self.highlight_square(self.temp_val)
