"""Small, deterministic simple cubic graph fixtures (no third-party dependencies)."""
from __future__ import annotations


def make_graph(name: str, vertex_count: int, edges) -> dict:
    """Canonicalize a graph and reject malformed, noncubic or bridged inputs."""
    graph = {"name": name, "vertex_count": vertex_count,
             "edges": sorted([sorted(edge) for edge in edges])}
    validate_graph(graph)
    return graph


def validate_graph(graph: dict) -> None:
    """Raise ValueError unless the graph is simple, connected, cubic, bridgeless."""
    n = graph.get("vertex_count")
    if type(n) is not int or n < 4:
        raise ValueError("vertex_count must be an integer at least four")
    edges = graph.get("edges")
    if not isinstance(edges, list):
        raise ValueError("edges must be a list")
    adjacent = [[] for _ in range(n)]
    seen = set()
    for i, edge in enumerate(edges):
        if not isinstance(edge, (list, tuple)) or len(edge) != 2:
            raise ValueError("each edge must have two endpoints")
        u, v = edge
        if type(u) is not int or type(v) is not int or not 0 <= u < v < n:
            raise ValueError("endpoints must be ordered distinct integers in range")
        if (u, v) in seen:
            raise ValueError("parallel edges are not supported")
        seen.add((u, v))
        adjacent[u].append((v, i))
        adjacent[v].append((u, i))
    if any(len(neighbors) != 3 for neighbors in adjacent):
        raise ValueError("graph must be cubic")
    # Tarjan low links distinguish connectivity and bridges in one traversal.
    discovery = [-1] * n
    low = [0] * n
    clock = 0
    bridges = []

    def visit(u, parent_edge=-1):
        nonlocal clock
        discovery[u] = low[u] = clock
        clock += 1
        for v, edge_id in adjacent[u]:
            if edge_id == parent_edge:
                continue
            if discovery[v] == -1:
                visit(v, edge_id)
                low[u] = min(low[u], low[v])
                if low[v] > discovery[u]:
                    bridges.append(edge_id)
            else:
                low[u] = min(low[u], discovery[v])

    visit(0)
    if -1 in discovery:
        raise ValueError("graph must be connected")
    if bridges:
        raise ValueError("graph must be bridgeless")


def generalized_petersen(n: int, k: int) -> dict:
    """Return G(n,k), with outer vertices 0..n-1 and inner vertices n..2n-1."""
    if type(n) is not int or type(k) is not int or n < 3 or not 1 <= k < n / 2:
        raise ValueError("require n >= 3 and 1 <= k < n/2")
    edges = {(min(i, (i + 1) % n), max(i, (i + 1) % n)) for i in range(n)}
    edges.update((i, n + i) for i in range(n))
    edges.update((n + min(i, (i + k) % n), n + max(i, (i + k) % n))
                 for i in range(n))
    return make_graph(f"generalized-petersen-{n}-{k}", 2 * n, edges)


def fixtures() -> list[dict]:
    """K4, K3,3, cube, Petersen and triangular prism, in that order."""
    return [
        make_graph("k4", 4, [(u, v) for u in range(4) for v in range(u + 1, 4)]),
        make_graph("k3-3", 6, [(u, v) for u in range(3) for v in range(3, 6)]),
        make_graph("cube", 8, [(u, u ^ (1 << bit)) for u in range(8)
                               for bit in range(3) if u < (u ^ (1 << bit))]),
        dict(generalized_petersen(5, 2), name="petersen"),
        dict(generalized_petersen(3, 1), name="triangular-prism"),
    ]


def seeded_simple_cubic(vertex_count: int, seed: int, max_attempts: int = 1000) -> dict:
    """Sample a reproducible simple connected bridgeless cubic graph.

    Shuffle three stubs per vertex using a local Random(seed), pair adjacent
    stubs, and reject loops, repeated edges, disconnected graphs and bridges.
    This is bounded rejection sampling, not a guarantee of finding a graph.
    """
    import random
    if type(vertex_count) is not int or vertex_count < 4 or vertex_count % 2:
        raise ValueError("vertex_count must be an even integer at least four")
    if type(seed) is not int:
        raise ValueError("seed must be an integer")
    if type(max_attempts) is not int or max_attempts < 1:
        raise ValueError("max_attempts must be a positive integer")
    rng = random.Random(seed)
    for attempt in range(1, max_attempts + 1):
        stubs = [vertex for vertex in range(vertex_count) for _ in range(3)]
        rng.shuffle(stubs)
        edges = [sorted(stubs[i:i + 2]) for i in range(0, len(stubs), 2)]
        try:
            graph = make_graph(f"seeded-cubic-{vertex_count}-{seed}", vertex_count, edges)
        except ValueError:
            continue
        graph.update(seed=seed, generation_attempt=attempt)
        return graph
    raise RuntimeError("seeded cubic rejection sampler exhausted max_attempts")
