import pygame
import sys
import numpy as np

# Importing constants from constants.py
from constants import (WIDTH, HEIGHT, BG_COLOR, ROWS, COLS, SQSIZE, LINE_COLOR, LINE_WIDTH)
# from constants import *


# Initialize the pygame library
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Simulator')
screen.fill(BG_COLOR)


class Board:
    def __init__(self):
        # Create a 3x3 matrix of zeros to represent initial state of the board
        self.squares = np.zeros((ROWS, COLS))

    def mark_square(self, row, col, player):
        self.squares[row][col] = player


class Game:
    def __init__(self):
        self.board = Board()
        self.DOCTOR = 1
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
        # Update the display
        pygame.display.update()


# Main loop
def main():

    # Create an instance of the Game class
    game = Game()

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
                print(row, col)
        game.draw_lines()

        pygame.display.update()


main()
