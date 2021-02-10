#-*- coding: utf-8 -*-
import pygame
import random

class Piece:
    'The model of a piece'
    def __init__(self, matrix, display, square_side):
        self.matrix = matrix
        self.display = display
        self.square_side = square_side
        self.x = 0
        self.y = 0
        self.compute_size()

    def compute_size(self):
        'Computes the dimensions of the piece, in rows and columns'
        self.rows = len(self.matrix)
        self.columns = len(self.matrix[0])

    def rotate90(self):
        'Turns a piece 90 degrees, clockwise'
        self.matrix = list(zip(*self.matrix[::-1]))
        self.compute_size()

    def rotateM90(self):
        'Turns a piece 90 degrees, counterclockwise'
        self.matrix = list(zip(*self.matrix))[::-1]
        self.compute_size()

    def __draw_square(self, x, y, color):
        'Draws a square in the given (row, columns -- not pixels) coordinates'
        square = (x*self.square_side,
                    y*self.square_side,
                    self.square_side,
                    self.square_side)
        inner_square = (x*self.square_side+8,
                            y*self.square_side+8,
                            self.square_side-16,
                            self.square_side-16)
        pygame.draw.rect(self.display,
                         (int(color[0]/2),
                          int(color[1]/2),
                          int(color[2]/2)),
                         square,
                         0)
        pygame.draw.rect(self.display, color, inner_square, 0)

    def __delete_rectangle(self, rectangle):
        'deletes the specified area'
        pygame.draw.rect(self.display, Cuatris.colors[0], rectangle, 0)

    def draw(self, x_ini, y_ini):
        'draws the specified piece from the coordinates (rows, columns --not pixels) x_ini, y_ini'
        # actualizamos la posición de la pieza
        self.x = x_ini
        self.y = y_ini
        for i in range(0,len(self.matrix)):
            for j in range(0,len(self.matrix[i])):
                if self.matrix[i][j] != 0:
                    self.__draw_square(x_ini+j, y_ini+i, Cuatris.colors[self.matrix[i][j]])

    def delete(self, x_ini, y_ini):
        'deletes the specified piece from the coordinates (rows, columns --not pixels) x_ini, y_ini'
        for i in range(0,len(self.matrix)):
            for j in range(0,len(self.matrix[i])):
                if self.matrix[i][j] != 0:
                    self.__draw_square(x_ini+j, y_ini+i, Cuatris.colors[0])

    # Piece movement
    def move(self, delta_x, delta_y):
        'moves the piece the given delta, expressed in rows and columns --not pixels'
        self.x = self.x + delta_x
        self.y = self.y + delta_y

    # Piece status
    def self_draw(self):
        'draws the piece in its coordinates'
        self.draw(self.x, self.y)

    def self_delete(self):
        'deletes the piece from its coordinates'
        self.delete(self.x, self.y)

    def is_colliding_with(self, other):
        for i in range(0,len(self.matrix)):
            for j in range(0,len(self.matrix[i])):
                if self.matrix[i][j] != 0:
                    if other.matrix[self.y + i][self.x + j] != 0:
                        return True
        return False

class Container(Piece):
    'Container where the game takes place'
    def __remove_row(self, row):
        'removes the given row, adding a new one on the top of the Container'
        for row in range(row, 0, -1):
            self.matrix[row] = self.matrix[row - 1]
        self.matrix[0] = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

    def count_lines(self, other_piece):
        'checks how many lines are completed with a new piece'
        lines = 0
        for row in range(other_piece.y, other_piece.y + other_piece.rows):
            product = 1;
            for value in self.matrix[row]:
                product = product * value
                if product == 0:
                    break
            if product > 0:
                lines = lines +1
                self.__remove_row(row)
        return lines

    def incorporate(self, other_piece):
        'incorporates the other piece\'s matrix to the Container, returning the number of completed rows --this is to be used when a piece collides with the bottom of the container'
        for i in range(0,len(other_piece.matrix)):
            for j in range(0,len(other_piece.matrix[i])):
                if other_piece.matrix[i][j] != 0:
                    self.matrix[other_piece.y+i][other_piece.x+j] = other_piece.matrix[i][j]
        return self.count_lines(other_piece)

