def run_bmssp(graph: Graph, source, L=4, k=6, t=2):
    dist = [inf] * len(graph.adj)
    dist[source] = 0

    S = {source}
    B = inf

    while S:
        B_new, U = bmssp(graph, L, B, S, dist, t=t, k=k)

        # nova fronteira: só quem ainda pode melhorar
        S = set()
        for u in U:
            for v, w in graph.adj[u]:
                if dist[v] > dist[u] + w:
                    S.add(v)

        B = B_new

    return dist