import random
import time # Learned about this last year, but also read about it here: https://www.geeksforgeeks.org/python-time-module/
from kbhit import KBHit

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))) 
# Was having path issues trying to call on the Array2D file. So I found this workaround on Slack. https://stackoverflow.com/questions/21005822/what-does-os-path-abspathos-path-joinos-path-dirname-file-os-path-pardir
from datastructures.array2d import Array2D

    
class Cell:
    """Represents the cells within the Game of Life grid."""
    def __init__(self, is_alive = False): # The cell starts off as dead/False.
        self.is_alive = is_alive

    def set_as_alive(self, alive):
        """Updates the living condition of the cell."""
        self.is_alive = alive

    def __repr__(self):
        return "⚛︎" if self.is_alive else "·" # I changed the emoji because it was interfering with the spacing of my grid borders. I also added a marker for the dead cells because I found it visually confusing to have none.

class Grid:
    """Represents the grid of cells in the Game of Life."""
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = Array2D.empty(rows, cols, Cell)

    def randomize_seed(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col].set_as_alive(random.random() < 0.5)

    def count_neighbors(self, row, col):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)] # Handles indexing for directional checks. 
        count = 0
        for dr, dc in directions: # Learnt that delta row and delta column are used to signify change in direction. https://stackoverflow.com/questions/65247308/find-indices-of-elements-in-all-eight-directions-of-a-python-2d-array-matrix | https://www.reddit.com/r/leetcode/comments/1hswzgt/coming_from_java_python_has_so_many_niceties_that/ 
            r, c = row + dr, col + dc
            if 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c].is_alive:
                count += 1
        return count
    
    def copy_grid(self):
        new_grid = Grid(self.rows, self.cols)
        for row in range(self.rows):
            for col in range(self.cols):
                new_grid.grid[row][col].set_as_alive(self.grid[row][col].is_alive)
        return new_grid
    
    def update_grid(self):
        new_grid = self.copy_grid()
        for row in range(self.rows):
            for col in range(self.cols):
                neighbors = self.count_neighbors(row, col)
                if self.grid[row][col].is_alive:
                    new_grid.grid[row][col].set_as_alive(neighbors in [2, 3])
                else:
                    new_grid.grid[row][col].set_as_alive(neighbors == 3)
        self.grid = new_grid.grid

    def __repr__(self):
        horizontal_border = "𖢅" + "-" * (2 * self.cols + 1) + "𖢅"
        grid_str = [horizontal_border]

        for row in range(self.rows):
            row_str = "| " + " ".join(str(self.grid[row][col]) for col in range(self.cols)) + " |"
            grid_str.append(row_str)

        grid_str.append(horizontal_border)
        return "\n".join(grid_str)

class GameController:
    """Handles the Game of Life game logic."""
    def __init__(self, rows = 15, cols = 15):
        self.grid = Grid(rows, cols)
        self.history = []
        self.kb = KBHit()
        self.mode = "manual"
        self.speed = 1.0
        self.generation = 0
        self.grid.randomize_seed()

    def adjust_speed(self, key):
        if key == "+" and self.speed > 0.1:
            self.speed -= 0.1
        elif key == "-" and self.speed < 2.0:
            self.speed += 0.1
        print(f"Speed set to: {self.speed:.1f} seconds per step.")

    def check_stagnation(self):
        current_state = repr(self.grid)
        return current_state in self.history
    
    def run(self):
        print("Press 'q' to quit.")
        print("Press 's' to step to the next generation.")
        print("Press 'c' to continue in automatic mode.")
        print("Press '+' to increase simulation speed or '-' to decrease it.")
        
        while True:
            print(f"Generation {self.generation}:")
            print(self.grid)

            if self.check_stagnation():
                print(f"Game ended after {self.generation} generations due to non-stability.")
                break
        
            if self.kb.kbhit():
                key = self.kb.getch().lower() # Getch returns a keyboard character when it is input by the players.
                if key == 'q':
                    print("Simulation ended.")
                    break
                elif key == 's':
                    self.mode = "manual"
                elif key == 'c':
                    self.mode = "auto"
                elif key in ['+', '-']:
                    self.adjust_speed(key)

            if self.mode == "auto":
                time.sleep(self.speed) # Allows a pause duration between the display of each generation while in automatic mode.
            else:
                print("Press 's' to step, 'c' for auto mode, 'q' for quit, or '+'/'-' to increase or decrease simulation speed.")
                while not self.kb.kbhit():
                    pass
                key = self.kb.getch().lower()
                if key == 's':
                    pass
                elif key == 'c':
                    self.mode = "auto"
                elif key == 'q':
                    break

            self.history.append(repr(self.grid)) # Converting the current grid to a string and storing it in the history list.
            if len(self.history) > 5: # History stores five previous grids then gets rid of the oldest entry when that it exceeded.
                self.history.pop(0)
            self.grid.update_grid() # Transitions grid to the next generation.
            self.generation += 1 

        print("Simulation ended.")
        restart = input("Would you like to restart? (Y/N):").strip().upper()
        if restart == "Y":
            self.__init__(rows = self.grid.rows, cols = self.grid.cols)
            self.run()


if __name__ == '__main__':
    game = GameController(rows = 15, cols = 15)
    game.run()
