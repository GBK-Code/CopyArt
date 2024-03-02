from game_elements.GUI import GameObject, InteractedObject
from pygame import draw
import cv2


class Canvas(GameObject):
    def __init__(self, size, cell_size=20):
        super().__init__(size)

        self.cells_in_line = self.width // cell_size
        self.cell_size = cell_size
        self.total_cells = self.cells_in_line ** 2
        self.cell_x, self.cell_y = (0, 0)

        self.list = [[(255, 255, 255) for _ in range(self.cells_in_line)] for _ in range(self.cells_in_line)]

        self.draw_color = (0, 0, 0)
        self.fill((255, 255, 255))

    def draw_cell(self) -> None:
        draw_x = self.cell_x * self.cell_size
        draw_y = self.cell_y * self.cell_size
        draw.rect(self, self.draw_color, (draw_x, draw_y, self.cell_size, self.cell_size))

        self.list[self.cell_y][self.cell_x] = self.draw_color

    def draw_from_list(self):
        for cell_y in range(len(self.list)):
            for cell_x in range(len(self.list[cell_y])):
                self.cell_x = cell_x
                self.cell_y = cell_y
                self.draw_color = tuple(self.list[cell_y][cell_x])
                self.draw_cell()

    def clear_canvas(self):
        self.list = [[(255, 255, 255) for _ in range(self.cells_in_line)] for _ in range(self.cells_in_line)]
        self.draw_from_list()


class PlayerCanvas(Canvas, InteractedObject):
    def __init__(self, size, cell_size=20):
        super().__init__(size, cell_size)

    def mouse_moved(self, mouse_pos) -> None:
        self.mouse_x = int(mouse_pos[0] - self.x)
        self.mouse_y = int(mouse_pos[1] - self.y)
        self.cell_x = self.mouse_x // self.cell_size
        self.cell_y = self.mouse_y // self.cell_size


class ImageCanvas(Canvas):
    def __init__(self, size, cell_size=20):
        super().__init__(size, cell_size)

        self.unique_colors = []

    def read_image(self, image_path) -> None:
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.list = image

    def separate_colors(self) -> list:
        self.unique_colors = []

        for line in range(len(self.list)):
            for color in range(len(self.list[line])):
                add_color = tuple(self.list[line][color])

                if add_color not in self.unique_colors:
                    self.unique_colors.append(add_color)

        return self.unique_colors
