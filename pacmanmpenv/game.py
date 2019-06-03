

import numpy as np
import random
from pacmanmpenv.maze import Maze


class PacmanGame:
    def __init__(self, maze_size = 5, nb_ghosts=3, pacman_speed=1):
        self.pacman_speed = pacman_speed
        self.nb_ghosts = nb_ghosts
        self.Maze = Maze(maze_size, maze_size)

        self.score = 0
        self.pacman_pos = (0,0)
        self.ghost_pos = [(0,0) for i in range(nb_ghosts)]

    def reset_game(self):
        self.score = 0

        spawns = random.choices(self.Maze.emptyCells(), k=self.nb_ghosts +1)

        for k in range(self.nb_ghosts):
            i, j = spawns[k]
            self.ghost_pos[k] = i,j
            self.Maze.add2cell(i,j, "g" + str(k))

        i, j = spawns[self.nb_ghosts]
        self.pacman_pos = (i,j)
        self.Maze.add2cell(i, j, "pacman")

    def move(self, entity, dir):
        if entity == 0:
            i, j = self.pacman_pos

            if dir == 1: i+=1
            if dir == 2: i-=1
            if dir == 3: j+=1
            if dir == 4: j-=1


    def step(self, actions):

        # actions = pacman, g1, g2 ...


