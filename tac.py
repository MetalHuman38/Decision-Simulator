import pygame
import math
from itertools import cycle
from typing import NamedTuple


class Player(NamedTuple):
    label: str
    color: tuple


class Move(NamedTuple):
    row: int
    col: int
    label: str = ""
    color: tuple = (0, 0, 0)  # Default color is black


BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    Player(label="X", color=(0, 0, 255)),  # Blue
    Player(label="O", color=(0, 255, 0)),  # Green
)


class TicTacToeGame:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self._players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self._setup_board()

    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()

    def _get_winning_combos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]

    def toggle_player(self):
        """Return a toggled player."""
        self.current_player = next(self._players)

    def is_valid_move(self, move):
        """Return True if move is valid, and False otherwise."""
        row, col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label == ""
        no_winner = not self._has_winner
        return no_winner and move_was_not_played

    def process_move(self, move):
        """Process the current move and check if it's a win."""
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        for combo in self._winning_combos:
            results = set(self._current_moves[n][m].label for n, m in combo)
            is_win = (len(results) == 1) and ("" not in results)
            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break

    def has_winner(self):
        """Return True if the game has a winner, and False otherwise."""
        return self._has_winner

    def is_tied(self):
        """Return True if the game is tied, and False otherwise."""
        no_winner = not self._has_winner
        played_moves = (
            move.label for row in self._current_moves for move in row
        )
        return no_winner and all(played_moves)

    def reset_game(self):
        """Reset the game state to play again."""
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self._has_winner = False
        self.winner_combo = []

    def get_empty_cells(self):
        """Return a list of empty cells."""
        empty_cells = []
        for row, row_content in enumerate(self._current_moves):
            for col, move in enumerate(row_content):
                if move.label == "":
                    empty_cells.append((row, col))
        return empty_cells

    def minimax(self, depth, is_maximizing, current_player):
        """Implement the minimax algorithm."""
        if self.has_winner():
            return -1 if is_maximizing else 1
        elif self.is_tied():
            return 0

        if is_maximizing:
            best_score = -math.inf
            for row, col in self.get_empty_cells():
                self._current_moves[row][col] = Move(row, col, current_player.label)
                if self.has_winner() and self.get_winner() == current_player.label:
                    score = 1  # AI wins
                elif self.has_winner() and self.get_winner() != current_player.label:
                    score = -1  # Player wins
                else:
                    score = self.minimax(depth + 1, False, current_player)
                self._current_moves[row][col] = Move(row, col)
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for row, col in self.get_empty_cells():
                self._current_moves[row][col] = Move(row, col, current_player.label)
                if self.has_winner() and self.get_winner() == current_player.label:
                    score = -1  # Player wins
                elif self.has_winner() and self.get_winner() != current_player.label:
                    score = 1  # AI wins
                else:
                    score = self.minimax(depth + 1, True, current_player)
                self._current_moves[row][col] = Move(row, col)
                best_score = min(score, best_score)
            return best_score

    def get_best_move(self, current_player):
        """Get the best move for the AI."""
        best_score = -math.inf
        best_move = None
        for row, col in self.get_empty_cells():
            self._current_moves[row][col] = Move(row, col, current_player.label)
            score = self.minimax(0, False, current_player)
            self._current_moves[row][col] = Move(row, col)
            if score > best_score:
                best_score = score
                best_move = (row, col)
        return best_move


class TicTacToeBoard:
    def __init__(self, game):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Tic-Tac-Toe Game")
        self.clock = pygame.time.Clock()
        self.game = game
        self.font = pygame.font.Font(None, 48)
        self._create_board()

    def _create_board(self):
        self.cells = []
        cell_width = self.screen.get_width() // self.game.board_size
        cell_height = self.screen.get_height() // self.game.board_size
        for row in range(self.game.board_size):
            for col in range(self.game.board_size):
                rect = pygame.Rect(col * cell_width, row * cell_height, cell_width, cell_height)
                self.cells.append(rect)

    def draw_board(self):
        self.screen.fill((255, 255, 255))
        for i, row in enumerate(self.game._current_moves):
            for j, move in enumerate(row):
                rect = self.cells[i * self.game.board_size + j]
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
                label_surface = self.font.render(move.label, True, move.color)
                label_rect = label_surface.get_rect(center=rect.center)
                self.screen.blit(label_surface, label_rect)
        pygame.display.flip()

    def play(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.game.has_winner() and not self.game.is_tied():
                        mouse_pos = pygame.mouse.get_pos()
                        for i, cell in enumerate(self.cells):
                            if cell.collidepoint(mouse_pos):
                                row, col = i // self.game.board_size, i % self.game.board_size
                                move = Move(row, col, self.game.current_player.label)
                                if self.game.is_valid_move(move):
                                    self.game.process_move(move)
                                    self.game.toggle_player()
                                    if not self.game.has_winner() and not self.game.is_tied():
                                        ai_row, ai_col = self.game.get_best_move(self.game.current_player)
                                        ai_move = Move(ai_row, ai_col, self.game.current_player.label)
                                        self.game.process_move(ai_move)
                                        self.game.toggle_player()
            self.draw_board()
            if self.game.has_winner():
                print(f'Player "{self.game.current_player.label}" won!')
                pygame.time.wait(3000)
                self.game.reset_game()
            elif self.game.is_tied():
                print("Tied game!")
                pygame.time.wait(3000)
                self.game.reset_game()
            self.clock.tick(60)


def main():
    game = TicTacToeGame()
    board = TicTacToeBoard(game)
    board.play()


if __name__ == "__main__":
    main()
