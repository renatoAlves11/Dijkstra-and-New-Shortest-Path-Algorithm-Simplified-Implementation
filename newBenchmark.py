import matplotlib.pyplot as plt

import time
import math

from dijkstra import dijkstra, dijkstra_heap
from bmssp import run_bmssp
from graph import Graph

def build_sparse_graph(n, seed=3):
    g = Graph(directed=True)
    g.random_sparse_init(
        num_vertices=n,
        max_edges_per_vertex=3,
        weighted=True,
        seed=seed
    )
    return g


def build_dense_graph(n, seed=3):
    g = Graph(directed=True)
    g.random_dense_init(
        num_vertices=n,
        edge_probability=0.6,
        weighted=True,
        seed=seed
    )
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

        # --------- ESPARSO ----------
        g = build_sparse_graph(n)

        td, th, tb, d1, d2, db, ok = benchmark_once(g, 0)

        print(f"\n--- [ESPARSO] ---")
        print("Dijkstra simples:", round(td, 6))
        print("Heap Dijkstra:   ", round(th, 6))
        print("BMSSP:           ", round(tb, 6))
        print("Correção:", "OK ✅" if ok else "⚠️ Diferente")

        # salvar para o gráfico
        results_sparse.append((n, td, th, tb))

        # --------- ESPARSO ----------
        g = build_dense_graph(n)

        td, th, tb, d1, d2, db, ok = benchmark_once(g, 0)

        print(f"\n--- [DENSO] ---")
        print("Dijkstra simples:", round(td, 6))
        print("Heap Dijkstra:   ", round(th, 6))
        print("BMSSP:           ", round(tb, 6))
        print("Correção:", "OK ✅" if ok else "⚠️ Diferente")

        # salvar para o gráfico
        results_dense.append((n, td, th, tb))

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
