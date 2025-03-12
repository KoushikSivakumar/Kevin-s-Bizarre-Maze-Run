import pygame
import random

pygame.init()

WIDTH, HEIGHT = 750, 750
WHITE, BLACK = (0, 0, 0), (255, 255, 255)
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

player_img = pygame.image.load("kevin.jpg")  
wall_img = pygame.image.load("nokia.jpg")
exit_img = pygame.image.load("house.jpg") 

def scale_images(cell_size):
    global player_img, wall_img, exit_img
    player_img = pygame.transform.scale(player_img, (cell_size, cell_size))
    wall_img = pygame.transform.scale(wall_img, (cell_size, cell_size))
    exit_img = pygame.transform.scale(exit_img, (cell_size, cell_size))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KEVIN'S BIZARRE MAZE RUN")

icon = pygame.image.load('kevin.jpg')
pygame.display.set_icon(icon)

# maze gen
def gen_maze(rows, cols):
    maze = [[1] * cols for m in range(rows)]

    def carve_path(x, y):
        maze[x][y] = 0
        random.shuffle(DIRECTIONS)
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 1:
                maze[x + dx][y + dy] = 0
                carve_path(nx, ny)

    carve_path(0, 0)
    return maze

# exit
def find_exit(maze, rows, cols):
    for i in range(rows - 1, -1, -1):
        for j in range(cols - 1, -1, -1):
            if maze[i][j] == 0:
                return i, j
    return rows - 1, cols - 1

# end card
def show_victory_screen():
    screen.fill((33, 59, 59))
    font = pygame.font.Font(None, 50)
    text = font.render("KEVIN IS HOME!", True, (80, 135, 135))
    screen.blit(text, (WIDTH // 3, HEIGHT // 3))

    button_rect = pygame.Rect(WIDTH // 3 + 45, HEIGHT // 2, 215, 60)
    pygame.draw.rect(screen, (171, 201, 201), button_rect)
    button_text = font.render("NEXT LEVEL", True, WHITE)
    screen.blit(button_text, (WIDTH // 3 + 40, HEIGHT // 2 + 10))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                waiting = False

# loop
level = 1
running = True
while running:
    ROWS, COLS = 10 + level * 5, 10 + level * 5
    CELL_SIZE = WIDTH // COLS
    scale_images(CELL_SIZE)  
    maze = gen_maze(ROWS, COLS)

    # start
    player_x, player_y = 0, 0
    exit_x, exit_y = find_exit(maze, ROWS, COLS)

    playing = True
    while playing:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                playing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == (pygame.K_LEFT or pygame.K_a) and player_y > 0 and maze[player_x][player_y - 1] == 0:
                    player_y -= 1
                if event.key == pygame.K_RIGHT and player_y < COLS - 1 and maze[player_x][player_y + 1] == 0:
                    player_y += 1
                if event.key == pygame.K_UP and player_x > 0 and maze[player_x - 1][player_y] == 0:
                    player_x -= 1
                if event.key == pygame.K_DOWN and player_x < ROWS - 1 and maze[player_x + 1][player_y] == 0:
                    player_x += 1

        for i in range(ROWS):
            for j in range(COLS):
                if maze[i][j] == 1:
                    screen.blit(wall_img, (j * CELL_SIZE, i * CELL_SIZE))

        screen.blit(exit_img, (exit_y * CELL_SIZE, exit_x * CELL_SIZE))

        screen.blit(player_img, (player_y * CELL_SIZE, player_x * CELL_SIZE))

        if player_x == exit_x and player_y == exit_y:
            playing = False

        pygame.display.flip()

    if running:
        show_victory_screen()
        level += 1 

pygame.quit()
