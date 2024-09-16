from copy import copy
from VSeamCarver import VSeamCarver
from typing_extensions import deprecated


@deprecated
def fix_graph(graph, graph_list, path, h, w):

    """This was a function that fixes the graph, as in, it renames the nodes affected by the seam removal but
    it proved to be more work than what it was supposed to save time avoiding, so it is deprecated """

    old_list = copy(graph_list)
    count = 0
    extra = 0

    for i in range(1, h+1):
        graph_list.pop(path[i])

    for i in range(1, h*w - w + 1):
        x, y, xo = (i-1) % w, (i-1) // w, i+count
        prev_x = path[-y-2]
        if xo == prev_x:
            xo += 1
            count += 1
            if i == 1:
                extra = -1

        for j in range(len(graph.adj_to(i))):
            graph.adj_to(i)[j] -= (count + 1 + extra)

        if extra:
            extra = 0

        if x % w == 0 and len(old_list[xo]) == 3:
            graph.adj_to(i).pop()
        elif x % w == w - 1 and len(old_list[xo]) == 3:
            graph.adj_to(i).pop(0)

    for i in range(h*w - w + 1, h*w + 1):
        graph.adj_to(i)[0] -= h

    graph_list[0].pop()

    return graph_list

