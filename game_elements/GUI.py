from pygame import Surface
from pygame import font


class GameObject(Surface):
    def __init__(self, size=(0, 0)):
        super().__init__(size)

        self.size = size
        self.width, self.height = self.size

        self.position = (0, 0)
        self.x, self.y = self.position

        self.visible = True

        self.color = (0, 0, 0)

    def set_pos(self, position) -> None:
        self.position = position
        self.x, self.y = self.position

    def set_size(self, size):
        self.size = size
        self.width, self.height = self.size

    def hide(self):
        self.set_alpha(0)
        self.visible = False

    def show(self):
        self.set_alpha(255)
        self.visible = True


class InteractedObject(GameObject):
    def __init__(self, size):
        super().__init__(size)

        self.mouse_x, self.mouse_y = 0, 0
        self.__mouse_in = False
        self._prev_mouse_state = 0
        self._mouse_state = 0

    def mouse_moved(self, mouse_pos) -> None:
        self.mouse_x = int(mouse_pos[0] - self.x)
        self.mouse_y = int(mouse_pos[1] - self.y)

    def check_mouse(self, mouse_pos, mouse_state) -> tuple:
        self._prev_mouse_state = self._mouse_state
        self._mouse_state = mouse_state
        self.__mouse_in = False

        if (mouse_pos[0] > self.x) and (mouse_pos[0] < self.x + self.width):
            if (mouse_pos[1] > self.y) and (mouse_pos[1] < self.y + self.height):
                self.mouse_moved(mouse_pos)
                self.__mouse_in = True

        if not self.visible:
            self._mouse_state = 0
            self.__mouse_in = False

        return {'hover': self.__mouse_in, 'click': self._mouse_state}


class Button(InteractedObject):
    def __init__(self, color, hover_color=None, command=None, size=(50, 20), text=""):
        super().__init__(size=size)

        self.color = color
        self.hover_color = self.color
        self.__font = font.Font('game_elements/Pixeltype.ttf', 50)
        self.text = self.__font.render(text, False, "White")

        if hover_color:
            self.hover_color = list(hover_color)

            for i in range(len(self.hover_color)):
                if self.hover_color[i] > 255:
                    self.hover_color[i] = 255
                if hover_color[i] < 0:
                    self.hover_color[i] = 0

        self.fill(self.color)
        self.command = command

    def click(self, *args):
        if self._mouse_state != self._prev_mouse_state:
            return self.command(*args)