class Cuatris:
    'Cuatris Object: implements game logic'

    # Color definitions
    WHITE = (255,255,255)
    GRAY = (127,127,127)
    BLACK = (0, 0, 0)
    PURPLE = (200,0,200)
    GREEN = (0, 200, 0)
    RED = (200, 0, 0)
    BLUE = (0, 0, 200)
    YELLOW = (200, 200, 0)
    CYAN = (0, 200, 200)
    ORANGE = (255, 102, 16)
    colors = [BLACK, GRAY, CYAN, BLUE, ORANGE, GREEN, RED, PURPLE, YELLOW]



    matrix_L = [(7, 0),
               (7, 0),
                (7, 7)]

    matrix_J = [(0, 8),
                (0, 8),
                (8, 8)]

    matrix_I = [(6, 0),
                (6, 0),
                (6, 0),
                (6, 0)]

    matrix_S = [(0, 2, 2),
                (2, 2, 0)]

    matrix_Z = [(4, 4, 0),
                (0, 4, 4)]

    matrix_T = [(5, 5, 5),
                (0, 5, 0)]

    matrix_O = [(3, 3),
                (3, 3)]

    matrices = [0, 0, matrix_L, matrix_J, matrix_I, matrix_S, matrix_Z, matrix_T, matrix_O]

    next_matrix = [[1, 1, 1, 1, 1, 1],
                        [1, 0, 0, 0, 0, 1],
                        [1, 0, 0, 0, 0, 1],
                        [1, 0, 0, 0, 0, 1],
                        [1, 0, 0, 0, 0, 1],
                        [1, 1, 1, 1, 1, 1]]



    # Nº de cuadros por segundo
    FPS = 60

    # Lado del cuadrado por defecto
    SLOT = 40

    # Evento de Gravedad
    GRAVITY = pygame.USEREVENT + 1

    # Coordenadas iniciales de las piezas
    x_ini = 4
    y_ini = 0

    def __init__(self, square_side):
        try:
            self.slot = int(square_side)
        except ValueError:
            # Default value
            self.slot = SLOT
        self.lines = 0
        self.lines_for_next_level = 20
        self.level = 0
        self.width = 21*self.slot
        self.height = 22*self.slot
        
        pygame.init()

        # display definition
        self.display = pygame.display.set_mode((self.width, self.height))
        self.display.fill(Cuatris.BLACK)
        matrix_Container = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        self.next = Container (Cuatris.next_matrix, self.display, self.slot)
        self.next.draw(13, 0)

        self.container = Container (matrix_Container, self.display, self.slot)
        self.container.draw(0, 0)

        self.piece = self.get_next_piece()
        self.piece.draw(4,0)
        self.next_piece = self.get_next_piece()
        self.next_piece.draw(15,1)

        pygame.display.update()

        # Game clock
        self.clock = pygame.time.Clock()

        # Gravity Event

        self.t_FALL = 70
        self.t_GRAVITY = 2000 #milisegundos
        pygame.time.set_timer(Cuatris.GRAVITY, self.t_GRAVITY)


    def get_next_piece(self):
        n_piece = random.randint(2, 8)
        piece = Piece (self.matrices[n_piece], self.display, self.slot)
        return piece

    def _print(self, font, string, left, top, color, background):
        text = font.render(string, True, color, background)
        textrect = text.get_rect()
        textrect.left= left
        textrect.top= top
        self.display.blit(text, textrect)

    def score(self):
        basicfont = pygame.font.SysFont(None, self.slot)
        self._print(basicfont,'Lines: '+str(self.lines), 13*self.slot, 8*self.slot, Cuatris.WHITE, Cuatris.BLACK)
        self._print(basicfont,'Level: '+str(self.level), 13*self.slot, 9*self.slot, Cuatris.GRAY, Cuatris.BLACK)
        self._print(basicfont,'Next: ' + str(self.lines_for_next_level), 13*self.slot, 10*self.slot, Cuatris.GRAY, Cuatris.BLACK)


    def game_over(self):
        basicfont = pygame.font.SysFont(None, self.slot) # to refactor
        left = self.display.get_rect().centerx - len('GAME O')*self.slot
        top = self.display.get_rect().centery
        self._print(basicfont,'GAME OVER', left, top, Cuatris.RED, Cuatris.GRAY)
        self._print(basicfont,'RETURN TO START OVER', left, top+self.slot, Cuatris.RED, Cuatris.GRAY)

    def turn(self, counterclockwise, piece, container):
        piece.self_delete()
        if counterclockwise:
            piece.rotateM90()
        else:
            piece.rotate90()
        while piece.is_colliding_with(container):
            piece.move(-1,0)
        piece.self_draw()

    def move_right(self, units, piece, container):
        piece.self_delete()
        piece.move(units,0)
        if piece.is_colliding_with(container):
            piece.move(-units, 0)
        piece.self_draw()

    def run_game(self):

        is_continue = True

        self.score()

        while is_continue:
            # Pause until next tick
            self.clock.tick(Cuatris.FPS)

            # QUIT (x)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    is_continue = False
                else:
                    # Process gravity
                    if event.type == Cuatris.GRAVITY:
                        self.piece.self_delete()
                        self.piece.move(0, 1)
                        if self.piece.is_colliding_with(self.container):
                            pygame.time.set_timer(Cuatris.GRAVITY, self.t_GRAVITY)
                            self.piece.move(0,-1)
                            self.container.self_delete()
                            self.lines = self.lines + self.container.incorporate(self.piece)
                            # levels
                            if self.lines >= self.lines_for_next_level:
                                self.level = self.level +1
                                self.lines_for_next_level = self.lines_for_next_level + 20
                                if self.t_GRAVITY > 100:
                                    self.t_GRAVITY = self.t_GRAVITY - 1000
                            self.score()
                            self.container.self_draw()
                            self.next_piece.self_delete()
                            self.piece = self.next_piece
                            self.piece.draw(4,0)
                            self.next_piece = self.get_next_piece()
                            self.next_piece.draw(15,1)
                            if self.piece.is_colliding_with(self.container):
                                is_continue = False
                                self.game_over()
                        else:
                            self.piece.self_draw()

                    if event.type == pygame.KEYDOWN:

                        # Piece turning can cause collisions to the right
                        if event.key == pygame.K_z:
                            self.turn(True, self.piece, self.container)

                        if event.key == pygame.K_x:
                            self.turn(False, self.piece, self.container)

                        if event.key == pygame.K_LEFT:
                            self.move_right(-1,self.piece, self.container)

                        if event.key == pygame.K_RIGHT:
                            self.move_right(1,self.piece, self.container)

                        # accelerate gravity
                        if event.key == pygame.K_DOWN:
                            pygame.time.set_timer(Cuatris.GRAVITY, self.t_FALL)
                        else:
                            pygame.time.set_timer(Cuatris.GRAVITY, self.t_GRAVITY)

                    pygame.display.update()
        while True:
            # Pause until next tick
            self.clock.tick(Cuatris.FPS)
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return True
                else:
                    return False

play = True
while play == True:
    game = Cuatris(30)
    play= game.run_game()

print ("Game Over")
pygame.quit()
