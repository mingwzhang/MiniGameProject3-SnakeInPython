import pygame
import random

pygame.init()

w_width = 640
w_height = 480

window = pygame.display.set_mode((w_width, w_height))

food_size = 10

snake_size = 10
initial_snake_speed = 6
snake_speed = initial_snake_speed

snake_x = w_width // 2
snake_y = w_height // 2

direction = None

snake_length = 1
snake_body = [(snake_x, snake_y)]

food_x = random.randint(0, w_width - food_size)
food_y = random.randint(0, w_height - food_size)

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)

score = 0
game_over = False
game_started = False

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 36)
title_font = pygame.font.SysFont(None, 48)

def show_score():
    score_text = font.render("Score: " + str(score), True, white)
    window.blit(score_text, (10, 10))

def show_game_over():
    game_over_text = font.render("Game Over! Press R to restart", True, white)
    text_rect = game_over_text.get_rect(center=(w_width // 2, w_height // 2))
    window.blit(game_over_text, text_rect)

def restart_game():
    global snake_x, snake_y, direction, snake_length, snake_body, food_x, food_y, score, game_over, game_started, snake_speed
    snake_x = w_width // 2
    snake_y = w_height // 2
    direction = None
    snake_length = 1
    snake_body = [(snake_x, snake_y)]
    food_x = random.randint(0, w_width - food_size)
    food_y = random.randint(0, w_height - food_size)
    score = 0
    game_over = False
    game_started = False
    snake_speed = initial_snake_speed

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game_started:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
                    game_started = True
            elif not game_over:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if direction != "DOWN":
                        direction = "UP"
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if direction != "UP":
                        direction = "DOWN"
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if direction != "RIGHT":
                        direction = "LEFT"
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if direction != "LEFT":
                        direction = "RIGHT"
            elif game_over:
                if event.key == pygame.K_r:
                    restart_game()

    if game_started and not game_over:
        if direction == "UP":
            snake_y -= snake_speed
        elif direction == "DOWN":
            snake_y += snake_speed
        elif direction == "LEFT":
            snake_x -= snake_speed
        elif direction == "RIGHT":
            snake_x += snake_speed

        if snake_x < 0:
            snake_x = w_width - snake_size
        elif snake_x >= w_width:
            snake_x = 0
        elif snake_y < 0:
            snake_y = w_height - snake_size
        elif snake_y >= w_height:
            snake_y = 0

        # Check for collision with food
        if snake_x < food_x + food_size and snake_x + snake_size > food_x and \
                snake_y < food_y + food_size and snake_y + snake_size > food_y:
            snake_length += 1
            food_x = random.randint(0, w_width - food_size)
            food_y = random.randint(0, w_height - food_size)
            score += 1
            snake_speed += 0.5

        snake_body.append((snake_x, snake_y))

        if len(snake_body) > snake_length:
            del snake_body[0]

        # Check for collision with tail
        if any(body_part == (snake_x, snake_y) for body_part in snake_body[:-1]):
            game_over = True

    window.fill(black)

    if game_started:
        pygame.draw.rect(window, white, (food_x, food_y, food_size, food_size))

        for body_part in snake_body:
            pygame.draw.rect(window, green, (body_part[0], body_part[1], snake_size, snake_size))

        show_score()

        if game_over:
            show_game_over()
    else:
        title_text = title_font.render("SNAKE", True, white)
        title_rect = title_text.get_rect(center=(w_width // 2, w_height // 2 - 50))
        window.blit(title_text, title_rect)

        credit_text = font.render("Made by Mingwei", True, white)
        credit_rect = credit_text.get_rect(center=(w_width // 2, w_height // 2 + 50))
        window.blit(credit_text, credit_rect)

        start_text = font.render("Press Any Movement Key (WASD) to Start", True, white)
        start_rect = start_text.get_rect(center=(w_width // 2, w_height // 2 + 100))
        window.blit(start_text, start_rect)

    pygame.display.update()

    clock.tick(10)

pygame.quit()
