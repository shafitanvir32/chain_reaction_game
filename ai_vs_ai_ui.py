import pygame, subprocess, time, os, sys
from graphics import CELL_SIZE, draw_board, BG, RED, BLUE, get_font

ROWS, COLS = 9, 6
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE

AI_RED_DEPTH = '3'
AI_RED_HEURISTIC = '0' 

AI_BLUE_DEPTH = '3'
AI_BLUE_HEURISTIC = '0' 

FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'gamestate.txt')
ENGINE = os.path.join(os.path.dirname(__file__), '..', 'backend', 'build', 'chain_reaction_engine')
if sys.platform == "win32":
    ENGINE += ".exe"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chain Reaction – AI vs AI')
clock = pygame.time.Clock()

board = [['0' for _ in range(COLS)] for _ in range(ROWS)]
header = 'AI Move:'
game_over = False
winner = None
turn_count = 0
ai_process = None
def init_board():
    with open(FILE_PATH, 'w') as f:
        f.write('AI Move:\n')
        for r in range(ROWS):
            f.write(' '.join('0' for _ in range(COLS)) + '\n')

def parse_file():
    global header
    try:
        if not os.path.exists(FILE_PATH): return
        with open(FILE_PATH, 'r') as f:
            lines = f.read().strip().split('\n')
        header = lines[0]
        for r, line in enumerate(lines[1:]):
            if r < ROWS:
                board[r] = line.split()
    except Exception as e:
        print(f"Error parsing file: {e}")

def check_game_over():
    global game_over, winner
    if turn_count < 2: return
    red_present = any('R' in cell for row in board for cell in row)
    blue_present = any('B' in cell for row in board for cell in row)
    if red_present and not blue_present:
        winner = 'RED'
        game_over = True
    elif blue_present and not red_present:
        winner = 'BLUE'
        game_over = True

def render():
    screen.fill(BG)
    draw_board(screen, board)
    if ai_process and ai_process.poll() is None:
        font = get_font(36)
        thinking_text = "AI is thinking..."
        text_surf = font.render(thinking_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surf, text_rect)
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        win_color = RED if winner == 'RED' else BLUE
        win_text = f"AI {winner} WINS!"
        font = get_font(50)
        text_surf = font.render(win_text, True, win_color)
        text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surf, text_rect)
    pygame.display.flip()

init_board()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if ai_process and ai_process.poll() is not None:
        ai_process = None
        turn_count += 1
        parse_file()
        check_game_over()
    if not ai_process and not game_over:
        parse_file()
        if header == 'AI Move:':
            ai_process = subprocess.Popen([ENGINE, FILE_PATH, 'R', AI_RED_DEPTH, AI_RED_HEURISTIC])
        else:
            ai_process = subprocess.Popen([ENGINE, FILE_PATH, 'B', AI_BLUE_DEPTH, AI_BLUE_HEURISTIC])
    render()
    clock.tick(30)

pygame.quit()