import heapq
from math import inf
from graph import Graph


def expand_pivot(graph, dist, pivot, low, high):
    """
    Mini-Dijkstra limitado à faixa [low, high).
    """
    pq = [(dist[pivot], pivot)]

    while pq:
        d, u = heapq.heappop(pq)

        if d >= high:
            break
        if d != dist[u]:
            continue

        for v, w in graph.adj[u]:
            nd = d + w
            if low <= nd < high and nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))


def bmssp_simple(graph: Graph, source, width=9, num_pivots=4):
    """
    Versão simplificada (faixas + pivôs), inspirada no paper.

    width      = largura das faixas de distância
    num_pivots = quantos pivôs usamos por faixa
    """

    dist = {v: inf for v in graph.vertices()}
    dist[source] = 0

    finished = set()
    max_dist = 0

    while True:
        low = max_dist
        high = max_dist + width

        # vértices na faixa atual
        S = [u for u in graph.vertices()
             if low <= dist[u] < high and u not in finished]

        if not S:
            break

        # escolhe os pivôs mais promissores
        S.sort(key=lambda x: dist[x])
        pivots = S[:num_pivots]

        # expande cada pivô
        for p in pivots:
            expand_pivot(graph, dist, p, low, high)

        # marca faixa como concluída
        for u in S:
            finished.add(u)

        max_dist += width

    # converte para lista
    res = [inf] * len(graph.vertices())
    for v, d in dist.items():
        res[v] = d
    return res
