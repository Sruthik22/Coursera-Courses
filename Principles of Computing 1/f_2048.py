"""
Clone of 2048 game.
"""

import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    orig_size = len(line)

    line = [i for i in line if i != 0]

    arr = []

    index = 0
    while index < len(line):
        if index == len(line) - 1:
            arr.append(line[index])
        else:
            if line[index] == line[index + 1]:
                arr.append(line[index] * 2)
                index += 1
            else:
                arr.append(line[index])
        index += 1
    arr += [0] * (orig_size - len(arr))
    return arr


def check_equal(orig_row, update_row):
    """
    Checks if two arrays are equal by comparing all of the characters
    """
    length = len(orig_row)
    for index in range(length):
        if orig_row[index] != update_row[index]:
            return False
    return True


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self._height = grid_height
        self._width = grid_width
        self._grid = []
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for dummy_i in range(self._width)] for dummy_j in range(self._height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        grid_string = "["
        for index_r in range(self._height):
            if index_r != 0:
                grid_string += ' '
            grid_string += str(self._grid[index_r])
            if index_r < self._height - 1:
                grid_string += '\n'
        grid_string += "]"
        return grid_string

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def upper(self, changed):
        """
        :param changed:
        :return:
        """
        for index_w in range(self._width):
            orig_column = []
            column_to_change = []
            for index_h in range(self._height):
                orig_column.append(self.get_tile(index_h, index_w))
                column_to_change.append(self.get_tile(index_h, index_w))
            column_to_change = merge(column_to_change)
            for index_h in range(self._height):
                self.set_tile(index_h, index_w, column_to_change[index_h])
            if not check_equal(column_to_change, orig_column):
                changed = True
        return changed

    def down(self, changed):
        """
        :param changed:
        :return:
        """
        for index_w in range(self._width):
            orig_column = []
            column_to_change = []
            for index_h in range(self._height):
                orig_column.append(self.get_tile(index_h, index_w))
                column_to_change.append(self.get_tile(index_h, index_w))
            column_to_change.reverse()
            column_to_change = merge(column_to_change)
            column_to_change.reverse()
            for index_h in range(self._height):
                self.set_tile(index_h, index_w, column_to_change[index_h])
            if not check_equal(column_to_change, orig_column):
                changed = True
        return changed

    def right(self, changed):
        """

        :param changed:
        :return:
        """
        for index_h in range(self._height):
            orig_row = self._grid[index_h]
            orig_row.reverse()
            update_row = merge(orig_row)
            update_row.reverse()
            orig_row.reverse()
            if not check_equal(orig_row, update_row):
                changed = True
            self._grid[index_h] = update_row
        return changed

    def left(self, changed):
        """

        :param changed:
        :return:
        """
        for index_h in range(self._height):
            orig_row = self._grid[index_h]
            update_row = merge(orig_row)
            self._grid[index_h] = update_row
            if not check_equal(orig_row, update_row):
                changed = True
        return changed

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        changed = False

        if direction == UP:
            changed = self.upper(changed)
        elif direction == DOWN:
            changed = self.down(changed)
        elif direction == RIGHT:
            changed = self.right(changed)
        else:
            changed = self.left(changed)
        if changed:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        prob = random.random()
        tile = 2
        if prob < 0.1:
            tile = 4
        empty_squares = []
        for index_h in range(self._height):
            for index_w in range(self._width):
                if self.get_tile(index_h, index_w) == 0:
                    empty_squares.append([index_h, index_w])
        selected_index = random.choice(empty_squares)
        self.set_tile(selected_index[0], selected_index[1], tile)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]
