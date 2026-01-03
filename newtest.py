import math
import time

from graph import Graph
from dijkstra import dijkstra, dijkstra_heap
from bmssp import run_bmssp


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


def build_graph(n, avg_degree=4, weighted=True):
    g = Graph(directed=True)

    # probabilidade para manter grau constante ~ paper
    p = avg_degree / n

    g.random_init(
        num_vertices=n,
        edge_probability=p,
        weighted=weighted,
        seed=None
    )
    return g


def main():
    origin = 0

    # tamanhos crescentes
    sizes = [200, 500, 1000, 3000, 6000]

    # parâmetros BMSSP (boas escolhas educacionais)
    L = 4
    k = 6
    t = 2

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
        print("Correção:", "OK ✅" if ok else "⚠️ Diferente")


if __name__ == "__main__":
    main()
