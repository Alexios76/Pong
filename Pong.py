import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE = 20
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Initialize paddles and ball
left_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Initial ball speed
ball_speed = [5, 5]

# Initial score
score = 0
high_score = 0

# Load high score from file
try:
    with open("high_score.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    pass

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save high score to file before quitting
            with open("high_score.txt", "w") as file:
                file.write(str(high_score))
            pygame.quit()
            sys.exit()

    # Move the left paddle with the mouse
    left_paddle.y = pygame.mouse.get_pos()[1] - PADDLE_HEIGHT // 2

    # Move the right paddle to follow the ball
    if ball.centery < right_paddle.centery:
        right_paddle.y -= 5
    elif ball.centery > right_paddle.centery:
        right_paddle.y += 5

    # Update ball position
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Ball collision with top and bottom walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed[1] = -ball_speed[1]

    # Ball collision with paddles
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed[0] = -ball_speed[0]
        # Adjust ball direction based on where it hits the paddle
        if ball.centery > left_paddle.centery + PADDLE_HEIGHT // 2:
            ball_speed[1] = abs(ball_speed[1])
        elif ball.centery < left_paddle.centery - PADDLE_HEIGHT // 2:
            ball_speed[1] = -abs(ball_speed[1])

    if ball.colliderect(left_paddle):
        score += 1
        ball_speed[0] += 1

    # Ball goes past the left paddle
    if ball.left <= 0:
        ball_speed = [5, 5]  # Reset ball speed
        if score > high_score:
            high_score = score
        score = 0  # Increment score
        ball.x = WIDTH // 2 - BALL_SIZE // 2
        ball.y = HEIGHT // 2 - BALL_SIZE // 2

    # Ball goes past the right paddle
    if ball.right >= WIDTH:
        ball_speed = [5, 5]  # Reset ball speed
        ball.x = WIDTH // 2 - BALL_SIZE // 2
        ball.y = HEIGHT // 2 - BALL_SIZE // 2

    # Draw everything on the screen
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))  # Center line
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(high_score_text, (10, 50))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
