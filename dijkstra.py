import math
import heapq

from graph import Graph

def dijkstra (graph, origin):

    """
    
    Computes the shortest path distances from a source vertex to all other
    vertices using Dijkstra's algorithm without a priority queue.

    The algorithm repeatedly selects the non-visited vertex with the smallest
    tentative distance by scanning all vertices, then relaxes its outgoing
    edges.

    Parameters
    ----------
    graph : list[list[tuple[int, float]]]
        Adjacency list where graph[u] contains (v, weight) pairs.
        Edge weights must be non-negative.

    origin : int
        Source vertex index.

    Returns
    -------
    list[float]
        Shortest distance from the source to each vertex.

    Complexity
    ----------
    O(V^2 + E) time, O(V) space.

    """

    n = len(graph)
    dist = [math.inf] * n
    visited = [False] * n

    dist[origin] = 0

    for _ in range(n):
        # escolhe vértice não visitado com menor distância
        u = -1
        min_dist = math.inf
        for i in range(n):
            if not visited[i] and dist[i] < min_dist:
                min_dist = dist[i]
                u = i

        if u == -1:
            break  # não há mais vértices alcançáveis

        visited[u] = True

        # relaxamento
        for v, w in graph[u]:
            if not visited[v]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w

    return dist

def dijkstra_heap(graph, origin):

    """
    
    Computes the shortest path distances from a source vertex to all other
    vertices using Dijkstra's algorithm with a binary heap (priority queue).

    The heap allows efficient selection of the non-visited vertex with the
    smallest tentative distance, improving performance compared to the
    array-based implementation.

    Parameters
    ----------
    graph : list[list[tuple[int, float]]]
        Adjacency list where graph[u] contains (v, weight) pairs.
        Edge weights must be non-negative.

    origin : int
        Source vertex index.

    Returns
    -------
    list[float]
        Shortest distance from the source to each vertex.
        Unreachable vertices have distance infinity.

    Complexity
    ----------
    O((V + E) log V) time, O(V + E) space.

    """

    n = len(graph)
    dist = [math.inf] * n
    dist[origin] = 0

    visited = [False] * n

    # (distância, vértice)
    heap = [(0, origin)]

    while heap:
        current_dist, u = heapq.heappop(heap)

        # se já foi processado com menor distância, ignora
        if visited[u]:
            continue

        visited[u] = True

        for v, w in graph[u]:
            if not visited[v]:
                new_dist = current_dist + w
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    heapq.heappush(heap, (new_dist, v))

    return dist

if __name__ == "__main__":
    g = Graph()
    g.random_init(num_vertices=4, edge_probability=0.5, seed=4)
    print('Utilizando dijkstra padrão:')
    print(dijkstra(g.adj, 0))
    print('Utilizando dijkstra com heap binário:')
    print(dijkstra_heap(g.adj, 0))
