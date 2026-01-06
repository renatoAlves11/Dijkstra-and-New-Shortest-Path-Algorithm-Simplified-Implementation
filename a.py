import matplotlib.pyplot as plt

import time
import math

from dijkstra import dijkstra, dijkstra_heap
from bmssp import run_bmssp
from graph import Graph

def build_graph(n, avg_degree=4, weighted=True, seed=2):
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

    ok = len(d2) == len(db) and all(abs(a - b) < 1e-6 for a, b in zip(d2, db))

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
    sizes = [10, 50, 100, 200, 400, 800]

    results_sparse = []
    results_dense  = []

    for n in sizes:
        print(f"\n=================== n = {n} ===================")

        for label, avg_deg, store in [
            ("ESPARSO", 4, results_sparse),
            ("DENSO", n // 2, results_dense),
        ]:
            g = build_graph(n, avg_degree=avg_deg, weighted=True)

            td, th, tb, d1, d2, db, ok = benchmark_once(g, 0)

            print(f"\n--- {label} ---")
            print("Dijkstra simples:", round(td, 6))
            print("Heap Dijkstra:   ", round(th, 6))
            print("BMSSP:           ", round(tb, 6))
            print("Correção:", "OK ✅" if ok else "⚠️ Diferente")

            print("\n=== Resultados ===")
            print("Dijkstra simples:      ", d1)
            print("Dijkstra com heap:     ", d2)
            print("BMSSP:                 ", db)

            # salvar para o gráfico
            store.append((n, td, th, tb))

    # ---- GRÁFICOS ----
    plot_results("Grafos Esparsos", results_sparse)
    plot_results("Grafos Densos",  results_dense)


def plot_results(title, data):
    ns  = [x[0] for x in data]
    td  = [x[1] for x in data]
    th  = [x[2] for x in data]
    tb  = [x[3] for x in data]

    plt.figure()
    plt.plot(ns, td, label="Dijkstra simples")
    plt.plot(ns, th, label="Dijkstra heap")
    plt.plot(ns, tb, label="BMSSP")
    plt.xlabel("Número de vértices (n)")
    plt.ylabel("Tempo (s)")
    plt.title(title)
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    main()
