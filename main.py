import pygame
import sys
# import time
# import math
import random

# управление на стполочки
# A - пошаговое обновление
# S - убрать режим ртмования(игрок стоновится нивидимым)
# D - debug_mode (вроде бы кастрировал эту функцию)
# SPACE - непрерывное обновление

# Это можно менять!
draw_net = False

game_max_fps = 60

print("Default state (Game of life): 2433")
rule_bs = [int(input("If neighbor >= x then remove; x = ")),
           int(input("If neighbor < y then remove; y = ")),
           int(input("If neighbor == [z1; z2] burth; from z1 = ")),
           int(input("If neighbor == [z1; z2] burth; to z2 = "))]

box_color = (48, 98, 48)
net_color = (15, 56, 15)
text_color = (155, 188, 15)

main_step = []
second_step_append = []
second_step_remove = []

player_xy = [0, 0]
player_move = False
p_draw = False
player_shit = []

clear_bord = False

debug_mode = False
play = False
color_deb = [100, 200, 200]

r = 15
g = 40
b = 40


def color_cy_r():
    global r
    if r <= 250:
        r += 1
    else:
        r = 0
    return r


pygame.init()

bx_delta = 0
sc_delta = 0
screen_ch = False

screen_x = 1500  # ширина экрана
screen_y = 1000  # длина экрана
box_len_x = 20  # ширина пикселя
box_len_y = 20  # длина пикселя

box_quantity_x = screen_x // box_len_x
box_quantity_y = screen_y // box_len_y
text_size = (screen_y * screen_x) // (1600 * 20) + 1

screen = pygame.display.set_mode((screen_x, screen_y))


def net_draw():
    if draw_net:
        if box_quantity_x <= screen_x / 5 and box_quantity_y <= screen_y / 5:
            netx = 0
            nety = 0
            while netx <= box_quantity_x:
                pygame.draw.line(screen, net_color, [box_len_x * netx, 0],
                                 [box_len_x * netx, screen_y], 1)
                netx += 1
            while nety <= box_quantity_y:
                pygame.draw.line(screen, net_color, [0, box_len_y * nety],
                                 [screen_x, box_len_x * nety], 1)
                nety += 1


def player(xy: tuple, draw_mode):
    if box_quantity_x > xy[0] - 1 > 0 \
            and box_quantity_y > xy[1] - 1 > 0:
        if draw_mode:
            color = (150, 0, 0)
            pygame.draw.rect(screen, color,
                             (box_len_x * xy[0] - 1,  # x
                              box_len_y * xy[1] - 1,  # y
                              box_len_x + 2,
                              box_len_y + 2), 0)
            player_shit.append(xy)
        else:
            color = (200, 200, 200)
            pygame.draw.rect(screen, color,
                             (box_len_x * xy[0],  # x
                              box_len_y * xy[1],  # y
                              box_len_x,
                              box_len_y), 0)
            if xy in main_step and xy not in second_step_append:
                return
            second_step_append.append(xy)


def player_remove_box(remove_xy: tuple):
    pygame.draw.rect(screen, (0, 0, 0),
                     (box_len_x * remove_xy[0],  # x
                      box_len_y * remove_xy[1],  # y
                      box_len_x, box_len_y), 0)


def game_close(pyevent):
    if pyevent.type == pygame.QUIT:
        pygame.quit()
        sys.exit()


# Box neighbor check
def b_nb_check(b_cords):
    box_nb = 0
    b_cords1 = b_cords[0] - 1
    b_cords2 = b_cords[0] + 1
    b_cords3 = b_cords[1] - 1
    b_cords4 = b_cords[1] + 1
    if b_cords in main_step:
        box_nb += 1
    if (b_cords1, b_cords3) in main_step:
        box_nb += 1
    if (b_cords1, b_cords[1]) in main_step:
        box_nb += 1
    if (b_cords1, b_cords4) in main_step:
        box_nb += 1
    if (b_cords[0], b_cords4) in main_step:
        box_nb += 1
    if (b_cords[0], b_cords3) in main_step:
        box_nb += 1
    if (b_cords2, b_cords3) in main_step:
        box_nb += 1
    if (b_cords2, b_cords[1]) in main_step:
        box_nb += 1
    if (b_cords2, b_cords4) in main_step:
        box_nb += 1
    return box_nb


