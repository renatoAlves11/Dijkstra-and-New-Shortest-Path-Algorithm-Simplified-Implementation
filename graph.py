import random
from collections import defaultdict
from typing import Any, Dict, List, Tuple


class Graph:
    """
    Graph represented by an adjacency list.
    Supports directed or undirected graphs, with optional edge weights.
    """

    def __init__(self, directed: bool = False):
        self.directed = directed
        self.adj: Dict[Any, List[Tuple[Any, float]]] = defaultdict(list)

    # ----------------------------
    # Basic structure operations
    # ----------------------------
    def add_vertex(self, v: Any) -> None:
        """Add a vertex to the graph."""
        if v not in self.adj:
            self.adj[v] = []

    def add_edge(self, u: Any, v: Any, weight: float = 1.0) -> None:
        """Add an edge u -> v with a given weight."""
        self.add_vertex(u)
        self.add_vertex(v)

        self.adj[u].append((v, weight))

        if not self.directed:
            self.adj[v].append((u, weight))

    def remove_edge(self, u: Any, v: Any) -> None:
        """Remove edge u -> v (and v -> u if undirected)."""
        self.adj[u] = [(x, w) for x, w in self.adj[u] if x != v]

        if not self.directed:
            self.adj[v] = [(x, w) for x, w in self.adj[v] if x != u]

    def remove_vertex(self, v: Any) -> None:
        """Remove a vertex and all associated edges."""
        if v in self.adj:
            del self.adj[v]

        for u in self.adj:
            self.adj[u] = [(x, w) for x, w in self.adj[u] if x != v]

    # ----------------------------
    # Query operations
    # ----------------------------
    def vertices(self) -> List[Any]:
        return list(self.adj.keys())

    def edges(self) -> List[Tuple[Any, Any, float]]:
        result = []
        for u, neighbors in self.adj.items():
            for v, w in neighbors:
                result.append((u, v, w))
        return result

    def neighbors(self, v: Any) -> List[Tuple[Any, float]]:
        return self.adj.get(v, [])

    def __len__(self) -> int:
        return len(self.adj)

    # ----------------------------
    # Random graph generation
    # ----------------------------
    def random_init(
        self,
        num_vertices: int,
        edge_probability: float = 0.2,
        weighted: bool = True,
        min_weight: float = 1.0,
        max_weight: float = 10.0,
        seed: int | None = None,
    ) -> None:
        """
        Initialize the graph randomly.

        :param num_vertices: number of vertices
        :param edge_probability: probability of an edge between any pair
        :param weighted: whether edges have random weights
        :param min_weight: minimum edge weight
        :param max_weight: maximum edge weight
        :param seed: random seed for reproducibility
        """
        if seed is not None:
            random.seed(seed)

        self.adj.clear()

        # create vertices
        for v in range(num_vertices):
            self.add_vertex(v)

        # create edges
        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                if random.random() <= edge_probability:
                    weight = (
                        random.uniform(min_weight, max_weight)
                        if weighted
                        else 1.0
                    )
                    self.add_edge(i, j, weight)

    # ----------------------------
    # Utility
    # ----------------------------
    def __str__(self) -> str:
        lines = []
        for v, neighbors in self.adj.items():
            lines.append(f"{v}: {neighbors}")
        return "\n".join(lines)


if __name__ == "__main__":
    # Example usage
    g = Graph(directed=False)
    g.random_init(num_vertices=5, edge_probability=0.5, seed=42)
    print(g)
