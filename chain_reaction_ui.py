#!/usr/bin/env python3
import pygame, subprocess, time, os, sys
from graphics import CELL_SIZE, draw_board, BG, RED, BLUE, get_font

ROWS, COLS = 9, 6
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE
FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'gamestate.txt')
ENGINE = os.path.join(os.path.dirname(__file__), '..', 'backend', 'build', 'chain_reaction_engine')
DEPTH = '4'
HEURISTIC = '0'        # composite

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chain Reaction – Human vs AI')
clock = pygame.time.Clock()

board = [['0' for _ in range(COLS)] for _ in range(ROWS)]
header = 'AI Move:'  # Start with AI so human (red) goes first

# --- New variables for game state tracking ---
game_over = False
winner = None
turn_count = 0
# -------------------------------------------

# Ensure file exists
with open(FILE_PATH, 'w') as f:
    f.write(header + '\n')
    for r in range(ROWS):
        f.write(' '.join('0' for _ in range(COLS)) + '\n')


def check_game_over():
    """Checks the board for a win condition."""
    global game_over, winner
    # The game can only end after the first couple of moves.
    if turn_count < 2:
        return

    red_present = False
    blue_present = False
    for row in board:
        for cell in row:
            if cell.endswith('R'):
                red_present = True
            elif cell.endswith('B'):
                blue_present = True

    # If only one color remains, declare a winner.
    if red_present and not blue_present:
        winner = 'RED'
        game_over = True
    elif blue_present and not red_present:
        winner = 'BLUE'
        game_over = True


def parse_file():
    global header
    if not os.path.exists(FILE_PATH):
        return
    with open(FILE_PATH) as f:
        lines = f.read().strip().split('\n')
    header = lines[0]
    for r in range(ROWS):
        row_tokens = lines[1 + r].split()
        board[r] = [tok if tok != '0' else '0' for tok in row_tokens]


def write_file():
    with open(FILE_PATH, 'w') as f:
        f.write('Human Move:\n')
        for r in range(ROWS):
            f.write(' '.join(board[r]) + '\n')


def wait_ai():
    global turn_count
    mtime = os.path.getmtime(FILE_PATH)
    # spawn engine
    subprocess.Popen([ENGINE, FILE_PATH, 'B', DEPTH, HEURISTIC])
    # poll for change
    while os.path.getmtime(FILE_PATH) == mtime:
        time.sleep(0.05)
    
    parse_file()
    turn_count += 1
    check_game_over()


def handle_click(pos):
    global turn_count
    if game_over:  # Prevent moves after the game has ended
        return

    x, y = pos
    c, r = x // CELL_SIZE, y // CELL_SIZE
    tok = board[r][c]
    if tok == '0' or tok[1] == 'R':
        # place red orb
        if tok == '0':
            board[r][c] = '1R'
        else:
            count = int(tok[0]) + 1
            board[r][c] = f"{count}R"
        
        write_file()
        turn_count += 1
        check_game_over()
        if not game_over:
            wait_ai()


def render():
    screen.fill(BG)
    draw_board(screen, board)
    
    if game_over:
        # Display winner message on a semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        win_color = RED if winner == 'RED' else BLUE
        win_text = f"{winner} PLAYER WINS!"
        font = get_font(48)
        text_surf = font.render(win_text, True, win_color)
        text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surf, text_rect)

    pygame.display.flip()

parse_file()
render()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Add 'and not game_over' to prevent clicks after winning
        elif event.type == pygame.MOUSEBUTTONDOWN and header == 'AI Move:' and not game_over:
            handle_click(event.pos)
    
    render()
    clock.tick(30)
pygame.quit()