def draw_box(draw_xy: tuple):
    if box_quantity_x > draw_xy[0] >= 0 \
            and box_quantity_y > draw_xy[1] >= 0:
        if debug_mode:
            pygame.draw.rect(screen,
                             color_deb,
                             (box_len_x * draw_xy[0] + 1,  # x
                              box_len_y * draw_xy[1] + 1,  # y
                              box_len_x - 1,
                              box_len_y - 1), 0)
        else:
            pygame.draw.rect(screen, box_color,
                             (box_len_x * draw_xy[0] + 1,  # x
                              box_len_y * draw_xy[1] + 1,  # y
                              box_len_x - 1,
                              box_len_y - 1), 0)
        if draw_xy in main_step and draw_xy not in second_step_append:
            return
        second_step_append.append(draw_xy)


def draw_box_refresh(draw_xy):
    pygame.draw.rect(screen, box_color,
                     (box_len_x * draw_xy[0] + 1,  # x
                      box_len_y * draw_xy[1] + 1,  # y
                      box_len_x - 1,
                      box_len_y - 1), 0)


def remove_box(remove_xy: tuple):
    if remove_xy in main_step:
        pygame.draw.rect(screen, (0, 0, 0),
                         (box_len_x * remove_xy[0] + 1,  # x
                          box_len_y * remove_xy[1] + 1,  # y
                          box_len_x - 1,
                          box_len_y - 1), 0)

        second_step_remove.append(remove_xy)


def next_step():
    z = 0
    x = -1
    y = -1
    select_box_c = []
    main_len = len(main_step)
    while z < main_len:
        box_main = main_step[z]
        while x <= 1:
            while y <= 1:
                selected_box = (box_main[0] + x, box_main[1] + y)
                if selected_box not in select_box_c:
                    select_box_c.append(selected_box)
                    b_nbrs = b_nb_check(selected_box)

                    if b_nbrs <= rule_bs[0]:  # 2
                        remove_box(selected_box)
                    elif b_nbrs > rule_bs[1]:  # 4
                        remove_box(selected_box)  # 3
                    elif rule_bs[2] <= b_nbrs <= rule_bs[3] and selected_box not in main_step:
                        draw_box(selected_box)
                y += 1
            y = -1
            x += 1
        y = -1
        x = -1
        z += 1


def text_box_update():
    pygame.draw.rect(screen, (15, 56, 15),
                     (0,  # x
                      0,  # y
                      text_size * 3,
                      text_size * 3.2), 0)


def random_fill():
    x = 0
    y = 0
    while y <= box_quantity_y:
        while x <= box_quantity_x:
            if random.randint(0, 1) == 1:
                draw_box((x, y))
            x += 1
        x = 0
        y += 1


net_draw()

my_font = pygame.font.SysFont('Comic Sans MS', text_size)
text_surface = my_font.render('Pause', False, text_color)

text_box_update()
clock = pygame.time.Clock()

remove_min = True
remove_max = True

if rule_bs[0] <= 0:
    remove_min = False
if rule_bs[1] >= 9:
    remove_max = False


