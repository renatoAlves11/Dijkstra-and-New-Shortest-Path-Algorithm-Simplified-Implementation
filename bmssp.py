# bmssp.py
#
# Implementação educacional inspirada nos 3 algoritmos
# do paper "Breaking the Sorting Barrier for Directed Single-Source Shortest Paths"
#
# Componentes:
# 1. BaseCase (Algorithm 2)
# 2. FindPivots (Algorithm 1)
# 3. BMSSP (Algorithm 3)
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

    # pivôs = raízes com > k vértices
    P = set()
    for u in S:
        count = sum(1 for (a, b) in F if a == u or b == u)
        if count > k:
            P.add(u)

    return P, W


# ==========================================================
# Algorithm 3 — BMSSP(l, B, S)
# ==========================================================
def bmssp(graph: Graph, l, B, S, dist, t=2, k=2):
    # -------------------------
    # Caso base
    # -------------------------
    if l == 0:
        return base_case(graph, B, S, dist, k)

    # -------------------------
    # Encontrar pivôs
    # -------------------------
    P, W = find_pivots(graph, B, S, dist, k)

    # =====================================================
    # D = estrutura simplificada (D0 / D1)
    # D0  -> valores vindos de BatchPrepend (sempre menores)
    # D1  -> valores inseridos "normalmente"
    # =====================================================
    D0 = []        # heap menor-primeiro
    D1 = []

    # M = 2^{(l−1)t}
    M = 2 ** ((l - 1) * t)

    # inserir pivôs em D1
    for x in P:
        heapq.heappush(D1, (dist[x], {x}))

    # -------------------------
    # inicializações do paper
    # -------------------------
    U = set()
    i = 0
    B0 = min((dist[x] for x in P), default=B)

    # =====================================================
    # Função auxiliar: PULL()
    # =====================================================
    def pull():
        """Retorna até M itens com menores valores (misturando D0 e D1)."""
        batch = []

        while len(batch) < M and (D0 or D1):
            # compara topo de D0 e D1
            cands = []
            if D0:
                cands.append((D0[0][0], 0))
            if D1:
                cands.append((D1[0][0], 1))

            _, typ = min(cands)

            if typ == 0:
                batch.append(heapq.heappop(D0))
            else:
                batch.append(heapq.heappop(D1))

        if not (D0 or D1):
            sep = B
        else:
            # menor valor restante
            rest = []
            if D0:
                rest.append(D0[0][0])
            if D1:
                rest.append(D1[0][0])
            sep = min(rest)

        Skeys = set(s for _, Sset in batch for s in Sset)
        return sep, Skeys, batch

    # =====================================================
    # LOOP PRINCIPAL
    # =====================================================
    while len(U) < k * (2 ** (l * t)) and (D0 or D1):

        i += 1
        Bi, Si, pulled = pull()

        # chamada recursiva
        Bp, Ui = bmssp(graph, l - 1, Bi, Si, dist, t, k)

        U |= Ui
        B0 = min(B0, Bp)

        K = []     # itens que ficarão na faixa intermediária

        # relaxação sobre arestas saindo de Ui
        for u in Ui:
            for v, w in graph.adj[u]:
                nd = dist[u] + w

                if nd <= dist[v]:
                    dist[v] = nd

                    # -----------------------------
                    # Faixa 1: [Bi , B)
                    # vai para D1 (Insert)
                    # -----------------------------
                    if Bi <= nd < B:
                        heapq.heappush(D1, (nd, {v}))

                    # -----------------------------
                    # Faixa 2: [Bp , Bi)
                    # acumula em K (BatchPrepend)
                    # -----------------------------
                    elif Bp <= nd < Bi:
                        K.append((nd, {v}))

        # batch prepend = insere tudo em D0 como "menor do mundo"
        for item in K:
            heapq.heappush(D0, item)

        # também batch-prepend todas as fontes originais de Si na faixa
        for x in Si:
            dx = dist[x]
            if Bp <= dx < Bi:
                heapq.heappush(D0, (dx, {x}))

    # -------------------------
    # FECHAMENTO
    # -------------------------
    U |= {x for x in W if dist[x] < B0}

    return B0, U



# ==========================================================
# Wrapper externo — que roda BMSSP completo
# ==========================================================
def run_bmssp(graph: Graph, source, L=2, k=2, t=2):
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

