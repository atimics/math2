"""Independent, standard-library checker for labeled cycle double covers.

A label describes an even subgraph (possibly disconnected or empty). Each
edge belongs to exactly two distinct labels. No solver code is imported.
"""

import argparse
import json
from collections import deque


def _integer(value, name, minimum):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def _graph(data, name):
    if not isinstance(data, dict):
        raise ValueError(f"{name} must be an object")
    n = _integer(data.get("vertex_count"), f"{name}.vertex_count", 1)
    raw = data.get("edges")
    if not isinstance(raw, list):
        raise ValueError(f"{name}.edges must be a list")
    edges = []
    seen = set()
    adjacency = [[] for _ in range(n)]
    for i, edge in enumerate(raw):
        if not isinstance(edge, (list, tuple)) or len(edge) != 2:
            raise ValueError(f"{name}.edges[{i}] must have two endpoints")
        u, v = edge
        _integer(u, f"{name}.edges[{i}][0]", 0)
        _integer(v, f"{name}.edges[{i}][1]", 0)
        if u >= n or v >= n or u == v:
            raise ValueError(f"{name}.edges[{i}] has invalid endpoints")
        key = (min(u, v), max(u, v))
        if key in seen:
            raise ValueError(f"{name} contains duplicate edges")
        seen.add(key)
        edges.append(key)
        adjacency[u].append(v)
        adjacency[v].append(u)
    if any(len(neighbors) != 3 for neighbors in adjacency):
        raise ValueError(f"{name} must be cubic")
    reached = {0}
    pending = deque([0])
    while pending:
        u = pending.popleft()
        for v in adjacency[u]:
            if v not in reached:
                reached.add(v)
                pending.append(v)
    if len(reached) != n:
        raise ValueError(f"{name} must be connected")
    # Iterative low-link traversal avoids recursion limits for large inputs.
    arrival = [-1] * n
    low = [-1] * n
    parent = [-1] * n
    arrival[0] = low[0] = 0
    clock = 1
    stack = [(0, iter(adjacency[0]))]
    while stack:
        u, neighbors = stack[-1]
        v = next(neighbors, None)
        if v is None:
            stack.pop()
            if parent[u] != -1:
                p = parent[u]
                if low[u] > arrival[p]:
                    raise ValueError(f"{name} contains a bridge")
                low[p] = min(low[p], low[u])
        elif arrival[v] == -1:
            parent[v] = u
            arrival[v] = low[v] = clock
            clock += 1
            stack.append((v, iter(adjacency[v])))
        elif v != parent[u]:
            low[u] = min(low[u], arrival[v])
    return n, edges


def verify_cover(graph, witness):
    """Raise ValueError on invalid input; return counts for a valid cover.

    Graphs are simple, connected, bridgeless and cubic. Witness edge order and
    orientation may differ from graph order; pairs align with witness edges.
    Label indices are zero-based. Empty labels are allowed, so ``labels`` is
    an upper bound on the number of nonempty covering even subgraphs.
    """
    n, edges = _graph(graph, "graph")
    wn, witness_edges = _graph(witness, "witness")
    if wn != n or set(witness_edges) != set(edges):
        raise ValueError("witness graph does not match graph")
    k = _integer(witness.get("labels"), "witness.labels", 2)
    pairs = witness.get("pairs")
    if not isinstance(pairs, list) or len(pairs) != len(witness_edges):
        raise ValueError("witness.pairs must contain one pair per edge")
    # Sparse counts avoid allocation proportional to an untrusted label count.
    degree = {}
    counts = {}
    for i, ((u, v), pair) in enumerate(zip(witness_edges, pairs)):
        if not isinstance(pair, (list, tuple)) or len(pair) != 2:
            raise ValueError(f"witness.pairs[{i}] must have two labels")
        a, b = pair
        _integer(a, f"witness.pairs[{i}][0]", 0)
        _integer(b, f"witness.pairs[{i}][1]", 0)
        if a >= k or b >= k or a == b:
            raise ValueError(f"witness.pairs[{i}] has invalid labels")
        for label in pair:
            counts[label] = counts.get(label, 0) + 1
            for vertex in (u, v):
                key = (vertex, label)
                degree[key] = degree.get(key, 0) + 1
    for (vertex, label), count in degree.items():
        if count % 2:
            raise ValueError(f"label {label} has odd degree at vertex {vertex}")
    return {
        "vertices": n,
        "edges": len(edges),
        "labels": k,
        "used_labels": len(counts),
        "label_edge_counts": {str(label): count for label, count in sorted(counts.items())},
    }


def verify_palette_clique(witness, clique_labels, k):
    """Check a clique certificate against global palette coarsening to k labels.

    Every pair of clique labels occurs together on an edge, so no two can
    receive the same new label. This forbids only global label merging of
    this particular witness, not an unrestricted k-cover of its graph.
    """
    verify_cover(witness, witness)
    _integer(k, "k", 1)
    if not isinstance(clique_labels, (list, tuple)):
        raise ValueError("clique_labels must be a list of distinct label indices")
    labels = witness["labels"]
    for label in clique_labels:
        _integer(label, "clique label", 0)
        if label >= labels:
            raise ValueError("clique label outside witness palette")
    if len(set(clique_labels)) != len(clique_labels):
        raise ValueError("clique labels must be distinct")
    if len(clique_labels) <= k:
        raise ValueError("clique size must exceed the target palette size")
    interaction = {tuple(sorted(pair)) for pair in witness["pairs"]}
    ordered = sorted(clique_labels)
    for i, a in enumerate(ordered):
        for b in ordered[i + 1:]:
            if (a, b) not in interaction:
                raise ValueError(f"missing clique interaction pair {a}, {b}")
    return {
        "restriction": "global_palette_coarsening",
        "target_labels": k,
        "clique_labels": ordered,
        "clique_size": len(ordered),
        "checked_pairs": len(ordered) * (len(ordered) - 1) // 2,
        "unrestricted_impossibility_claim": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph", help="graph JSON file")
    parser.add_argument("witness", help="cover witness JSON file")
    args = parser.parse_args()
    try:
        with open(args.graph, encoding="utf-8") as stream:
            graph = json.load(stream)
        with open(args.witness, encoding="utf-8") as stream:
            witness = json.load(stream)
        print(json.dumps(verify_cover(graph, witness), sort_keys=True))
    except (ValueError, OSError) as error:
        parser.exit(1, f"invalid cover: {error}\n")


if __name__ == "__main__":
    main()
