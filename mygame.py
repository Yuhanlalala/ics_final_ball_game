import pygame as pg
import pygame.mixer
import sys
import random
import time

# pygame.mixer.music.load("background_music.mp3")

# pygame.mixer.music.play()
pg.mixer.init()
pg.mixer.pre_init(44100,16,2,4096)
pick_sound = pg.mixer.Sound('Glass_and_Metal_Collision.wav')

pg.init()

pg.mixer.music.load('Dark_Tranquility.mp3')
pg.mixer.music.set_volume(0.5)
pg.mixer.music.play(-1)
# pg.mixer.Sound('background_music.mp3').play()
game_window = pg.display.set_mode((600, 500))
pg.display.set_caption('pick up the ball !!')
window_color = (230,230,250)
ball_color = (131,139,131)
rect_color = (0, 0, 0)
score = 0
font = pg.font.Font(None, 60) #（字体，大小）
font1 = pg.font.Font(None, 30)
ball_x = random.randint(20, 580)
ball_y = 20
move_x = 3
move_y = 3
point = 1
count = 0
name = 'your score:\n'

# pg.mixer.Sound.play(pick_sound)
run = True
while run:
    game_window.fill(window_color)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            sys.exit()
    mouse_x, mouse_y = pg.mouse.get_pos() #return the position of the mouse
    pg.draw.circle(game_window, ball_color, (ball_x, ball_y), 18)
    pg.draw.rect(game_window, rect_color,(mouse_x, 490, 100, 10)) #定位在左上角
    my_text = font.render(str(score), True, (160,82,45))
    game_window.blit(my_text, (490, 50)) #文字位置的横纵坐标
    my_text1 = font1.render(name, True, (160,82,45))
    game_window.blit(my_text1, (460, 20))
    ball_x += move_x
    ball_y += move_y
    if ball_x <= 20 or ball_x >= 580:
        move_x = -move_x
    if ball_y <= 20:
        move_y = -move_y
    elif mouse_x - 20 < ball_x < mouse_x + 120 and ball_y >= 470:
        # pg.mixer.music.load('Glass_and_Metal_Collision.mp3')
        # pg.mixer.music.play(1)
        pick_sound.play()
        pg.mixer.music.play()
        time.sleep(0.001)
        move_y = -move_y
        score += point
        count += 1
        if count == 2:
            count = 0
            point += point
            if move_x > 0:
                move_x += 1
            else:
                move_x -= 1
            move_y -= 1
    elif ball_y >= 480 and (ball_x <= mouse_x - 20 or ball_x >= mouse_x + 120):
        break
    pg.display.update() #keep update,不会一闪而过
    time.sleep(0.001) #每隔0.005s循环一次
