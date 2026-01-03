# bmssp.py
#
# Implementação educacional inspirada fielmente nos 3 algoritmos
# do paper "Breaking the Sorting Barrier..."
#
# Componentes:
# 1. BaseCase (Algorithm 2)
# 2. FindPivots (Algorithm 1)
# 3. BMSSP (Algorithm 3)
#
# Comparação:
# - Melhora sobre o código do outro grupo:
#   ✔ pivôs de fato reduzem a fronteira
#   ✔ recursão sobre intervalos de distância
#   ✔ mantém coerência com a definição do paper
#
# Observação: Esta versão é simplificada para ensino.

import heapq
from math import inf
from graph import Graph


# ==========================================================
# Algorithm 2 — BaseCase(B, S)
# ==========================================================
def base_case(graph: Graph, B, S, dist, k):
    # S = {x}
    x = next(iter(S))

    U0 = set(S)
    H = [(dist[x], x)]   # heap de (distância, vértice)

    while H and len(U0) < k + 1:
        d_u, u = heapq.heappop(H)
        U0.add(u)

        for v, w in graph.adj[u]:
            nd = d_u + w

            if nd <= dist[v] and nd < B:
                dist[v] = nd
                heapq.heappush(H, (nd, v))

    if len(U0) <= k:
        return B, U0
    else:
        Bp = max(dist[v] for v in U0)
        U = {v for v in U0 if dist[v] < Bp}
        return Bp, U


# ==========================================================
# Algorithm 1 — FindPivots(B, S)
# ==========================================================
def find_pivots(graph: Graph, B, S, dist, k):
    W = set(S)
    W_prev = set(S)

    for _ in range(k):
        Wi = set()

        for u in W_prev:
            for v, w in graph.adj[u]:
                nd = dist[u] + w

                if nd <= dist[v]:
                    if nd < dist[v]:
                        dist[v] = nd
                    if nd < B:
                        Wi.add(v)

        W |= Wi
        W_prev = Wi

        if len(W) > k * len(S):
            return set(S), W

    # construir floresta F
    F = set()
    for u in W:
        for v, w in graph.adj[u]:
            if v in W and dist[v] == dist[u] + w:
                F.add((u, v))

    # pivôs = raízes com >= k vértices
    P = set()
    for u in S:
        count = sum(1 for (a, b) in F if a == u or b == u)
        if count >= k:
            P.add(u)

    return P, W


# ==========================================================
# Algorithm 3 — BMSSP(l, B, S)
# ==========================================================
def bmssp(graph: Graph, l, B, S, dist, t=2, k=2):

    if l == 0:
        return base_case(graph, B, S, dist, k)

    P, W = find_pivots(graph, B, S, dist, k)

    D = []
    for x in P:
        heapq.heappush(D, (dist[x], {x}))

    U = set()
    i = 0
    B0 = min((dist[x] for x in P), default=B)

    while len(U) < k * (2 ** (l * t)) and D:
        i += 1
        Bi, Si = heapq.heappop(D)

        Bp, Ui = bmssp(graph, l - 1, Bi, Si, dist, t, k)

        U |= Ui
        B0 = min(B0, Bp)

        for u in Ui:
            for v, w in graph.adj[u]:
                nd = dist[u] + w

                if nd <= dist[v]:
                    if nd < dist[v]:
                        dist[v] = nd

                    if nd < min(Bp, B):
                        heapq.heappush(D, (nd, {v}))

    # fase final
    U |= {x for x in W if dist[x] < B0}

    return B0, U


# ==========================================================
# Wrapper externo — que roda BMSSP completo
# ==========================================================
def run_bmssp(graph: Graph, source, L=4, k=6, t=2):
    # d^[·] — estimativas de distâncias
    dist = {v: inf for v in graph.vertices()}
    dist[source] = 0

    # vértices já comprovadamente completos
    complete = set()

    # fronteira inicial
    S = {source}
    B = inf

    while S:
        B_new, U = bmssp(graph, L, B, S, dist, t=t, k=k)

        # marca vertices resolvidos
        complete |= U

        # nova fronteira S:
        # todos vértices ainda incompletos com d(v) < B_new
        S = set()
        for v in graph.vertices():
            if v not in complete and dist[v] < B_new:
                S.add(v)

        B = B_new

    # converte dict -> lista ordenada por rótulo
    n = len(graph.vertices())
    result = [inf] * n
    for v, d in dist.items():
        result[v] = d
    return result