while True:
    clock.tick(game_max_fps)
    clock.tick()
    text_box_update()

    screen.blit(my_font.render(str(int(clock.get_fps())), 1, text_color), (0, text_size))
    screen.blit(my_font.render(str(len(main_step)), 1, text_color), (0, text_size * 2))
    for event in pygame.event.get():
        game_close(event)
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                screen_ch = True
                bx_delta = -1
            if event.y < 0:
                screen_ch = True
                bx_delta = +1
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                player_xy[0] -= 1
                player_move = True
            elif event.key == pygame.K_RIGHT:
                player_xy[0] += 1
                player_move = True
            elif event.key == pygame.K_UP:
                player_xy[1] -= 1
                player_move = True
            elif event.key == pygame.K_DOWN:
                player_xy[1] += 1
                player_move = True

            elif event.key == pygame.K_SPACE:

                if play:
                    play = False
                    text_box_update()
                    text_surface = my_font.render('Pause', False, text_color)
                else:
                    play = True
                    text_box_update()
                    text_surface = my_font.render('Play', False, text_color)

            elif event.key == pygame.K_a:
                if p_draw:
                    p_draw = False
                else:
                    p_draw = True
            elif event.key == pygame.K_d:
                if debug_mode:
                    debug_mode = False
                else:
                    debug_mode = True
            elif event.key == pygame.K_s:
                if not play:
                    next_step()
            elif event.key == pygame.K_e:
                screen_ch = True
                sc_delta = +100
            elif event.key == pygame.K_q:
                screen_ch = True
                sc_delta = -100
            elif event.key == pygame.K_f:
                random_fill()
            elif event.key == pygame.K_c:
                clear_bord = True
            if player_move:
                player((player_xy[0], player_xy[1]), p_draw)
                player_move = False

            if event.key == pygame.K_w:
                mouse_xy = pygame.mouse.get_pos()
                if not (mouse_xy[0] // box_len_x, mouse_xy[1] // box_len_y) in main_step:
                    draw_box((mouse_xy[0] // box_len_x,
                              mouse_xy[1] // box_len_y))
                else:
                    remove_box((mouse_xy[0] // box_len_x,
                                mouse_xy[1] // box_len_y))

    screen.blit(text_surface, (0, 0))

    if play:
        next_step()
        color_deb[0], color_deb[1], color_deb[2] = color_cy_r(), g, b

        # next_step()
        # color_deb[0], color_deb[1], color_deb[2] = \
        #    random.randint(0, 255), \
        #        random.randint(0, 255), \
        #        random.randint(0, 255)
    if not remove_max and not remove_min:
        pref = len(second_step_append)
    while not second_step_append == []:
        main_step.append(second_step_append[0])
        second_step_append.remove(second_step_append[0])
    while not second_step_remove == []:

        main_step.remove(second_step_remove[0])
        second_step_remove.remove(second_step_remove[0])

    while not player_shit == []:
        player_remove_box(player_shit[0])
        player_shit.remove(player_shit[0])

    if not remove_max and not remove_min and len(main_step) > 0:
        while len(main_step) >= 600:
            ra = 400
            while ra > 0:
                main_step.remove(main_step[0])
                ra -= 1

    if screen_ch:
        if screen_x + sc_delta > 300 and screen_y + sc_delta > 300:
            screen_x += sc_delta
            screen_y += sc_delta
        sc_delta = 0
        if box_len_y + bx_delta > 1 and box_len_x + bx_delta > 1:
            box_len_x += bx_delta
            box_len_y += bx_delta
        bx_delta = 0

        box_quantity_x = screen_x // box_len_x
        box_quantity_y = screen_y // box_len_y
        text_size = (screen_y * screen_x) // (1600 * 20) + 1
        screen = pygame.display.set_mode((screen_x, screen_y))
        my_font = pygame.font.SysFont('Comic Sans MS', text_size)
        text_surface = my_font.render('Pause', False, text_color)
        net_draw()
        screen_ch = False
        refresh_step = main_step.copy()
        while refresh_step:
            draw_box_refresh(refresh_step[0])
            refresh_step.remove(refresh_step[0])
    if clear_bord:
        while main_step:
            remove_box(main_step[0])
            main_step.remove(second_step_remove[0])
            second_step_remove.clear()
        clear_bord = False

    pygame.display.flip()
