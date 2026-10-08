"""Bounded searches for Eulerian cycle-double-cover witnesses.

Each edge belongs to two distinct labels.  Each label's edge set has even
degree at every vertex.  MILP solver conclusions are not proof certificates.
Restricted compression only merges labels; it cannot change an edge's pair.
"""

from itertools import combinations
from math import isfinite


def _graph(graph):
    n = graph["vertex_count"]
    if type(n) is not int or n < 0:
        raise ValueError("vertex_count must be a nonnegative integer")
    edges = []
    for edge in graph["edges"]:
        if len(edge) != 2:
            raise ValueError("edges must have two endpoints")
        u, v = edge
        if any(type(x) is not int or not 0 <= x < n for x in (u, v)):
            raise ValueError("edge endpoint outside vertex range")
        if u == v:
            raise ValueError("loops are not supported")
        edges.append([u, v])
    return n, edges


def _checked_witness(witness):
    n, edges = _graph(witness)
    labels = witness["labels"]
    if type(labels) is not int or labels < 1:
        raise ValueError("labels must be a positive integer")
    pairs = witness["pairs"]
    if len(pairs) != len(edges):
        raise ValueError("one label pair is required per edge")
    parity = [[0] * labels for _ in range(n)]
    for (u, v), pair in zip(edges, pairs):
        if len(pair) != 2:
            raise ValueError("each edge must have two distinct labels")
        a, b = pair
        if a == b or any(type(x) is not int or not 0 <= x < labels for x in pair):
            raise ValueError("invalid label pair")
        for label in pair:
            parity[u][label] ^= 1
            parity[v][label] ^= 1
    if any(any(row) for row in parity):
        raise ValueError("a label has odd degree at a vertex")
    return n, edges, labels, pairs


def solve_cover(graph, k, time_limit=10.0):
    """Search all pair assignments with at most k Eulerian labels.

    Binary x[e,{a,b}] selects exactly one pair for each edge.  For each
    vertex v and label a, its incident membership sum equals 2*z[v,a],
    where z is an integer.  This encodes exact double coverage and parity.
    """
    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint, milp
    from scipy.sparse import coo_matrix

    n, edges = _graph(graph)
    if type(k) is not int or k < 1:
        raise ValueError("k must be a positive integer")
    if not isfinite(time_limit) or time_limit <= 0:
        raise ValueError("time_limit must be finite and positive")
    metadata = {"method": "scipy.optimize.milp", "k": k,
                "time_limit": time_limit, "proof_certified_unsat": False}
    if not edges:
        return {"status": "found", "witness": {
            "vertex_count": n, "edges": [], "labels": k, "pairs": []},
            "metadata": metadata}
    if k == 1:
        # A nonempty edge cannot have two distinct memberships in one label.
        metadata.update(reason="nonempty graph needs two distinct labels",
                        proof_certified_unsat=True)
        return {"status": "infeasible", "witness": None, "metadata": metadata}
    palette_pairs = list(combinations(range(k), 2))
    p = len(palette_pairs)
    m = len(edges)
    binary_count = m * p
    variable_count = binary_count + n * k
    row_count = m + n * k
    rows, cols, data = [], [], []
    degree = [0] * n
    for e, (u, v) in enumerate(edges):
        degree[u] += 1
        degree[v] += 1
        for j, pair in enumerate(palette_pairs):
            column = e * p + j
            rows.append(e)
            cols.append(column)
            data.append(1.0)
            for vertex in (u, v):
                for label in pair:
                    rows.append(m + vertex * k + label)
                    cols.append(column)
                    data.append(1.0)
    for vertex in range(n):
        for label in range(k):
            rows.append(m + vertex * k + label)
            cols.append(binary_count + vertex * k + label)
            data.append(-2.0)
    matrix = coo_matrix((data, (rows, cols)),
                        shape=(row_count, variable_count)).tocsc()
    target = np.zeros(row_count)
    target[:m] = 1
    upper = np.ones(variable_count)
    for vertex in range(n):
        upper[binary_count + vertex * k:binary_count + (vertex + 1) * k] = degree[vertex] // 2
    try:
        result = milp(
            c=np.zeros(variable_count),
            integrality=np.ones(variable_count, dtype=np.uint8),
            bounds=Bounds(np.zeros(variable_count), upper),
            constraints=LinearConstraint(matrix, target, target),
            options={"time_limit": float(time_limit)},
        )
    except Exception as exc:
        metadata["message"] = str(exc)
        return {"status": "error", "witness": None, "metadata": metadata}
    metadata.update(solver_status=int(result.status), message=str(result.message))
    if result.x is not None:
        assignments = result.x[:binary_count].reshape(m, p)
        chosen = []
        for values in assignments:
            selected = [j for j, value in enumerate(values) if value > 0.5]
            if len(selected) != 1:
                break
            chosen.append(list(palette_pairs[selected[0]]))
        if len(chosen) == m:
            witness = {"vertex_count": n, "edges": edges, "labels": k,
                       "pairs": chosen}
            try:
                _checked_witness(witness)
            except ValueError:
                pass
            else:
                metadata["integer_witness_checked"] = True
                return {"status": "found", "witness": witness, "metadata": metadata}
    status = {1: "timeout", 2: "infeasible"}.get(result.status, "error")
    if result.status == 0:
        metadata["message"] += "; no valid integer witness could be extracted"
    return {"status": status, "witness": None, "metadata": metadata}


def compress_cover(witness, k, node_limit=100000):
    """Try label merging by a bounded exact coloring of the interaction graph.

    Two old labels are adjacent if they occur together on some edge.  A
    proper k-coloring merges them without collapsing either membership.
    Failure after exhausting this search concerns this witness and this
    restricted operation only; it says nothing about unrestricted k-CDCs.
    """
    n, edges, labels, pairs = _checked_witness(witness)
    if type(k) is not int or k < 1:
        raise ValueError("k must be a positive integer")
    if type(node_limit) is not int or node_limit < 1:
        raise ValueError("node_limit must be a positive integer")
    adjacency = [set() for _ in range(labels)]
    for a, b in pairs:
        adjacency[a].add(b)
        adjacency[b].add(a)
    colors = [-1] * labels
    nodes = 0
    limit_hit = False

    def search(used):
        nonlocal nodes, limit_hit
        if nodes >= node_limit:
            limit_hit = True
            return False
        nodes += 1
        remaining = [v for v in range(labels) if colors[v] < 0]
        if not remaining:
            return True
        vertex = max(remaining, key=lambda v: (
            len({colors[w] for w in adjacency[v] if colors[w] >= 0}),
            len(adjacency[v]), -v))
        forbidden = {colors[w] for w in adjacency[vertex] if colors[w] >= 0}
        # Color permutations are symmetric: introduce only the next color.
        for color in range(min(k, used + 1)):
            if color in forbidden:
                continue
            colors[vertex] = color
            if search(max(used, color + 1)):
                return True
            colors[vertex] = -1
            if limit_hit:
                return False
        return False

    found = search(0)
    metadata = {"method": "interaction_graph_coloring", "k": k,
                "nodes": nodes, "node_limit": node_limit,
                "exhaustive_restricted_search": not found and not limit_hit,
                "unrestricted_impossibility_claim": False}
    if found:
        compressed = {"vertex_count": n, "edges": edges, "labels": k,
                      "pairs": [[colors[a], colors[b]] for a, b in pairs]}
        _checked_witness(compressed)
        metadata["label_map"] = colors[:]
        return {"status": "compressed", "witness": compressed, "metadata": metadata}
    return {"status": "node_limit" if limit_hit else "impossible",
            "witness": None, "metadata": metadata}
