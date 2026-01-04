import time
import math

from dijkstra import dijkstra, dijkstra_heap
from bmssp import run_bmssp
from graph import Graph

def build_graph(n, avg_degree=4, weighted=True, seed=None):
    g = Graph(directed=True)

    p = avg_degree / n

    g.random_init(
        num_vertices=n,
        edge_probability=p,
        weighted=weighted,
        seed=seed
    )

    # --- garantir conectividade ---
    visited = set()

    def dfs(u):
        visited.add(u)
        for v, _ in g.adj[u]:
            if v not in visited:
                dfs(v)

    dfs(0)

    last = 0
    for v in range(1, n):
        if v not in visited:
            g.add_edge(last, v, 1.0)
            dfs(v)
        last = v

    return g


def benchmark_once(graph, origin):
    t0 = time.time()
    d1 = dijkstra(graph.adj, origin)
    t1 = time.time()

    t2 = time.time()
    d2 = dijkstra_heap(graph.adj, origin)
    t3 = time.time()

    t4 = time.time()
    db = run_bmssp(graph, origin)
    t5 = time.time()

    ok = all(
        abs(a - b) < 1e-6
        for a, b in zip(d2, db)
    )

    return (
        t1 - t0,
        t3 - t2,
        t5 - t4,
        d1,
        d2,
        db,
        ok
    )


def main():
    sizes = [10, 100, 200]

    for n in sizes:
        print(f"\n=================== n = {n} ===================")

        for label, avg_deg in [
            ("ESPARSO", 4),
            ("DENSO", n // 2),
        ]:
            g = build_graph(n, avg_degree=avg_deg, weighted=True)

            origin = 0
            td, th, tb, d1, d2, db, ok = benchmark_once(g, origin)

            print(f"\n--- {label} --- (avg_degree={avg_deg})")
            print("Dijkstra simples:", round(td, 6))
            print("Heap Dijkstra:   ", round(th, 6))
            print("BMSSP:           ", round(tb, 6))
            print("Correção:", "OK ✅" if ok else "⚠️ Diferente")

            print("\n=== Resultados ===")
            print("Dijkstra simples:      ", d1)
            print("Dijkstra com heap:     ", d2)
            print("BMSSP:                 ", db)

if __name__ == "__main__":
    main()
