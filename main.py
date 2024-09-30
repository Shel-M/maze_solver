from time import sleep
from maze import Maze
from window import Window

def main(): 
    win = Window(800, 600) 

    maze = Maze(10, 10, 10, 10, 50, 50, win)
    sleep(1)
    print(maze.solve())

    win.wait_for_close()

if __name__ == '__main__':
    main()
