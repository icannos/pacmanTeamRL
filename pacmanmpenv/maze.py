
import numpy as np
from PIL import Image
from noise import snoise2
import matplotlib.pyplot as plt

import networkx as nx


class Maze:
    def __init__(self, width=5, height=5, cells_types=("rewards", "wall", "empty", "g1", "g2", "g3", "pacman")):
        self.height = height
        self.width = width

        self.map_height = 2 * self.height + 1
        self.map_width = 2*self.width+1

        self.cellsTypes = cells_types

        self.maze_map = None

    def add2cell(self, i, j, type):
        self.maze_map[i, j] = np.logical_or(self.maze_map[i, j], self.vectorCell(type))

    def rm2cell(self, i, j, type):
        self.maze_map[i, j] = np.logical_and(self.maze_map[i, j], np.logical_not(self.vectorCell(type)))

    def emptyCells(self):
        empty_cells = []
        for i in range(self.map_height):
            for j in range(self.map_width):
                if self.maze_map[i,j] != self.vectorCell("wall"):
                    empty_cells.append((i,j))
        return empty_cells

    def vectorCell(self, type="empty"):
        cell = np.zeros(len(self.cellsTypes), dtype=np.bool)
        cell[self.cellsTypes.index(type)] = True

        return cell

    def regen_maze(self):
        graph = nx.grid_graph([self.height, self.width])

        for u,v,d in graph.edges(data=True):
            d["weight"] = np.random.uniform(0, 10)

        T = nx.minimum_spanning_tree(graph, "weight")

        graph = self.rounding_path(T)
        self.maze_map = self.graph2map(graph)

    def rounding_path(self, T):
        for i in range(self.height-1):
            T.add_edge((i,0), (i+1, 0))
            T.add_edge((i,self.width-1), (i+1, self.width-1))

        for j in range(self.width-1):
            T.add_edge((0, j), (0, j+1))
            T.add_edge((self.height-1, j), (self.height-1, j+1))

        return T

    def graph2map(self, graph):
        maze_map = np.ones((2*self.height+1, 2*self.width+1, len(self.cellsTypes)), dtype=np.bool)

        for i in range(self.height):
            for j in range(self.width):
                ui = 2*i+1
                uj = 2*j+1
                maze_map[2*i+1, 2*j+1] = 0
                if graph.has_edge((i, j), (i, j+1)): maze_map[ui, uj+1] = self.vectorCell("reward")
                if graph.has_edge((i, j), (i+1, j)): maze_map[ui+1, uj] = self.vectorCell("reward")

        return maze_map

    def to_str(self):
        s = ""
        for i in range(2*self.height+1):

            for j in range(2*self.width+1):
                if self.maze_map[i, j] == 1:
                    s+= "#"
                else:
                    s+= " "
            s+="\n"
