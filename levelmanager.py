import os


class LevelManager:
    def __init__(self, path):
        self.levels = [f'{path}/{picture}' for picture in os.listdir(path)]
        self.current_level = 0

    def get_level_picture(self):
        return self.levels[self.current_level]

    @staticmethod
    def check_level(draw_canvas, image_canvas) -> int:
        total_pixels = draw_canvas.total_cells
        right_pixels = 0

        draw_canvas_list = draw_canvas.list
        image_canvas_list = image_canvas.list

        for line in range(len(draw_canvas_list)):
            for color in range(len(draw_canvas_list[line])):
                if draw_canvas_list[line][color] == tuple(image_canvas_list[line][color]):
                    right_pixels += 1

        return int(right_pixels / total_pixels * 100)
