# -*- coding: utf-8 -*-
import pygame
import random


class Piece:
    """The model of a piece"""

    def __init__(self, matrix, display, square_side):
        self.matrix = matrix
        self.rows = 0
        self.columns = 0
        self.display = display
        self.square_side = square_side
        self.x = 0
        self.y = 0
        self.compute_size()

    def compute_size(self):
        """Computes the dimensions of the piece, in rows and columns"""
        self.rows = len(self.matrix)
        self.columns = len(self.matrix[0])

    def rotate90(self):
        """Turns a piece 90 degrees, clockwise"""
        self.matrix = list(zip(*self.matrix[::-1]))
        self.compute_size()

    def rotate_minus_90(self):
        """Turns a piece 90 degrees, counterclockwise"""
        self.matrix = list(zip(*self.matrix))[::-1]
        self.compute_size()

    def _draw_square(self, x, y, color):
        """Draws a square in the given (row, columns -- not pixels)
        coordinates"""
        square = (
            x * self.square_side,
            y * self.square_side,
            self.square_side,
            self.square_side,
        )
        inner_square = (
            x * self.square_side + 8,
            y * self.square_side + 8,
            self.square_side - 16,
            self.square_side - 16,
        )
        pygame.draw.rect(
            self.display,
            (int(color[0] / 2), int(color[1] / 2), int(color[2] / 2)),
            square,
            0,
        )
        pygame.draw.rect(self.display, color, inner_square, 0)

    def _delete_rectangle(self, rectangle):
        """Deletes the specified area"""
        pygame.draw.rect(self.display, Cuatris.colors[0], rectangle, 0)

    def draw(self, x_ini, y_ini):
        """Draws the specified piece from the coordinates (rows, columns
        --not pixels) x_ini, y_ini"""
        # update the position of the piece
        self.x = x_ini
        self.y = y_ini
        for i in range(0, len(self.matrix)):
            for j in range(0, len(self.matrix[i])):
                if self.matrix[i][j] != 0:
                    self._draw_square(
                        x_ini + j, y_ini + i, Cuatris.colors[self.matrix[i][j]]
                    )

    def delete(self, x_ini, y_ini):
        """Deletes the specified piece from the coordinates (rows, columns
        --not pixels) x_ini, y_ini"""
        for i in range(0, len(self.matrix)):
            for j in range(0, len(self.matrix[i])):
                if self.matrix[i][j] != 0:
                    self._draw_square(x_ini + j, y_ini + i, Cuatris.colors[0])

    # Piece movement
    def move(self, delta_x, delta_y):
        """Moves the piece the given delta, expressed in rows and columns
        --not pixels"""
        self.x = self.x + delta_x
        self.y = self.y + delta_y

    # Piece status
    def self_draw(self):
        """Draws the piece in its coordinates"""
        self.draw(self.x, self.y)

    def self_delete(self):
        """Deletes the piece from its coordinates"""
        self.delete(self.x, self.y)

    def is_colliding_with(self, other):
        """Checks for the collision of this piece with other"""
        for i in range(0, len(self.matrix)):
            for j in range(0, len(self.matrix[i])):
                if self.matrix[i][j] != 0:
                    if other.matrix[self.y + i][self.x + j] != 0:
                        return True
        return False


class Container(Piece):
    """Container where the game takes place"""

    def _remove_row(self, row):
        """removes the given row, adding a new one on the top of the
        Container"""
        for row in range(row, 0, -1):
            self.matrix[row] = self.matrix[row - 1]
        self.matrix[0] = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

    def count_lines(self, other_piece):
        """checks how many lines are completed with a new piece"""
        lines = 0
        for row in range(other_piece.y, other_piece.y + other_piece.rows):
            product = 1
            for value in self.matrix[row]:
                product = product * value
                if product == 0:
                    break
            if product > 0:
                lines = lines + 1
                self._remove_row(row)
        return lines

    def incorporate(self, other_piece):
        """incorporates the other piece\'s matrix to the Container, returning
        the number of completed rows --this is to be used when a piece
        collides with the bottom of the container"""
        for i in range(0, len(other_piece.matrix)):
            for j in range(0, len(other_piece.matrix[i])):
                if other_piece.matrix[i][j] != 0:
                    self.matrix[other_piece.y + i][
                        other_piece.x + j
                    ] = other_piece.matrix[i][j]
        return self.count_lines(other_piece)


