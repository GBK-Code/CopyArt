from game_elements.GUI import GameObject, Button
from game_elements.layouts import GridLayout
from math import ceil


class Palette(GameObject):
    def __init__(self, size, color):
        super().__init__(size)
        self.color = color
        self.size = size

        self.fill(self.color)

        self.colors = []

    def create(self, colors, command=None):
        color_buttons = []
        for i in range(len(colors)):
            color_button = Button(color=colors[i],
                                  hover_color=(colors[i][0] + 20, colors[i][1] + 20, colors[i][2] + 20),
                                  size=(50, 50), command=command)
            color_buttons.append(color_button)

        grid = GridLayout(3, ceil(len(color_buttons) / 3), 10)
        grid.set_pos((5, 5))
        layout = grid.create(color_buttons)

        for i, color_button in enumerate(color_buttons):
            color_button.x = layout[i][0]
            color_button.y = layout[i][1]
            color_button.set_pos((self.x + color_button.x, self.y + color_button.y))
            self.colors.append(color_button)

        return self.colors

    def set_size(self, size):
        return Palette(size, self.color)


class LevelSelect(GameObject):
    def __init__(self, size, color, levels):
        super().__init__(size)

        self.levels = levels
        self.level_buttons = []

        self.fill(color)

    def create(self, command):
        level_buttons = []
        grid = GridLayout(3, ceil(len(self.levels) / 3), 10)
        grid.set_pos((5, 5))

        for level in range(len(self.levels)):
            level_btn = Button(color=(92, 34, 15), hover_color=(102, 44, 25), size=(50, 50), command=command,
                               text=str(level + 1))
            level_buttons.append(level_btn)

        layout = grid.create(level_buttons)

        for i, level_btn in enumerate(level_buttons):
            level_btn.set_pos((self.x + layout[i][0], self.y + layout[i][1]))
            self.level_buttons.append(level_btn)

        return self.level_buttons
