from tkinter import Canvas

class Line:
    def __init__(self, point_a, point_b) -> None:
        self.point_a = point_a
        self.point_b = point_b

    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(
            self.point_a.x,
            self.point_a.y,
            self.point_b.x,
            self.point_b.y, 
            fill=fill_color,
            width=2
        )



