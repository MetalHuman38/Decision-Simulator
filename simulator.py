import pygame
import sys
import numpy as np

# Importing constants from constants.py
from constants import (WIDTH, HEIGHT,
                       BG_COLOR, ROWS,
                       COLS, SQSIZE,
                       LINE_COLOR,
                       LINE_WIDTH,
                       CIRCLE_COLOR,
                       CIRCLE_WIDTH,
                       RADIUS,
                       CROSS_COLOR,
                       CROSS_WIDTH,
                       OFFSET)

# Initialize the pygame library
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Simulator')
screen.fill(BG_COLOR)


class Board:
    def __init__(self):
        # Create a 3x3 matrix of zeros to represent initial state of the board
        self.squares = np.zeros((ROWS, COLS))

    def mark_square(self, row, col, doctor):
        self.squares[row][col] = doctor

    def empty_square(self, row, col):
        return self.squares[row][col] == 0


class Game:
    def __init__(self):
        self.board = Board()
        self.player = 1  # player 1-cross #2-circles
        self.draw_lines()

    def draw_lines(self):
        # Clear the screen with the background color
        screen.fill(BG_COLOR)
        # Horizontal lines
        for i in range(ROWS):
            pygame.draw.line(screen, LINE_COLOR, (0, i * HEIGHT / ROWS), (WIDTH, i * HEIGHT / ROWS), LINE_WIDTH)
        # Vertical lines
        for i in range(COLS):
            pygame.draw.line(screen, LINE_COLOR, (i * WIDTH / COLS, 0), (i * WIDTH / COLS, HEIGHT), LINE_WIDTH)

        pygame.display.update()

    def draw_fig(self, row, col):
        if self.player == 1:
            # draw cross
            # descending line
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

            # ascending line
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            center = (col * WIDTH / COLS + WIDTH / COLS // 2, row * HEIGHT / ROWS + HEIGHT / ROWS // 2)
            pygame.draw.circle(screen, CIRCLE_COLOR, center, RADIUS, CIRCLE_WIDTH)

    def next_turn(self):
        self.player = self.player % 2 + 1


# Main loop
def main():

    # Create an instance of the Game class
    game = Game()
    board = game.board

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position of the mouse
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE

                if board.empty_square(row, col):
                    board.mark_square(row, col, game.player)
                    game.draw_fig(row, col)
                    game.next_turn()
                    print(board.squares)

        pygame.display.update()


main()