"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list=None,
                 zombie_list=None, human_list=None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        self._obstacle_list = obstacle_list
        if obstacle_list is not None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list is not None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list is not None:
            self._human_list = list(human_list)
        else:
            self._human_list = []

    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._human_list = []
        self._zombie_list = []

    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))

    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)

    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """

        for index in range(len(self._zombie_list)):
            yield self._zombie_list[index]

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))

    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)

    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield human

    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """

        dist_field = [[self._grid_height * self._grid_width for dummy_i in range(self._grid_width)] for dummy_j in range(self._grid_height)]

        queue = poc_queue.Queue()

        if entity_type == ZOMBIE:
            for zombie in self.zombies():
                queue.enqueue(zombie)
                dist_field[zombie[0]][zombie[1]] = 0
        else:
            for human in self.humans():
                queue.enqueue(human)
                dist_field[human[0]][human[1]] = 0

        while len(queue) > 0:
            elem = queue.dequeue()
            x_pos = elem[0]
            y_pos = elem[1]
            next_moves = self.four_neighbors(x_pos, y_pos)
            for [new_x, new_y] in next_moves:
                if 0 <= new_x < self._grid_height and 0 <= new_y < self._grid_width and self.is_empty(new_x, new_y):
                    if dist_field[x_pos][y_pos] + 1 < dist_field[new_x][new_y]:
                        dist_field[new_x][new_y] = dist_field[x_pos][y_pos] + 1
                        queue.enqueue([new_x, new_y])

        return dist_field

    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """

        for index in range(len(self._human_list)):
            element = self._human_list[index]
            x_pos = element[0]
            y_pos = element[1]

            max_dist = 0
            cells_allowed = []

            next_moves = self.eight_neighbors(x_pos, y_pos)
            next_moves.append((x_pos, y_pos))
            print(next_moves)
            for [new_x, new_y] in next_moves:
                if 0 <= new_x < self._grid_height and 0 <= new_y < self._grid_width and self.is_empty(new_x, new_y):
                    if zombie_distance_field[new_x][new_y] == max_dist:
                        cells_allowed.append((new_x, new_y))
                    if zombie_distance_field[new_x][new_y] > max_dist:
                        cells_allowed = [(new_x, new_y)]
                        max_dist = zombie_distance_field[new_x][new_y]
            ran_select = random.choice(cells_allowed)
            self._human_list[index] = ran_select

    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """

        for index in range(len(self._zombie_list)):
            element = self._zombie_list[index]
            x_pos = element[0]
            y_pos = element[1]

            min_dist = float("inf")
            cells_allowed = []

            next_moves = self.four_neighbors(x_pos, y_pos)
            next_moves.append((x_pos, y_pos))
            for [new_x, new_y] in next_moves:
                if 0 <= new_x < self._grid_height and 0 <= new_y < self._grid_width and self.is_empty(new_x, new_y):
                    if human_distance_field[new_x][new_y] == min_dist:
                        cells_allowed.append((new_x, new_y))
                    if human_distance_field[new_x][new_y] < min_dist:
                        cells_allowed = [(new_x, new_y)]
                        min_dist = human_distance_field[new_x][new_y]
            ran_select = random.choice(cells_allowed)
            self._zombie_list[index] = ran_select
