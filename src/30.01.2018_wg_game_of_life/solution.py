"""
This challenge is about calculating the next generation of Conway’s game of life,
given any starting position.
See http://en.wikipedia.org/wiki/Conway%27s_Game_of_Life for background.

You start with a two dimensional grid of cells,
where each cell is either alive or dead. In this version of the problem,
the grid is finite, and no life can exist off the edges.
When calcuating the next generation of the grid, follow these rules:

1. Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
2. Any live cell with more than three live neighbours dies, as if by overcrowding.
3. Any live cell with two or three live neighbours lives on to the next generation.
4. Any dead cell with exactly three live neighbours becomes a live cell.

You should write a program that accepts an arbitrary grid of cells,
and will output a similar grid showing the next generation based on the rules above.
"""

class Life(object):
    def __init__(self, input):
        self.state = input

    def will_cell_survive_after_first_rule(self, x, y):
        alive = self.get_alive_neighbours_count(x, y)
        return alive > 1

    def will_cell_die_after_second_rule(self, x, y):
        alive = self.get_alive_neighbours_count(x, y)
        return alive > 3

    def get_alive_neighbours_count(self, x, y):
        count = 0
        for x_diff in range(x-1, x+2):
            if x_diff < 0 or x_diff >= len(self.state):
                continue

            for y_diff in range(y-1, y+2):
                if y_diff < 0 or y_diff >= len(self.state):
                    continue

                if x == x_diff and y == y_diff:
                    continue

                if self.state[x_diff][y_diff] == '#':
                    count += 1

        return count


