import numpy as np
from PIL import Image
from Graph import DiGraph
from math import sqrt
from AcyclicSP import AcyclicSPMOD
from sorts import topological_sort


class VSeamCarver:

    def __init__(self, picture, ans, pic2=None, w=None, h=None, x1=None, y1=None, x2=None, y2=None):
        if isinstance(picture, str):
            self.picture = Image.open(picture)
            self.width, self.height = self.picture.width, self.picture.height
            self.energy_list = [[None for _ in range(self.width)] for _ in range(self.height)]
        else:
            self.picture = picture
            self.energy_list = pic2
            self.width, self.height = w, h
        self.graphV = None
        self.ans = ans
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self._construct()
        self.sortV = topological_sort(self.graphV)

    def _construct(self):
        pixels = self.__construct_list()
        self.graphV = DiGraph(pixels + 2)
        for vertex in range(self.graphV.v):

            if vertex == 0:
                for p in range(1, self.width + 1):
                    self.graphV.add_edge(vertex, p)
                continue
            elif vertex == self.width*self.height + 1:
                for p in range(vertex - 1, self.width*(self.height - 1), -1):
                    self.graphV.add_edge(p, vertex)
                continue

            w = (vertex - 1) % self.width
            if vertex + self.width >= self.width * self.height + 1:
                continue
            elif w == 0:
                self.graphV.add_edge(vertex, vertex + self.width)
                self.graphV.add_edge(vertex, vertex + self.width + 1)
            elif w == self.width - 1:
                self.graphV.add_edge(vertex, vertex + self.width - 1)
                self.graphV.add_edge(vertex, vertex + self.width)
            else:
                self.graphV.add_edge(vertex, vertex + self.width - 1)
                self.graphV.add_edge(vertex, vertex + self.width)
                self.graphV.add_edge(vertex, vertex + self.width + 1)

        if self.energy_list[0][0] is not None:
            pass
        else:
            self.__construct_energy()

    def __construct_energy(self):
        for i in range(self.height):
            for j in range(self.width):
                self.energy_list[i][j] = self.energy(j, i)

    def __construct_list(self):
        if self.energy_list[0][0] == 1000.0 or self.energy_list[0][0] == 1500.0:
            self._rgb = self.picture
            return self.width*self.height
        self._rgb = []
        stuff = list(self.picture.getdata())
        for y in range(0, self.width * self.height, self.width):
            z = stuff[y:y + self.width]
            self._rgb.append(z)
        return self.width*self.height

    def energy(self, x, y):
        if x >= self.width or y >= self.height:
            raise IndexError(f"Coord nots right")
        if self.x1 is not None and self.x2 is not None and self.y1 is not None and self.y2 is not None:
            if (self.x1 <= x <= self.x2) and (self.y1 <= y <= self.y2):
                return self.ans*15000.0
        if x == self.width - 1 or x == 0 or y == 0 or y == self.height - 1:
            return 1000.0
        rx, bx, gx = (self._rgb[y][x + 1][i] - self._rgb[y][x - 1][i] for i in range(3))
        ry, by, gy = (self._rgb[y + 1][x][i] - self._rgb[y - 1][x][i] for i in range(3))
        sq_dx = (rx ** 2) + (bx ** 2) + (gx ** 2)
        sq_dy = (ry ** 2) + (by ** 2) + (gy ** 2)
        return sqrt(sq_dx + sq_dy)

    def findvseam(self):
        total_energy = 0.0
        finder = AcyclicSPMOD(self.graphV, 0, self, self.sortV)
        path = finder.shortest_path_to(self.width*self.height + 1)
        for v in path:
            if v == 0 or v == self.width*self.height + 1:
                continue
            v -= 1
            x, y = v % self.width, v // self.width
            total_energy += self.energy_list[y][x]
        return path

    def removeverticalseam(self, path):
        flag = 0
        if path is None:
            raise ValueError("Must have a legitimate path!")
        for pixel in path:
            if pixel == 0 or pixel == self.width*self.height + 1:
                continue
            pixel -= 1
            x, y = pixel % self.width, pixel // self.width
            if self.x1 is not None and self.y1 is not None and self.x2 is not None and self.y2 is not None:
                if x < self.x1 and flag == 0:
                    flag = 1
            self._rgb[y].pop(x)
            self.energy_list[y].pop(x)
        self.width -= 1
        for pixel in path:
            pixel -= 1
            x, y = pixel % (self.width + 1), pixel //(self.width + 1)
            if y == self.height:
                continue
            if x == 0:
                self.energy_list[y][x] = self.energy(x, y)
                if y < self.height - 1:
                    self.energy_list[y + 1][x] = self.energy(x, y + 1)
                if y > 0:
                    self.energy_list[y - 1][x] = self.energy(x, y - 1)
            elif y == 0:
                self.energy_list[y][x - 1] = self.energy(x - 1, y)
                self.energy_list[y + 1][x] = self.energy(x, y + 1)
                if x < self.width:
                    self.energy_list[y][x] = self.energy(x, y)
            elif x == self.width:
                self.energy_list[y][x - 1] = self.energy(x - 1, y)
                self.energy_list[y - 1][x - 1] = self.energy(x - 1, y - 1)
                if y < self.height - 1:
                    self.energy_list[y + 1][x - 1] = self.energy(x - 1, y + 1)
            elif y == self.height - 1:
                self.energy_list[y][x] = self.energy(x, y)
                self.energy_list[y - 1][x] = self.energy(x, y - 1)
            else:
                self.energy_list[y][x] = self.energy(x, y)
                self.energy_list[y - 1][x] = self.energy(x, y - 1)
                self.energy_list[y][x - 1] = self.energy(x-1, y)
                self.energy_list[y + 1][x] = self.energy(x, y + 1)

        temp = self._rgb
        temp2 = self.energy_list
        if flag == 0:
            return temp, temp2, self.width, self.height, self.x1, self.y1, self.x2, self.y2
        elif flag == 1:
            return temp, temp2, self.width, self.height, self.x1-1, self.y1, self.x2-1, self.y2


''' First, you need to obtain the min path, to do that you have to
    go (assuming we are looking for v seam) point by point in width checking
    every path from each point in the bottom row with every one in the upper, w*h
    attempts will occur and only one will be minimum, as for the horizontal one
    i have chosen to keep a horizontal version of the graph what i described
    will be the same procedure

    deletion will start bottom-up, first find the last point that will be deleted
    and make sure to remove it from every upper point that has previously mentioned
    point in its adj_to same will happen with the other ones in the upper rows until
    the highest is reached then no deletion will be needed other than the deletion of the point
    itself.

 '''