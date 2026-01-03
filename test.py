import math
import time

from graph import Graph
from dijkstra import dijkstra, dijkstra_heap
from bmssp import run_bmssp

def main():
    # ------ cria grafo aleatório ------
    g = Graph()
    g.random_init(num_vertices=10, edge_probability=0.4, seed=7)

    origin = 0

    # --------- Dijkstra simples ----------
    t0 = time.time()
    dist_d1 = dijkstra(g.adj, origin)
    t1 = time.time()

    # --------- Dijkstra com heap ----------
    t2 = time.time()
    dist_d2 = dijkstra_heap(g.adj, origin)
    t3 = time.time()

    # --------- BMSSP ----------
    t4 = time.time()
    dist_b = run_bmssp(g, origin)
    t5 = time.time()

    print("\n=== Resultados ===")
    print("Dijkstra simples:      ", dist_d1)
    print("Dijkstra com heap:     ", dist_d2)
    print("BMSSP:                 ", dist_b)

    print("\n=== Tempos (segundos) ===")
    print("Dijkstra simples:", round(t1 - t0, 6))
    print("Heap Dijkstra:   ", round(t3 - t2, 6))
    print("BMSSP:           ", round(t5 - t4, 6))

    # --------- comparação ----------
    ok = True
    for a, b in zip(dist_d2, dist_b):
        if abs(a - b) > 1e-6:
            ok = False
            break

    print("\nCorreção BMSSP:", "OK ✅" if ok else "⚠️ Diferente do Dijkstra")


if __name__ == "__main__":
    main()
