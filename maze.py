from typing import List, Tuple
from window import Window
from cell import Cell
import time
import random

class Maze:
    def __init__(self,
                 x1,
                 y1,
                 num_rows,
                 num_cols, 
                 cell_size_x, 
                 cell_size_y,
                 win: Window | None = None,
                 seed: str | None = None
                 ) -> None:
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        
        self._cells: List[List[Cell]] = []

        random.seed(seed)

        self._create_cells()

    def _create_cells(self):
        for _ in range(0, self.num_cols):
            col = []
            for _ in range(0, self.num_rows):
                cell = Cell(self.win)
                cell.set_walls(True)
                col.append(cell)
            self._cells.append(col)

        self._break_entrance_and_exit()
        self.draw_maze()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _last_cell(self):
        last_col = self._cells[len(self._cells) - 1]
        return last_col[len(last_col) - 1]


    def draw_maze(self):
        if self.win:
            print("drawing maze")
            for i, column in enumerate(self._cells):
                for j in range(0, len(column)):
                    self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        pos_x = self.x1 + (i * self.cell_size_x)
        pos_y = self.y1 + (j * self.cell_size_y)

        self._cells[i][j].draw(
            pos_x,
            pos_y,
            pos_x + self.cell_size_x,
            pos_y + self.cell_size_y
        )

        self._animate()

    def _animate(self):
        if self.win:
            self.win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        first_cell = self._cells[0][0]
        first_cell.walls['top'].state = False

        self._last_cell().walls['bottom'].state = False

    def _break_walls_r(self, i = 0, j = 0):
        cell: Cell = self._cells[i][j]
        cell.visited = True
        while True:
            to_visit: List[Tuple[str, int, int]] = []
            if i - 1 >= 0 and not self._cells[i-1][j].visited:
                to_visit.append(("left", i - 1, j))
            if i + 1 < len(self._cells) and not self._cells[i+1][j].visited:
                to_visit.append(("right", i + 1, j))
            if j - 1 >= 0 and not self._cells[i][j-1].visited:
                to_visit.append(("top", i, j - 1))
            if j + 1 < len(self._cells[i]) and not self._cells[i][j+1].visited:
                to_visit.append(("bottom", i, j + 1))

            if not to_visit:
                self._draw_cell(i, j)
                return

            choice = random.choice(to_visit)

            next_cell: Cell = self._cells[choice[1]][choice[2]]
            cell.walls[choice[0]].state = False
            next_cell.walls[Cell.shared_wall(choice[0])].state = False
            
            self._break_walls_r(choice[1], choice[2])

    def _reset_cells_visited(self):
        for i, column in enumerate(self._cells):
            for j in range(0, len(column)):
                self._cells[i][j].visited = False
    

    def solve(self):
        print("solving")
        self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        current_cell: Cell = self._cells[i][j]
        current_cell.visited = True
        if current_cell == self._last_cell():
            return True
        
        addrs = [(i - 1, j, "left"), (i + 1, j, "right"), (i, j - 1, "top"), (i, j + 1, "bottom")]
        for addr in addrs:
            if addr[0] in range(0, len(self._cells)) and \
                addr[1] in range(0, len(self._cells[i])) and \
                not self._cells[addr[0]][addr[1]].visited and \
                not self._cells[i][j].walls[addr[2]].state:

                print(f"Checking addr {addr}")
                current_cell.draw_move(self._cells[addr[0]][addr[1]])
                if self._solve_r(i=addr[0], j=addr[1]):
                    return True
                current_cell.draw_move(self._cells[addr[0]][addr[1]], undo=True)

        return False
