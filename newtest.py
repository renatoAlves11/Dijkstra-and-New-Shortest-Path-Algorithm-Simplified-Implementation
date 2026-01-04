import math
import time
import random

from graph import Graph
from dijkstra import dijkstra, dijkstra_heap
from bmssp import run_bmssp
from bmssp_simple import bmssp_simple


# --------------------------------------------------------
# utilitário — roda função repetidas vezes e tira média
# --------------------------------------------------------
def benchmark(fn, *args, repeats=3):
    t = 0.0
    result = None
    for _ in range(repeats):
        t0 = time.time()
        result = fn(*args)
        t += time.time() - t0
    return result, t / repeats


def build_graph(n, avg_degree=4, weighted=True, seed=None):
    g = Graph(directed=True)

    # 1️⃣ gera normalmente
    p = avg_degree / n
    g.random_init(
        num_vertices=n,
        edge_probability=p,
        weighted=weighted,
        seed=seed
    )

    # 2️⃣ garante conectividade (faz um spanning tree)
    visited = set()

    def dfs(u):
        visited.add(u)
        for v, _ in g.adj[u]:
            if v not in visited:
                dfs(v)

    dfs(0)

    # 3️⃣ conecta componentes desconexas
    last = 0
    for v in range(1, n):
        if v not in visited:
            # conecta v ao último alcançável
            g.add_edge(last, v, 1.0)
            dfs(v)
        last = v

    return g



def main():
    origin = 0

    # tamanhos crescentes
    sizes = [10, 100, 200, 500, 1000]

    # parâmetros BMSSP 
    L = 1000
    k = 1000
    t = 500

    # parâmetros BMSSP Simple
    w = 20
    p = 4

    for n in sizes:
        print(f"\n=================== n = {n} ===================")

        g = build_graph(n)

        # --------- DIJKSTRA (array) ----------
        dist_d1, td1 = benchmark(dijkstra, g.adj, origin)

        # --------- HEAP DIJKSTRA ----------
        dist_d2, td2 = benchmark(dijkstra_heap, g.adj, origin)

        # --------- BMSSP ----------
        dist_b, tb = benchmark(run_bmssp, g, origin, L, k, t)

        # --------- checagem ----------
        ok = True
        for a, b in zip(dist_d2, dist_b):
            if abs(a - b) > 1e-6:
                ok = False
                break

        print(f"Dijkstra simples: {round(td1, 6)} s")
        print(f"Dijkstra heap:   {round(td2, 6)} s")
        print(f"BMSSP:           {round(tb, 6)} s")
        print(f"BMSSP Simple:           {round(tb, 6)} s")
        print("Correção:", "OK ✅" if ok else "⚠️ Diferente")

        print("\n=== Resultados ===")
        print("Dijkstra simples:      ", dist_d1)
        print("Dijkstra com heap:     ", dist_d2)
        print("BMSSP:                 ", dist_b)


if __name__ == "__main__":
    main()
