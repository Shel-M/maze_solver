from point import Point
from line import Line
from window import Window


class Cell:
    def __init__(self, win: Window | None = None) -> None:
        self.walls = {
            "left": Wall(),
            "right": Wall(),
            "top": Wall(),
            "bottom": Wall()
        }
        self.visited = False

        self._x1 = 0
        self._x2 = 0
        self._y1 = 0
        self._y2 = 0
        self._win = win

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2

        self.draw_wall("left", Line(Point(self._x1, self._y1), Point(self._x1, self._y2)))
        self.draw_wall("right", Line(Point(self._x2, self._y1), Point(self._x2, self._y2)))
        self.draw_wall("top", Line(Point(self._x1, self._y1), Point(self._x2, self._y1)))
        self.draw_wall("bottom", Line(Point(self._x1, self._y2), Point(self._x2, self._y2)))

    def set_walls(self, state = False):
        for wall in self.walls:
            self.walls[wall].state = state
        
    def draw_wall(self, wall_name, line):
        if self._win:
            self.walls[wall_name].draw(line, self._win)

    def draw_move(self, to_cell, undo=False):
        print("drawing move")
        line = Line(
            Point(
                (self._x1 + self._x2) // 2,
                (self._y1 + self._y2) // 2,
            ),
            Point(
                (to_cell._x1 + to_cell._x2) // 2,
                (to_cell._y1 + to_cell._y2) // 2,
            ),
        )
    
        fill_color = "red"
        if undo: fill_color = "gray"

        if self._win:
            self._win.draw_line(line, fill_color=fill_color)

    @staticmethod
    def shared_wall(cell_wall: str) -> str:
        if cell_wall == 'left':
            return 'right'
        if cell_wall == 'right':
            return 'left'
        if cell_wall == 'top':
            return 'bottom'
        if cell_wall == 'bottom':
            return 'top'

        raise Exception(f'Invalid wall passed to Cell.shared_wall "{cell_wall}"')


class Wall:
    def __init__(self) -> None:
        self.state = False
        self._drawn_state = False

    def draw(self, line: Line, win: Window):
        fill_color = ""
        if self.state != self._drawn_state:
            if self.state:
                fill_color = "black"
            else: 
                fill_color = "white"
                
        win.draw_line(line, fill_color)
        self._drawn_state = self.state
