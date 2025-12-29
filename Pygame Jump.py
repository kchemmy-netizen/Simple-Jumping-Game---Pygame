import pygame
import os

# ------------------
# Initialization
# ------------------
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chemmy's Pygame Jump")

clock = pygame.time.Clock()
FPS = 60

font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 64)

# -----------------
# Background
# -----------------
background = pygame.image.load("background.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# -----------------
# Colors
# -----------------
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
RED = (255, 80, 80)
GREEN = (0, 255, 0)

# -----------------
# Constants
# -----------------
ground_y = HEIGHT - 50
GRAVITY = 0.8
JUMP_POWER = -15
OBSTACLE_SPEED = 6
SPAWN_TIME = 1500  # ms

HIGHSCORE_FILE = "highscore.txt"

# -----------------
# High score
# -----------------
def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read())
    return 0

def save_highscore(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

high_score = load_highscore()

# -----------------
# Reset game
# -----------------
def reset_game():
    global player, player_vel_y, on_ground
    global obstacles, score, game_over, last_spawn

    player = pygame.Rect(100, ground_y - 50, 50, 50)
    player_vel_y = 0
    on_ground = True

    obstacles = []
    score = 0
    last_spawn = pygame.time.get_ticks()
    game_over = False

reset_game()

# -----------------
# Main loop
# -----------------
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and on_ground:
                    player_vel_y = JUMP_POWER
                    on_ground = False
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()

    # ----------------
    # Update
    # ----------------
    if not game_over:
        player_vel_y += GRAVITY
        player.y += player_vel_y

        if player.bottom >= ground_y:
            player.bottom = ground_y
            player_vel_y = 0
            on_ground = True

        now = pygame.time.get_ticks()
        if now - last_spawn > SPAWN_TIME:
            obstacles.append(pygame.Rect(WIDTH, ground_y - 50, 50, 50))
            last_spawn = now

        for obstacle in obstacles[:]:
            obstacle.x -= OBSTACLE_SPEED

            if obstacle.right < player.left:
                score += 1
                obstacles.remove(obstacle)

            if player.colliderect(obstacle):
                game_over = True
                if score > high_score:
                    high_score = score
                    save_highscore(high_score)

    # ----------------
    # Drawing
    # ----------------
    screen.blit(background, (0, 0))

    pygame.draw.rect(screen, GREEN, (0, ground_y, WIDTH, 50))
    pygame.draw.rect(screen, BLUE, player)

    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, obstacle)

    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    screen.blit(font.render(f"High Score: {high_score}", True, WHITE), (10, 40))

    if game_over:
        screen.blit(
            big_font.render("GAME OVER", True, WHITE),
            (WIDTH // 2 - 150, HEIGHT // 2 - 50)
        )
        screen.blit(
            font.render("Press R to restart", True, WHITE),
            (WIDTH // 2 - 120, HEIGHT // 2 + 10)
        )

    pygame.display.update()

pygame.quit()
