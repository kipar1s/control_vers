import pygame
import random
import sys

# Инициализация pygame
pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Настройки FPS
FPS = 10

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")
font = pygame.font.SysFont("Arial", 36)

# Функции для экранов
def draw_text(text, color, x, y):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

def start_screen():
    screen.fill(BLACK)
    draw_text("Змейка", WHITE, WIDTH // 2 - 80, HEIGHT // 2 - 100)
    draw_text("Нажмите ПРОБЕЛ для начала", WHITE, WIDTH // 2 - 200, HEIGHT // 2)
    pygame.display.flip()
    wait_for_key(pygame.K_SPACE)

def game_over_screen(score):
    screen.fill(BLACK)
    draw_text(f"Вы проиграли! Очки: {score}", RED, WIDTH // 2 - 150, HEIGHT // 2 - 100)
    draw_text("Нажмите R для перезапуска", WHITE, WIDTH // 2 - 180, HEIGHT // 2)
    pygame.display.flip()
    wait_for_key(pygame.K_r)

def win_screen(score):
    screen.fill(BLACK)
    draw_text(f"Вы победили! Очки: {score}", BLUE, WIDTH // 2 - 150, HEIGHT // 2 - 100)
    draw_text("Нажмите R для перезапуска", WHITE, WIDTH // 2 - 180, HEIGHT // 2)
    pygame.display.flip()
    wait_for_key(pygame.K_r)

def wait_for_key(key):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == key:
                return

# Функция для сброса игры
def reset_game():
    global snake, direction, food, score, game_active
    snake = [(100, 100), (90, 100), (80, 100)]  # Начальное тело змейки
    direction = 'RIGHT'
    food = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
            random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)
    score = 0
    game_active = True

# Основные переменные
reset_game()

# Функция для рисования объектов
def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))

def draw_food(food):
    pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE))

# Основной игровой цикл
start_screen()
clock = pygame.time.Clock()
while True:
    if not game_active:
        reset_game()
        start_screen()

    screen.fill(BLACK)
    draw_text(f"Очки: {score}", WHITE, 10, 10)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Управление змейкой
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != 'DOWN':
        direction = 'UP'
    if keys[pygame.K_DOWN] and direction != 'UP':
        direction = 'DOWN'
    if keys[pygame.K_LEFT] and direction != 'RIGHT':
        direction = 'LEFT'
    if keys[pygame.K_RIGHT] and direction != 'LEFT':
        direction = 'RIGHT'

    # Обновление позиции змейки
    x, y = snake[0]
    if direction == 'UP':
        y -= CELL_SIZE
    if direction == 'DOWN':
        y += CELL_SIZE
    if direction == 'LEFT':
        x -= CELL_SIZE
    if direction == 'RIGHT':
        x += CELL_SIZE
    new_head = (x, y)

    # Проверка на столкновение с самим собой или границами экрана
    if new_head in snake or x < 0 or y < 0 or x >= WIDTH or y >= HEIGHT:
        game_active = False
        game_over_screen(score)

    # Добавляем новую голову змейки
    snake.insert(0, new_head)

    # Проверка на поедание еды
    if new_head == food:
        score += 1
        if score == 50:
            game_active = False
            win_screen(score)
        else:
            food = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                    random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)
    else:
        snake.pop()  # Убираем хвост, если еда не съедена

    # Рисуем змейку и еду
    draw_snake(snake)
    draw_food(food)

    # Обновляем экран
    pygame.display.flip()
    clock.tick(FPS)
