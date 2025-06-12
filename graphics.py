import pygame, math
CELL_SIZE = 60
MARGIN = 2
BG = (33, 34, 38)
RED = (220, 30, 40)
BLUE = (30, 120, 245)
EMPTY = (140, 140, 140)
FONT_CACHE = {}


def get_font(size):
    if size not in FONT_CACHE:
        FONT_CACHE[size] = pygame.font.SysFont("arial", size, bold=True)
    return FONT_CACHE[size]


def draw_board(screen, board):
    rows, cols = len(board), len(board[0])
    for r in range(rows):
        for c in range(cols):
            x = c * CELL_SIZE
            y = r * CELL_SIZE
            cell = board[r][c]
            pygame.draw.rect(screen, BG, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, EMPTY, (x, y, CELL_SIZE, CELL_SIZE), 1)
            if cell == '0':
                continue
            count, col = int(cell[0]), cell[1]
            color = RED if col == 'R' else BLUE
            radius = CELL_SIZE // 4
            if count == 1:
                pygame.draw.circle(screen, color, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), radius)
            elif count == 2:
                pygame.draw.circle(screen, color, (x + CELL_SIZE // 3, y + CELL_SIZE // 2), radius)
                pygame.draw.circle(screen, color, (x + 2 * CELL_SIZE // 3, y + CELL_SIZE // 2), radius)
            elif count == 3:
                pygame.draw.circle(screen, color, (x + CELL_SIZE // 2, y + CELL_SIZE // 3), radius)
                pygame.draw.circle(screen, color, (x + CELL_SIZE // 3, y + 2 * CELL_SIZE // 3), radius)
                pygame.draw.circle(screen, color, (x + 2 * CELL_SIZE // 3, y + 2 * CELL_SIZE // 3), radius)
            else:
                # 4+ (rare) – draw number
                pygame.draw.circle(screen, color, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), radius)
                txt = get_font(16).render(str(count), True, (255, 255, 255))
                rect = txt.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                screen.blit(txt, rect)