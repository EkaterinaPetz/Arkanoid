import pygame
import random

width = 700
height = 500
r_ball = 40
platform_width = 100
platform_height = 20
platform_move = 10
bg_color = (205, 205, 255)
black = (0, 0, 0)
ball_color = black
block_color = (50, 50, 150)
bonus_color = (100, 160, 40)
live_bonus_color = (255, 130, 15)
speed_bonus_color = (255, 60, 255)
fine_color = (200, 0, 0)
block_width = 80
block_height = 20
lives = 5
ball_speed = 4


# pygame.display.set_caption("Всплывающее окно")

def show_popup(text, color):
    # Создаем поверхность для окна
    popup_width = 400
    popup_height = 200
    popup_surface = pygame.Surface((popup_width, popup_height))
    popup_surface.fill((255, 255, 255))

    # Рендерим текст
    font2 = pygame.font.Font(None, 72)
    text_surface = font2.render(text, True, color)
    text_rect = text_surface.get_rect(center=(popup_width // 2, popup_height // 2))

    # Рисуем на поверхности
    popup_surface.blit(text_surface, text_rect)

    # Рисуем окно на экране
    popup_rect = popup_surface.get_rect(center=(width // 2, height // 2))
    screen.blit(popup_surface, popup_rect)
    pygame.display.flip()

    # Ожидаем, пока пользователь не закроет окно
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


# Шарик движение
ball_move_x = ball_speed * random.choice([-1, 1])
ball_move_y = ball_speed * random.choice([-1, 1])

is_paused = False
bonus_flag = False
live_bonus_flag = False
fine_flag = False
speed_bonus_flag = False
flash_time = 0  # начало паузы
bonus_time = 0  # начало работы бонуса 1
bonus_time2 = 0 # начало работы бонуса 2

# создаём объекты по размерам
ball = pygame.Rect(width // 2 - r_ball, height // 2 - r_ball, r_ball, r_ball)
platform = pygame.Rect(width // 2 - platform_width, height - platform_height - 30, platform_width, platform_height)
bonus = pygame.Rect(width // 2 - 20, height // 2 - 20, r_ball - 10, r_ball - 10)
live_bonus = pygame.Rect(width // 2 - 20, height // 2 - 20, r_ball - 10, r_ball - 10)
speed_bonus = pygame.Rect(width // 2 - 20, height // 2 - 20, r_ball - 10, r_ball - 10)
fine = pygame.Rect(width // 2 - 20, height // 2 - 20, r_ball - 10, r_ball - 10)
# массив объектов(блоков)
blocks = [pygame.Rect(x, y, block_width, block_height) for x in range(0, width, block_width + 10) for y in
          range(40, (block_height + 5) * 4 + 40, block_height + 5)]

# Кнопка
button_width = 200
button_height = 50
button_x = width // 2 - button_width // 2
button_y = height // 2 - button_height // 2
button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()  # создание объекта часов чтобы отслеживать время

done = False
while not done:
    for event in pygame.event.get():
        if pygame.QUIT == event.type:
            done = True

    if not is_paused:
        # Управление платформой
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            platform.x -= platform_move
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            platform.x += platform_move

        # Ограничение перемещения платформы
        platform.x = max(0, min(platform.x, width - platform_width))

        # Обновление положения шарика
        ball.x += ball_move_x
        ball.y += ball_move_y

        # Проверка столкновения с платформой
        if ball.colliderect(platform):
            ball_move_y = -ball_move_y

        # проверка столкновения с блоками
        for i in range(len(blocks)):
            if ball.colliderect(blocks[i]):
                blocks.pop(i)
                ball_move_y = -ball_move_y
                # бонусы и штрафы
                if random.randint(1,10) == 1 and platform.width != 200 and not live_bonus_flag and not fine_flag and not bonus_flag and not speed_bonus_flag:
                    bonus_flag = True
                elif random.randint(1,10) == 1 and not live_bonus_flag and not fine_flag and not bonus_flag and not speed_bonus_flag:
                    live_bonus_flag = True
                elif random.randint(1,10) == 1 and not fine_flag and not live_bonus_flag and not bonus_flag and not speed_bonus_flag:
                    fine_flag = True
                elif random.randint(1,10) == 1 and not ball_speed == 2 and not speed_bonus_flag and not live_bonus_flag and not bonus_flag and not fine_flag:
                    speed_bonus_flag = True
                break

        # Проверка на отскок от границ экрана и проигрыш
        if ball.x <= r_ball or ball.x >= width - r_ball:
            ball_move_x = -ball_move_x
        if ball.y <= r_ball:
            ball_move_y = -ball_move_y
        if ball.y >= height - r_ball:
            lives -= 1
            ball_speed += 0.5
            ball.x = width // 2 - 20  # начало с центра экрана
            ball.y = height // 2 - 20
            ball_move_x = ball_speed * random.choice([-1, 1])
            ball_move_y = ball_speed * random.choice([-1, 1])
            is_paused = True  # начало паузы
            flash_time = pygame.time.get_ticks()  # время начала мигания

        # проверка бонуса
        if pygame.time.get_ticks() - bonus_time > 10000 and platform.width == 200:
            platform.width = 100
        if pygame.time.get_ticks() - bonus_time2 > 10000 and ball_speed == 2:
            ball_speed = 4

        if bonus_flag:  # если есть бонус
            if bonus.colliderect(platform):
                platform.width = 200
                bonus_time = pygame.time.get_ticks()
                bonus.y = height // 2
                bonus_flag = False
            elif bonus.y > height:
                bonus_flag = False
                bonus.y = height // 2
            else:
                bonus.y += 4

        if live_bonus_flag:  # если есть бонус жизни
            if live_bonus.colliderect(platform):
                lives += 1
                if ball_speed > 4:
                    ball_speed -= 0.5  # замедляем шарик
                live_bonus_flag = False
            elif live_bonus.y > height:
                live_bonus_flag = False
                live_bonus.y = height // 2
            else:
                live_bonus.y += 4

        if speed_bonus_flag:
            if speed_bonus.colliderect(platform):
                ball_speed = 2
                bonus_time2 = pygame.time.get_ticks()
                speed_bonus.y = height // 2
                speed_bonus_flag = False
            elif speed_bonus.y > height:
                speed_bonus_flag = False
                speed_bonus.y = height // 2
            else:
                speed_bonus.y += 4

        if fine_flag:  # если есть штраф
            if fine.colliderect(platform):
                lives -= 1
                fine.y = height // 2
                fine_flag = False
            elif fine.y > height:
                fine_flag = False
                fine.y = height // 2
            else:
                fine.y += 4




    else:
        current_time = pygame.time.get_ticks()
        if current_time - flash_time < 1000:  # пауза 1000 милисекунд
            if ((current_time - flash_time) // 100) % 2 == 0:  # мигание каждые 100 милисекунды
                ball_color = bg_color
            else:
                ball_color = black
        else:
            is_paused = False

    # Отрисовка
    screen.fill(bg_color)

    for block in blocks:
        pygame.draw.rect(screen, block_color, block)

    font1 = pygame.font.Font(None, 36)
    text1 = font1.render('LIVES:' + str(lives), 1, (0, 0, 0))

    screen.blit(text1, (10, 10))

    pygame.draw.ellipse(screen, ball_color, ball)
    pygame.draw.rect(screen, black, platform)
    if bonus_flag:
        pygame.draw.ellipse(screen, bonus_color, bonus)

    if live_bonus_flag:
        pygame.draw.ellipse(screen, live_bonus_color, live_bonus)

    if fine_flag:
        pygame.draw.ellipse(screen, fine_color, fine)

    if speed_bonus_flag:
        pygame.draw.ellipse(screen, speed_bonus_color, speed_bonus)

    if lives == 0:
        show_popup("You lose!", fine_color)
        # окно проигрыш

    if len(blocks) == 0:
        show_popup("You win!", bonus_color)
        # окно выигрыш


    pygame.display.flip()  # Обновляем экран
    clock.tick(60)  # ограничение

pygame.quit()