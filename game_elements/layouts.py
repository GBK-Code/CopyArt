from game_elements.GUI import GameObject


class GridLayout(GameObject):
    def __init__(self, cell_width, cell_height, offset):
        super().__init__()
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.offset = offset

        self.elements = []

    def create(self, game_objects) -> list:
        for i, game_object in enumerate(game_objects):
            x = self.x + (game_object.width + self.offset) * (i - self.cell_width * (i // self.cell_width))
            y = self.y + (game_object.height + self.offset) * (i // self.cell_width)
            self.elements.append((x, y))

        return self.elements