class Cuatris:
    """Cuatris Object: implements game logic"""

    # Color definitions
    WHITE = (255, 255, 255)
    GRAY = (127, 127, 127)
    BLACK = (0, 0, 0)
    PURPLE = (200, 0, 200)
    GREEN = (0, 200, 0)
    RED = (200, 0, 0)
    BLUE = (0, 0, 200)
    YELLOW = (200, 200, 0)
    CYAN = (0, 200, 200)
    ORANGE = (255, 102, 16)
    colors = [BLACK, GRAY, CYAN, BLUE, ORANGE, GREEN, RED, PURPLE, YELLOW]

    # These are the matrix for the different pieces of the game. The numbers
    # will index the color in the previous array, so that then it is easy for
    # the game to draw it.

    matrix_L = [(7, 0), (7, 0), (7, 7)]

    matrix_J = [(0, 8), (0, 8), (8, 8)]

    matrix_I = [(6, 0), (6, 0), (6, 0), (6, 0)]

    matrix_S = [(0, 2, 2), (2, 2, 0)]

    matrix_Z = [(4, 4, 0), (0, 4, 4)]

    matrix_T = [(5, 5, 5), (0, 5, 0)]

    matrix_O = [(3, 3), (3, 3)]

    matrices = [
        0,
        0,
        matrix_L,
        matrix_J,
        matrix_I,
        matrix_S,
        matrix_Z,
        matrix_T,
        matrix_O,
    ]

    next_matrix = [
        [1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1],
    ]

    # Frames per Second
    FPS = 60

    # Gravity Event
    GRAVITY = pygame.USEREVENT + 1

    # Initial coordinates for the pieces
    x_ini = 4
    y_ini = 0

    def __init__(self, square_side):
        try:
            self.slot = int(square_side)
        except ValueError:
            # Default value
            self.slot = 40
        self.lines = 0
        self.lines_for_next_level = 20
        self.level = 0
        self.width = 19 * self.slot
        self.height = 22 * self.slot

        pygame.init()

        # display definition
        self.display = pygame.display.set_mode((self.width, self.height))
        self.display.fill(Cuatris.BLACK)
        matrix_container = [
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
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
        self.next = Container(Cuatris.next_matrix, self.display, self.slot)
        self.next.draw(13, 0)

        self.container = Container(matrix_container, self.display, self.slot)
        self.container.draw(0, 0)

        self.piece = self.get_next_piece()
        self.piece.draw(4, 0)
        self.next_piece = self.get_next_piece()
        self.next_piece.draw(15, 1)

        pygame.display.update()

        # Game clock
        self.clock = pygame.time.Clock()

        # Gravity Event

        self.t_FALL = 70
        self.t_GRAVITY = 2000  # milliseconds
        pygame.time.set_timer(Cuatris.GRAVITY, self.t_GRAVITY)

    def get_next_piece(self):
        """Creates a random next piece"""
        n_piece = random.randint(2, 8)
        piece = Piece(self.matrices[n_piece], self.display, self.slot)
        return piece

    def _print(self, font, string, left, top, color, background):
        """Prints a string"""
        text = font.render(string, True, color, background)
        text_rectangle = text.get_rect()
        text_rectangle.left = left
        text_rectangle.top = top
        self.display.blit(text, text_rectangle)

    def score(self):
        """Prints the score"""
        basic_font = pygame.font.SysFont(None, self.slot)
        self._print(
            basic_font,
            "Lines: " + str(self.lines),
            13 * self.slot,
            8 * self.slot,
            Cuatris.WHITE,
            Cuatris.BLACK,
        )
        self._print(
            basic_font,
            "Level: " + str(self.level),
            13 * self.slot,
            9 * self.slot,
            Cuatris.GRAY,
            Cuatris.BLACK,
        )
        self._print(
            basic_font,
            "Next: " + str(self.lines_for_next_level),
            13 * self.slot,
            10 * self.slot,
            Cuatris.GRAY,
            Cuatris.BLACK,
        )

    def game_over(self):
        """Prompts the user for a next game / quit"""
        basic_font = pygame.font.SysFont(None, self.slot)  # to refactor
        left = self.display.get_rect().centerx - len("GAME O") * self.slot
        top = self.display.get_rect().centery
        self._print(
            basic_font, "GAME OVER", left, top, Cuatris.RED, Cuatris.GRAY
        )
        self._print(
            basic_font,
            "RETURN TO START OVER",
            left,
            top + self.slot,
            Cuatris.RED,
            Cuatris.GRAY,
        )

    @staticmethod
    def turn(counterclockwise, piece, container):
        """Turns a piece"""
        piece.self_delete()
        if counterclockwise:
            piece.rotate_minus_90()
        else:
            piece.rotate90()
        while piece.is_colliding_with(container):
            piece.move(-1, 0)
        piece.self_draw()

    @staticmethod
    def move_right(units, piece, container):
        """Moves a piece the given units (squares) to the right"""
        piece.self_delete()
        piece.move(units, 0)
        if piece.is_colliding_with(container):
            piece.move(-units, 0)
        piece.self_draw()

    def _process_gravity(self):
        """This method makes the current piece fall 1 square, and checks for
        the consequences of it"""
        game_should_continue = True

        # Move a piece one square downwards
        self.piece.self_delete()
        self.piece.move(0, 1)

        if self.piece.is_colliding_with(self.container):
            # Reset gravity in case user was pressing down arrow
            pygame.time.set_timer(Cuatris.GRAVITY, self.t_GRAVITY)

            # Back one square (collision implies overlapping)
            self.piece.move(0, -1)

            # Redraw container adding the colliding piece
            self.container.self_delete()
            self.lines = self.lines + self.container.incorporate(self.piece)
            # Check if the user advanced levels
            if self.lines >= self.lines_for_next_level:
                self.level = self.level + 1
                self.lines_for_next_level = self.lines_for_next_level + 20
                if self.t_GRAVITY > 100:
                    self.t_GRAVITY = self.t_GRAVITY - 1000
            # Update score, spawn a new piece and calculate and redraw next
            # piece
            self.score()
            self.container.self_draw()
            self.next_piece.self_delete()
            self.piece = self.next_piece
            self.piece.draw(4, 0)
            self.next_piece = self.get_next_piece()
            self.next_piece.draw(15, 1)

            # If the new piece is colliding upon spawn, game over
            if self.piece.is_colliding_with(self.container):
                game_should_continue = False
        else:
            self.piece.self_draw()
        return game_should_continue

    def _play_again(self):
        """Process the user response to the question of whether he/she wants to
        play again. Return returns True to play again; any other key returns
        False to exit the game."""
        while True:
            # Pause until next tick
            self.clock.tick(Cuatris.FPS)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return True
                    else:
                        return False

    def run_game(self):
        """Game and Event loop"""
        is_continue = True

        self.score()

        # Game loop
        while is_continue:
            # Pause until next tick
            self.clock.tick(Cuatris.FPS)

            # Event Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                else:
                    # Process gravity
                    if event.type == Cuatris.GRAVITY:
                        is_continue = self._process_gravity()
                    if event.type == pygame.KEYDOWN:
                        # Piece turning can cause collisions to the right
                        if event.key == pygame.K_z:
                            self.turn(True, self.piece, self.container)
                        if event.key == pygame.K_x:
                            self.turn(False, self.piece, self.container)
                        if event.key == pygame.K_LEFT:
                            self.move_right(-1, self.piece, self.container)
                        if event.key == pygame.K_RIGHT:
                            self.move_right(1, self.piece, self.container)
                        # accelerate gravity
                        if event.key == pygame.K_DOWN:
                            pygame.time.set_timer(Cuatris.GRAVITY, self.t_FALL)

                    # Release any key means fall speed back to gravity
                    if event.type == pygame.KEYUP:
                        pygame.time.set_timer(Cuatris.GRAVITY, self.t_GRAVITY)
                if not is_continue:
                    self.game_over()
                pygame.display.update()

        return self._play_again()


# This code executes the game.
play = True
while play:
    game = Cuatris(30)
    play = game.run_game()

print("Thanks for playing!")
pygame.quit()
