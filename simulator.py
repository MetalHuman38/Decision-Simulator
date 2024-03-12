import pygame
import sys
import numpy as np
import random
import copy

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
        self.empty_squares = self.squares  # [list of empty squares]
        self.marked_squares = 0  # To keep track of the number of marked squares

    # final_state method
    def final_state(self, show=False):
        '''
          @return 0 if no player has won
          @return 1 if player 1 has won
          @return 2 if player 2 has won
        '''
 
        # vertical win
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRCLE_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]
            
        # horizontal win
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRCLE_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
                return self.squares[row][0]
  
        # desc diagonal win
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRCLE_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                    iPos = (20, 20)
                    fPos = (WIDTH - 20, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]
  
        # asc diagonal win
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRCLE_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        return 0

    def mark_square(self, row, col, player):
        self.squares[row][col] = player
        self.marked_squares += 1  # Indicates when the board is full

    def empty_square(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_squares(self):
        return [(i, j) for i in range(3) for j in range(3) if self.squares[i][j] == 0]  # Return a list of empty squares

    # def get_empty_sq(self):
    #     empty_sqrs = []
    #     for row in range(ROWS):
    #         for col in range(COLS):
    #             if self.squares[row][col] == 0:
    #                 empty_sqrs.append((row, col))
    #     return empty_sqrs

    def is_full(self):
        return self.marked_squares == 9  # check if the board is full

    def is_empty(self):
        return self.marked_squares == 0  # check if the board is empty


class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player
        
    def random_move(self, board):
        empty_squares = board.get_empty_squares()
        index = random.randrange(0, len(empty_squares))
        return empty_squares[index]  # (row, col)
    
    def minimax(self, board, is_maximizing):
        # Check terminal cases
        case = board.final_state()
        # player 1 wins
        if case == 1:
            return 1, None  # evaluate the move
        # player 2 wins AI
        elif case == 2:
            return -1, None  # evaluate the move
        # draw
        elif board.is_full():
            return 0, None  # evaluate the move
        
        # Maximizing player
        if is_maximizing:
            max_score = -1000
            best_move = None
            empty_sqrs = board.get_empty_squares()
            for row, col in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_score:
                    max_score = eval
                    best_move = (row, col)
            return max_score, best_move
        
        # Minimizing player
        elif not is_maximizing:
            min_score = 1000
            best_move = None
            empty_sqrs = board.get_empty_squares()
            for row, col in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_score:
                    min_score = eval
                    best_move = (row, col)
            return min_score, best_move
        
    def evaluate(self, main_board):
        if self.level == 0:
            move = self.random_move(main_board)
        else:
            evaluate, move = self.minimax(main_board, False)
        print(f"Cancer has chosen to mark the square in pos {move} with the evaluation of {evaluate}")
        return move  # (row, col)


class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1  # player 1-cross #2-circles # set 1 for player 1 to start or 2 for AI to start
        self.game_mode = 'ai'  # playerVSai or playerVSplayer
        self.running = True
        self.draw_lines()
        
    def make_move(self, row, col):
        self.board.mark_square(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()
        print(f"Doctor {self.player} has marked the square in pos {row, col}")

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
        
    def change_game_mode(self):
        self.game_mode = 'ai' if self.game_mode == 'playerVSplayer' else 'playerVSplayer'
        print(f"Game mode changed to {self.game_mode}")
        
    def isOver(self):
        return self.board.final_state(show=True) != 0 or self.board.is_full()
        
    def reset(self):
        self.__init__()
        
        
# Main loop
def main():

    # Create an instance of the Game class
    game = Game()
    board = game.board
    ai = game.ai

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
                # Change game mode.
            if event.type == pygame.KEYDOWN:
                
                # sets game to player vs player mode
                if event.key == pygame.K_g:
                    game.change_game_mode()
                    
                # Resets the screen to start playing.
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai
                    
                # change AI's level
                if event.type == pygame.K_0:
                    ai.level = 0
                    
                # 1-random AI
                if event.key == pygame.K_1:
                    ai.level = 1
                    
            # Human marking cells
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position of the mouse
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE

                if board.empty_square(row, col) and game.running:
                    game.make_move(row, col)
                    
                    if game.isOver():
                        game.running = False
                    
        # AI marking cells
        if game.game_mode == 'ai' and game.player == ai.player and game.running:
            pygame.display.update()
            row, col = ai.evaluate(board)
            game.make_move(row, col)
            if game.isOver():
                game.running = False
                           
        pygame.display.update()


main()
