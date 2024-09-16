from PIL import Image
from Code.Graph import DiGraph
from math import sqrt
from AcyclicSP import AcyclicSPMOD
from Code.sorts import topological_sort


class VSeamCarver:

    """Backwards Vertical seam carver, shrinks width of picture"""

    def __init__(self, picture, ans, pic2=None, w=None, h=None, x1=None, y1=None, x2=None, y2=None):

        """
        :param picture: either the path of the picture, or a Image from PIL
        :param ans: variable to enable protection for certain pixels or to target them
        :param pic2: the energy table if the picture is already initialized, else leave it a None
        :param w: width of the picture if initialized, else is None
        :param h: height of the picture if initialized, else is None
        :param x1: x of the first border pixel of the target region (to protect or target)
        :param y1: y of the first border pixel of the target region (to protect or target)
        :param x2: x of the second border pixel of the target region (to protect or target)
        :param y2: y of the second border pixel of the target region (to protect or target)"""    

        if isinstance(picture, str):
            self.picture = Image.open(picture)
            self.width, self.height = self.picture.width, self.picture.height
            self.energy_list = [[None for _ in range(self.width)] for _ in range(self.height)]  # creates the energy table
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
        self.graphV = DiGraph(pixels + 2)           # two extra points for source and sink nodes
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

            elif w == self.width - 1:                                       # constructs the image graph as shown in the readme
                self.graphV.add_edge(vertex, vertex + self.width - 1)
                self.graphV.add_edge(vertex, vertex + self.width)

            else:
                self.graphV.add_edge(vertex, vertex + self.width - 1)
                self.graphV.add_edge(vertex, vertex + self.width)
                self.graphV.add_edge(vertex, vertex + self.width + 1)

        if self.energy_list[0][0] is not None:              # just a check to see if the energy table exists or not
            pass
        else:
            self.__construct_energy()

    def __construct_energy(self):
        for i in range(self.height):
            for j in range(self.width):
                self.energy_list[i][j] = self.energy(j, i)

    # both functions are called only once at the very start of the compression

    def __construct_list(self):                 # constructs the RGB pixel table
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

        """Returns the square diff of the lumunosity of the pixels by calculating delR, delG, delB
        This is the backwards method.

        :param x: x coordinate of the pixel in the energy table
        :param y: y coordinate of the pixel in the energy table"""


        if x >= self.width or y >= self.height:
            raise IndexError(f"Coord nots right")
        if self.x1 is not None and self.x2 is not None and self.y1 is not None and self.y2 is not None: # checks if there is a target
            if (self.x1 <= x <= self.x2) and (self.y1 <= y <= self.y2):                                 # region first and multiply it
                return self.ans*15000.0                                                             # by 1 to protect or by -1 to target
        if x == self.width - 1 or x == 0 or y == 0 or y == self.height - 1:
            return 1000.0
        rx, bx, gx = (self._rgb[y][x + 1][i] - self._rgb[y][x - 1][i] for i in range(3))
        ry, by, gy = (self._rgb[y + 1][x][i] - self._rgb[y - 1][x][i] for i in range(3))
        sq_dx = (rx ** 2) + (bx ** 2) + (gx ** 2)
        sq_dy = (ry ** 2) + (by ** 2) + (gy ** 2)
        return sqrt(sq_dx + sq_dy)

    def findvseam(self):
        """Driver function that finds the shortest path and returns the list"""

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
            pixel -= 1                  # the count of pixels in both lists

            x, y = pixel % self.width, pixel // self.width
            if self.x1 is not None and self.y1 is not None and self.x2 is not None and self.y2 is not None:
                if x < self.x1 and flag == 0:                       # checks if it will return the region coords or not
                    flag = 1
            self._rgb[y].pop(x)
            self.energy_list[y].pop(x)                          # removing the nodes in the seam from the lists

        self.width -= 1
        for pixel in path:                                      # recalculates the energy of affected nodes
            pixel -= 1
            x, y = pixel % (self.width + 1), pixel //(self.width + 1)       # calculates the x and y of the points deleted

            if y == self.height:                    # pixels at the bottom have a set amount of energy, constants
                continue

            if x == 0:                                               # checks where was the points was and decides which pixels to re calculate
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

            elif x == self.width:                                       # could have been wrote better, instead of repeating code
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

