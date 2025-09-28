import pygame
import sys
import random

# 初始化 Pygame
pygame.init()
pygame.mixer.init()

# 螢幕設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("貪食蛇")

# 載入音訊檔案
try:
    pygame.mixer.music.load('background_music.mp3')
    eat_sound = pygame.mixer.Sound('eat_sound.wav')
except pygame.error as e:
    print(f"Cannot load sound files: {e}")
    eat_sound = None

# 顏色
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# 字型設定
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, white)
    screen.blit(value, [0, 0])

def Your_level(level):
    value = score_font.render("Level: " + str(level), True, white)
    screen.blit(value, [screen_width - 120, 0])

def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, green, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [screen_width / 6, screen_height / 3])

def gameLoop():
    game_over = False
    game_close = False

    # 蛇的初始設定
    snake_x = screen_width / 2
    snake_y = screen_height / 2
    snake_x_change = 0
    snake_y_change = 0
    snake_list = []
    length_of_snake = 1
    score = 0
    level = 1
    snake_speed = 15

    # 食物的初始設定
    food_x = round(random.randrange(0, screen_width - snake_block) / 20.0) * 20.0
    food_y = round(random.randrange(0, screen_height - snake_block) / 20.0) * 20.0

    if pygame.mixer.music.get_init():
        pygame.mixer.music.play(-1)

    while not game_over:

        while game_close == True:
            screen.fill(black)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            Your_score(score)
            Your_level(level)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake_x_change = -snake_block
                    snake_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    snake_x_change = snake_block
                    snake_y_change = 0
                elif event.key == pygame.K_UP:
                    snake_y_change = -snake_block
                    snake_x_change = 0
                elif event.key == pygame.K_DOWN:
                    snake_y_change = snake_block
                    snake_x_change = 0

        if snake_x >= screen_width or snake_x < 0 or snake_y >= screen_height or snake_y < 0:
            game_close = True
        
        snake_x += snake_x_change
        snake_y += snake_y_change
        screen.fill(black)
        pygame.draw.rect(screen, red, [food_x, food_y, snake_block, snake_block])
        
        snake_head = []
        snake_head.append(snake_x)
        snake_head.append(snake_y)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        draw_snake(snake_block, snake_list)
        Your_score(score)
        Your_level(level)

        pygame.display.update()

        if snake_x == food_x and snake_y == food_y:
            if eat_sound:
                eat_sound.play()
            food_x = round(random.randrange(0, screen_width - snake_block) / 20.0) * 20.0
            food_y = round(random.randrange(0, screen_height - snake_block) / 20.0) * 20.0
            length_of_snake += 1
            score += 10
            if score % 50 == 0:
                level += 1
                snake_speed += 2


        clock.tick(snake_speed)

    pygame.quit()
    sys.exit()

gameLoop()
