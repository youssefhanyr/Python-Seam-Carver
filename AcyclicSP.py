from sorts import topological_sort


class AcyclicSP:

    def __init__(self, graph, s):
        self.graph = graph
        self.distTo, self.edgeTo = [99999999999.9 for _ in range(self.graph.v)], [None for _ in range(self.graph.v)]
        self.distTo[s] = 0.0
        self._construct()

    def _construct(self):
        order = topological_sort(self.graph, True)
        for v in order:
            for e in self.graph.adj_to(v):
                self._relax(e)

    def _relax(self, e):
        v, w = e.start(), e.end()
        hold = self.distTo[v] + e.weight
        if self.distTo[w] >= hold:
            self.distTo[w] = hold
            self.edgeTo[w] = e

    def shortest_path_to(self, destination):
        pather = []
        while self.edgeTo[destination]:
            hold = self.edgeTo[destination]
            pather.append(hold)
            destination = hold.start()
        return pather
        
        
class AcyclicSPMOD:

    def __init__(self, graph, s, sc, sort):
        self.s = s
        self.sc = sc
        self.sort = sort
        self.graph = graph
        self.distTo, self.edgeTo = [99999999999.9 for _ in range(self.graph.v)], [None for _ in range(self.graph.v)]
        self.distTo[s] = 0.0
        self._construct()

    def _construct(self):
        for v in self.sort:
            for e in self.graph.adj_to(v):
                self._relax(e-1, v)

    def _relax(self, e, v):
        if e == self.sc.height*self.sc.width:
            hold = self.distTo[v]
        else:
            x, y = e % self.sc.width, e // self.sc.width
            hold = self.distTo[v] + self.sc.energy_list[y][x]
        if self.distTo[e+1] >= hold:
            self.distTo[e+1] = hold
            self.edgeTo[e+1] = v

    def shortest_path_to(self, destination):
        pather = [destination]
        while self.edgeTo[destination] is not None:
            hold = self.edgeTo[destination]
            pather.append(hold)
            destination = hold
        return pather


class AcyclicSPMODMarkII:

    def __init__(self, graph, s, sc, sort):
        self.s = s
        self.sc = sc
        self.sort = sort
        self.graph = graph
        self.distTo, self.edgeTo = [99999999999.9 for _ in range(self.graph.v)], [None for _ in range(self.graph.v)]
        self.distTo[s] = 0.0
        self._construct()

    def _construct(self):
        for v in self.sort:
            for e in self.graph.adj_to(v):
                self._relax(e-1, v-1)


    def _relax(self, e, v):
        hold = 0.0
        if e == self.sc.height*self.sc.width:
            hold = self.distTo[v+1]
        else:
            x2, y2 = e % self.sc.width, e // self.sc.width
            x1, y1 = v % self.sc.width, v // self.sc.width
            if y2 - 1 == y1 and x1 == x2:
                hold = self.distTo[v+1] + self.sc.energy_list[y2][x2]
            elif x2 - 1 == x1 and y2 - 1 == y1:
                hold = self.distTo[v+1] + self.sc.energy_list[y2][x2] + self._caclu_eneregy(x2, y2-1, x2-1, y2)
            elif x2 + 1 == x1 and y2 - 1 == y1:
                hold = self.distTo[v+1] + self.sc.energy_list[y2][x2] + self._caclu_eneregy(x2, y2-1, x2+1, y2)
            else:
                hold = self.sc.energy_list[y2][x2]
        if self.distTo[e+1] >= hold:
            self.distTo[e+1] = hold
            self.edgeTo[e+1] = v + 1

    def _caclu_eneregy(self, x1, y1, x2, y2):
        if y1  == 0:
            return 0.0
        if x2 < 0:
            X2 = 0
        elif x2 == self.sc.width:
            x2 = self.sc.width - 1
        rx, bx, gx = (self.sc._rgb[y2][x2][i] - self.sc._rgb[y1][x1][i] for i in range(3))
        ry, by, gy = (self.sc._rgb[y2][x2][i] - self.sc._rgb[y1][x1][i] for i in range(3))
        sq_dx = (rx ** 2) + (bx ** 2) + (gx ** 2)
        sq_dy = (ry ** 2) + (by ** 2) + (gy ** 2)
        return sq_dx + sq_dy

    def shortest_path_to(self, destination):
        pather = [destination]
        while self.edgeTo[destination] is not None:
            hold = self.edgeTo[destination]
            pather.append(hold)
            destination = hold
        return pather

