def topological_sort(graph, mode=False):
    """
    Sorts the graph topologically, only works in acyclic graphs, sorts all the nodes from the source node
    to the farthest one it can reach without going back

    :param graph: the graph list it will sort
    :param mode: is working with bidirectional nodes (true) or monodirectional nodes (false)
    """
    marked = [False for _ in range(graph.v)]
    reverse_post = []

    def dfs(v):
        marked[v] = True
        for w in graph.adj_to(v):
            if mode:
                try:
                    w = w.other(v)
                except AttributeError:      # incase a node is not connected bothways
                    w = w.end()
            if not marked[w]:
                dfs(w)
        reverse_post.append(v)

    for vertix in range(graph.v):
        if not marked[vertix]:
            dfs(vertix)

    reverse_post.reverse()          # reverses the list because it is added (because of recrusion) in opposite order
    return reverse_post
    
