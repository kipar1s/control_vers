import pygame
import random
import sys

# Настройки игры
SIZE_OPTIONS = {1: 4, 2: 6}  # 1 - 4x4, 2 - 6x6
WIDTH_OPTIONS = {4: 400, 6: 600}
HEIGHT_OPTIONS = {4: 400, 6: 600}
TILE_SIZE_OPTIONS = {4: 100, 6: 100}
FONT_SIZE_OPTIONS = {4: 50, 6: 100}

# Цвета
BACKGROUND_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

# Инициализация Pygame
pygame.init()
font = pygame.font.Font(None, 50)

# Переменные игры
score = 0
high_score = 0
size = 4
WIDTH = WIDTH_OPTIONS[size]
HEIGHT = HEIGHT_OPTIONS[size]
TILE_SIZE = TILE_SIZE_OPTIONS[size]
FONT_SIZE = FONT_SIZE_OPTIONS[size]

# Инициализация экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

# Функции для игры
def init_board():
    board = [[0] * size for _ in range(size)]
    add_new_tile(board)
    add_new_tile(board)
    return board

def add_new_tile(board):
    empty_tiles = [(i, j) for i in range(size) for j in range(size) if board[i][j] == 0]
    if empty_tiles:
        i, j = random.choice(empty_tiles)
        board[i][j] = 2 if random.random() < 0.9 else 4

def draw_board(board):
    screen.fill(BACKGROUND_COLOR)
    for i in range(size):
        for j in range(size):
            value = board[i][j]
            color = TILE_COLORS.get(value, TILE_COLORS[2048])
            pygame.draw.rect(screen, color, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if value != 0:
                text = font.render(str(value), True, (0, 0, 0))
                text_rect = text.get_rect(center=(j * TILE_SIZE + TILE_SIZE / 2, i * TILE_SIZE + TILE_SIZE / 2))
                screen.blit(text, text_rect)
    # Отображение очков и рекорда
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    high_score_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 50))
    pygame.display.update()

def slide_left(row):
    global score
    new_row = [num for num in row if num != 0]
    new_row += [0] * (size - len(new_row))
    for i in range(size - 1):
        if new_row[i] == new_row[i + 1] and new_row[i] != 0:
            new_row[i] *= 2
            score += new_row[i]  # Увеличиваем счет
            new_row[i + 1] = 0
    new_row = [num for num in new_row if num != 0]
    new_row += [0] * (size - len(new_row))
    return new_row

def move_left(board):
    new_board = [slide_left(row) for row in board]
    return new_board

def move_right(board):
    new_board = [slide_left(row[::-1])[::-1] for row in board]
    return new_board

def move_up(board):
    transposed = [list(row) for row in zip(*board)]
    new_board = [slide_left(row) for row in transposed]
    return [list(row) for row in zip(*new_board)]

def move_down(board):
    transposed = [list(row) for row in zip(*board)]
    new_board = [slide_left(row[::-1])[::-1] for row in transposed]
    return [list(row) for row in zip(*new_board)]

def has_moves(board):
    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                return True
            if j < size - 1 and board[i][j] == board[i][j + 1]:
                return True
            if i < size - 1 and board[i][j] == board[i + 1][j]:
                return True
    return False

def game_over_screen():
    screen.fill((0, 0, 0))
    game_over_text = font.render("Game Over!", True, (255, 255, 255))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    restart_text = font.render("Press R to Restart", True, (255, 255, 255))
    
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 40))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 40))
    
    pygame.display.update()

def main_menu():
    global size, WIDTH, HEIGHT, TILE_SIZE, FONT_SIZE
    while True:
        screen.fill((0, 0, 0))
        title_text = font.render("2048", True, (255, 255, 255))
        option_text1 = font.render("Press 1 for 4x4", True, (255, 255, 255))
        option_text2 = font.render("Press 2 for 6x6", True, (255, 255, 255))
        
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(option_text1, (WIDTH // 2 - option_text1.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(option_text2, (WIDTH // 2 - option_text2.get_width() // 2, HEIGHT // 2))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    size = SIZE_OPTIONS[1]
                    WIDTH = WIDTH_OPTIONS[size]
                    HEIGHT = HEIGHT_OPTIONS[size]
                    TILE_SIZE = TILE_SIZE_OPTIONS[size]
                    FONT_SIZE = FONT_SIZE_OPTIONS[size]
                    return init_board()
                elif event.key == pygame.K_2:
                    size = SIZE_OPTIONS[2]
                    WIDTH = WIDTH_OPTIONS[size]
                    HEIGHT = HEIGHT_OPTIONS[size]
                    TILE_SIZE = TILE_SIZE_OPTIONS[size]
                    FONT_SIZE = FONT_SIZE_OPTIONS[size]
                    return init_board()

# Основной игровой цикл
board = main_menu()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                new_board = move_left(board)
            elif event.key == pygame.K_RIGHT:
                new_board = move_right(board)
            elif event.key == pygame.K_UP:
                new_board = move_up(board)
            elif event.key == pygame.K_DOWN:
                new_board = move_down(board)
            elif event.key == pygame.K_r:  # Перезапуск игры
                board = init_board()
                score = 0
                continue
            else:
                continue

            if new_board != board:
                board = new_board
                add_new_tile(board)

            if not has_moves(board):
                if score > high_score:
                    high_score = score  # Обновляем рекорд
                game_over_screen()
                while True:  # Ожидание нажатия клавиши для перезапуска
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                            board = init_board()
                            score = 0
                            break
                    else:
                        continue
                    break
    
    draw_board(board)