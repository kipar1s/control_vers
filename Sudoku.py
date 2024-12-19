import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 540, 600
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE
FONT = pygame.font.SysFont("comicsans", 40)
SMALL_FONT = pygame.font.SysFont("comicsans", 25)
BACKGROUND_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
SELECTED_COLOR = (255, 200, 200)  # Нежно-красный цвет для выбранной клетки

# Функция для отрисовки сетки
def draw_grid(win):
    for i in range(GRID_SIZE + 1):
        line_width = 4 if i % 3 == 0 else 1
        pygame.draw.line(win, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), line_width)
        pygame.draw.line(win, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH), line_width)

# Генерация поля Судоку
def generate_sudoku():
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    # Заполнение некоторых случайных чисел
    for _ in range(20):
        row, col = random.randint(0, 8), random.randint(0, 8)
        num = random.randint(1, 9)
        while not is_valid(grid, row, col, num) or grid[row][col] != 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            num = random.randint(1, 9)
        grid[row][col] = num

    solve(grid)
    remove_numbers(grid, 40)
    return grid

# Удаление чисел для создания головоломки
def remove_numbers(grid, holes):
    while holes > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if grid[row][col] != 0:
            grid[row][col] = 0
            holes -= 1

# Проверка допустимости числа
def is_valid(grid, row, col, num):
    if num in grid[row]:
        return False
    if num in [grid[i][col] for i in range(GRID_SIZE)]:
        return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False
    return True

# Решение Судоку
def solve(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(grid, row, col, num):
                        grid[row][col] = num
                        if solve(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True

# Отрисовка чисел и подсветки выбранной клетки
def draw_numbers_and_highlight(win, grid, selected_cell):
    # Подсветка выбранной клетки
    if selected_cell:
        row, col = selected_cell
        pygame.draw.rect(win, SELECTED_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Отрисовка чисел
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] != 0:
                x, y = col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2
                text = FONT.render(str(grid[row][col]), True, LINE_COLOR)
                win.blit(text, text.get_rect(center=(x, y)))

# Основная функция
def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Судоку")
    clock = pygame.time.Clock()

    grid = generate_sudoku()
    solution = [row[:] for row in grid]
    solve(solution)
    selected_cell = None
    fixed_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] != 0]

    running = True
    while running:
        win.fill(BACKGROUND_COLOR)
        draw_grid(win)
        draw_numbers_and_highlight(win, grid, selected_cell)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                selected_cell = y // CELL_SIZE, x // CELL_SIZE

            if event.type == pygame.KEYDOWN:
                if selected_cell and selected_cell not in fixed_cells:
                    row, col = selected_cell
                    if event.key == pygame.K_1:
                        grid[row][col] = 1
                    elif event.key == pygame.K_2:
                        grid[row][col] = 2
                    elif event.key == pygame.K_3:
                        grid[row][col] = 3
                    elif event.key == pygame.K_4:
                        grid[row][col] = 4
                    elif event.key == pygame.K_5:
                        grid[row][col] = 5
                    elif event.key == pygame.K_6:
                        grid[row][col] = 6
                    elif event.key == pygame.K_7:
                        grid[row][col] = 7
                    elif event.key == pygame.K_8:
                        grid[row][col] = 8
                    elif event.key == pygame.K_9:
                        grid[row][col] = 9
                    elif event.key == pygame.K_BACKSPACE:
                        grid[row][col] = 0
                    elif event.key == pygame.K_RETURN:
                        if grid == solution:
                            print("Congratulations! You've solved the Sudoku!")
                            running = False

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
    pygame.quit()