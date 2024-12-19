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
 
# Настройки FPS 
FPS = 10 
 
# Создание экрана 
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Змейка") 
 
# Основные переменные 
snake = [(100, 100), (90, 100), (80, 100)]  # Начальное тело змейки 
direction = 'RIGHT'  # Направление змейки 
food = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE, 
        random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE) 
 
# Функция для рисования объектов 
def draw_snake(snake): 
    for segment in snake: 
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE)) 
 
def draw_food(food): 
    pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE)) 
 
# Основной игровой цикл 
clock = pygame.time.Clock() 
running = True 
while running: 
    screen.fill(BLACK) 
 
    # Обработка событий 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 
 
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
        running = False 
 
    # Добавляем новую голову змейки 
    snake.insert(0, new_head) 
 
    # Проверка на поедание еды 
    if new_head == food: 
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
 
pygame.quit() 
sys.exit()