import sys
import math
import pygame as pg
from game_elements.GUI import Button
from game_elements.canvases import PlayerCanvas, ImageCanvas
from game_elements.controls import Palette, LevelSelect
from levelmanager import LevelManager

pg.init()

clock = pg.time.Clock()

SCREEN_SIZE = (800, 600)
SCREEN_W, SCREEN_H = SCREEN_SIZE[0], SCREEN_SIZE[1]
SCREEN_X_CENTER = int(SCREEN_W / 2)
SCREEN_Y_CENTER = int(SCREEN_H / 2)

DRAW_CANVAS_CELL_SIZE = 20
IMAGE_CANVAS_CELL_SIZE = 10
CANVAS_LINE = 16

SCREEN = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption("CopyArt")
icon = pg.image.load('icon.png')
pg.display.set_icon(icon)

level_manager = LevelManager('pictures')
levels = level_manager.levels

GAME_FONT = pg.font.Font('game_elements/Pixeltype.ttf', 40)

show_result_check = 0
show_result_font = None

# player's canvas
draw_canvas = PlayerCanvas(size=(DRAW_CANVAS_CELL_SIZE * CANVAS_LINE, DRAW_CANVAS_CELL_SIZE * CANVAS_LINE),
                           cell_size=DRAW_CANVAS_CELL_SIZE)
draw_canvas_pos = (SCREEN_X_CENTER - draw_canvas.width / 2, SCREEN_H - 340)
draw_canvas.set_pos(draw_canvas_pos)

# picture's canvas
image_canvas = ImageCanvas(size=(IMAGE_CANVAS_CELL_SIZE * CANVAS_LINE, IMAGE_CANVAS_CELL_SIZE * CANVAS_LINE),
                           cell_size=IMAGE_CANVAS_CELL_SIZE)
image_canvas_pos = (SCREEN_X_CENTER - image_canvas.width / 2, 50)
image_canvas.set_pos(image_canvas_pos)

image_canvas.read_image(level_manager.get_level_picture())
image_canvas.draw_from_list()

colors = image_canvas.separate_colors()

# palette
palette = Palette(size=(180, math.ceil(len(colors) / 3) * 60), color=(51, 17, 6))
palette.set_pos((25, (SCREEN_H - 65 * math.ceil(len(colors) / 3)) - 5))

finish_level_btn = Button((104, 223, 60), (143, 223, 104), size=(210, 40),
                          command=level_manager.check_level, text="Check level")
finish_level_btn.set_pos((570, SCREEN_H - 60))

level_select_win = LevelSelect(size=(180, math.ceil(len(levels) / 3) * 60), color=(51, 17, 6), levels=levels)
level_select_win.set_pos((SCREEN_W - 200, 20))


def choose_level(level):
    global color_buttons, colors, palette, show_result_check

    show_result_check = 0
    draw_canvas.clear_canvas()
    draw_canvas.draw_color = color_buttons[0].color

    level_manager.current_level = level

    image_canvas.read_image(level_manager.get_level_picture())
    image_canvas.draw_from_list()

    colors = image_canvas.separate_colors()

    palette = palette.set_size((180, math.ceil(len(colors) / 3) * 60))
    palette.set_pos((25, (SCREEN_H - 65 * math.ceil(len(colors) / 3)) - 5))

    color_buttons = palette.create(colors, change_draw_color)


def change_draw_color(color):
    draw_canvas.draw_color = color


def show_result(result):
    global show_result_check, show_result_font

    if points is not None:
        show_result_font = GAME_FONT.render(f'Your result: {result}%', False, 'White')
        show_result_check = 1


color_buttons = palette.create(colors, change_draw_color)
level_buttons = level_select_win.create(choose_level)

draw_canvas.draw_color = color_buttons[0].color
cursor_color = draw_canvas.draw_color


while True:
    mouse_pos = pg.mouse.get_pos()
    mouse_state = pg.mouse.get_pressed()

    SCREEN.fill((92, 34, 15))

    SCREEN.blit(draw_canvas, (draw_canvas.x, draw_canvas.y))
    SCREEN.blit(image_canvas, (image_canvas.x, image_canvas.y))
    SCREEN.blit(palette, palette.position)
    SCREEN.blit(level_select_win, level_select_win.position)

    SCREEN.blit(finish_level_btn, finish_level_btn.position)
    SCREEN.blit(finish_level_btn.text, (finish_level_btn.x + 20, finish_level_btn.y + 10))

    draw_canvas_frame = (draw_canvas.x - 5, draw_canvas.y - 5, draw_canvas.width + 10, draw_canvas.height + 10)
    pg.draw.rect(SCREEN, (51, 17, 6), draw_canvas_frame, 5)

    image_canvas_frame = (image_canvas.x - 5, image_canvas.y - 5, image_canvas.width + 10, image_canvas.height + 10)
    pg.draw.rect(SCREEN, (51, 17, 6), image_canvas_frame, 5)

    # finish level button logic
    finish_level_btn.fill(finish_level_btn.color)
    finish_level_btn_state = finish_level_btn.check_mouse(mouse_pos, mouse_state[0])

    if finish_level_btn_state['hover']:
        finish_level_btn.fill(finish_level_btn.hover_color)

        if finish_level_btn_state['click']:
            points = finish_level_btn.click(draw_canvas, image_canvas)

            show_result(points)

    # show result
    if show_result_check:
        SCREEN.blit(show_result_font, (570, 510))

    # draw canvas logic
    draw_canvas_state = draw_canvas.check_mouse(mouse_pos, mouse_state[0])
    if draw_canvas_state['hover']:
        # cursor
        cursor_pos = (mouse_pos[0] // DRAW_CANVAS_CELL_SIZE * DRAW_CANVAS_CELL_SIZE,
                      mouse_pos[1] // DRAW_CANVAS_CELL_SIZE * DRAW_CANVAS_CELL_SIZE)
        pg.draw.rect(SCREEN, cursor_color, (*cursor_pos, DRAW_CANVAS_CELL_SIZE, DRAW_CANVAS_CELL_SIZE))

        if draw_canvas_state['click']:
            draw_canvas.draw_cell()

    # color_buttons blit and handling input
    for color_button in color_buttons:
        SCREEN.blit(color_button, color_button.position)
        color_button.fill(color_button.color)
        color_button_state = color_button.check_mouse(mouse_pos, mouse_state[0])

        if color_button_state['hover']:
            color_button.fill(color_button.hover_color)

            if color_button_state['click']:
                cursor_color = color_button.color
                color_button.click(color_button.color)

    # level_buttons blit
    for level_n, level_button in enumerate(level_buttons):
        SCREEN.blit(level_button, level_button.position)
        SCREEN.blit(level_button.text, (level_button.x + 5, level_button.y + 15))
        level_button_state = level_button.check_mouse(mouse_pos, mouse_state[0])

        level_button.fill(level_button.color)

        if level_button_state['hover']:
            level_button.fill(level_button.hover_color)

            if level_button_state['click']:
                cursor_color = level_button.color
                level_button.click(level_n)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    clock.tick(60)
    pg.display.update()
