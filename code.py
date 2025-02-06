import numpy as np
import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARE_SIZE = 100
RADIUS = SQUARE_SIZE // 2 - 5
WIDTH = COLUMN_COUNT * SQUARE_SIZE
HEIGHT = (ROW_COUNT + 1) * SQUARE_SIZE
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Game variables
board = np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)
player_turn = 1  # Player 1 starts

# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect Four")
font = pygame.font.SysFont("monospace", 50)

def draw_board():
    screen.fill(WHITE)
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            pygame.draw.rect(screen, BLUE, (col * SQUARE_SIZE, (row + 1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, WHITE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)

    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            if board[row][col] == 1:
                pygame.draw.circle(screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - (row * SQUARE_SIZE + SQUARE_SIZE // 2)), RADIUS)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, YELLOW, (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - (row * SQUARE_SIZE + SQUARE_SIZE // 2)), RADIUS)

    pygame.display.update()

def drop_piece(col, piece):
    for row in range(ROW_COUNT-1, -1, -1):
        if board[row][col] == 0:
            board[row][col] = piece
            return True
    return False

def check_win(piece):
    # Check horizontal
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT - 3):
            if all(board[row][col + i] == piece for i in range(4)):
                return True

    # Check vertical
    for row in range(ROW_COUNT - 3):
        for col in range(COLUMN_COUNT):
            if all(board[row + i][col] == piece for i in range(4)):
                return True

    # Check positive diagonal
    for row in range(ROW_COUNT - 3):
        for col in range(COLUMN_COUNT - 3):
            if all(board[row + i][col + i] == piece for i in range(4)):
                return True

    # Check negative diagonal
    for row in range(3, ROW_COUNT):
        for col in range(COLUMN_COUNT - 3):
            if all(board[row - i][col + i] == piece for i in range(4)):
                return True

    return False

def reset_game():
    global board, player_turn
    board = np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)
    player_turn = 1
    draw_board()

# Main game loop
running = True
draw_board()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, SQUARE_SIZE))
            posx = event.pos[0]
            color = RED if player_turn == 1 else YELLOW
            pygame.draw.circle(screen, color, (posx, SQUARE_SIZE // 2), RADIUS)
            pygame.display.update()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            col = event.pos[0] // SQUARE_SIZE
            if drop_piece(col, player_turn):
                if check_win(player_turn):
                    text = font.render(f"Player {player_turn} Wins!", True, RED if player_turn == 1 else YELLOW)
                    screen.blit(text, (50, 10))
                    pygame.display.update()
                    pygame.time.delay(2000)
                    reset_game()
                else:
                    player_turn = 3 - player_turn  # Switch turn (1 → 2, 2 → 1)
                draw_board()

pygame.quit()
sys.exit()
