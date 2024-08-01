def topological_sort(graph, mode=False):
    marked = [False for _ in range(graph.v)]
    reverse_post = []

    def dfs(v):
        marked[v] = True
        for w in graph.adj_to(v):
            if mode:
                try:
                    w = w.other(v)
                except AttributeError:
                    w = w.end()
            if not marked[w]:
                dfs(w)
        reverse_post.append(v)

    for vertix in range(graph.v):
        if not marked[vertix]:
            dfs(vertix)

    reverse_post.reverse()
    return reverse_post
    
