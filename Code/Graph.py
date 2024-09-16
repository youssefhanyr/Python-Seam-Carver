class Graph:

    """Graph's api, based on the algorithms course, princeton"""

    def __init__(self, v):
        self.v = v
        self.e = 0
        self._adj = [list() for _ in range(v)]

    def add_edge(self, v, w):
        """adds edge connected both ways, from v to w and the other way around

        :param v: first node to connected and be connected
        :param w: second node - - -"""
        self._adj[v].append(w)
        self._adj[w].append(v)
        self.e += 1
        
    def adj_to(self, v):
        return self._adj[v]

    def degree(self, v):            # most of these functions do not concern us so i wont bother doc'ing them
        degree = 0
        for _ in self._adj[v]:
            degree += 1
        return degree

    def max_degree(self):
        max_degree = 0
        for x in range(self.v):
            current_degree = self.degree(x)
            if current_degree > max_degree:
                max_degree = current_degree
        return max_degree

    def avg_degree(self):
        return (2 * self.e) / self.v

    def number_self_loop(self):
        count = 0
        for v in range(self.V):
            for x in self._adj[v]:
                if v == x:
                    count += 1
        return count // 2
        
class DiGraph:

    """Same api as the normal graph, but connects nodes in one way according to the order of the param"""

    def __init__(self, v):
        self.v = v
        self.e = 0
        self.adj = [list() for _ in range(v)]

    def add_edge(self, v, w):
        """connects v to w only
        
        :param v: the node to connect from
        :param w: the node to connect v to"""
        self.adj[v].append(w)
        self.e += 1

    def adj_to(self, v):
        return self.adj[v]

    def out_degree(self, v):
        degree = 0
        for _ in self.adj[v]:
            degree += 1
        return degree

    def in_degree(self, v):
        count = 0
        for vertix in self.adj:
            for edge in vertix:
                if edge == v:
                    count += 1
                    break
        return count

    def max_out_degree(self):
        max_degree = 0
        for x in range(self.v):
            current_degree = self.out_degree(x)
            if current_degree > max_degree:
                max_degree = current_degree
        return max_degree

    def avg_degree(self):
        return (2 * self.e) / self.v

    def number_self_loop(self):
        count = 0
        for v in range(self.v):
            for x in self.adj[v]:
                if v == x:
                    count += 1
        return count // 2

