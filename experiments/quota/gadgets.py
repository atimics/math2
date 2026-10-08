"""Exact degree-quota reductions to simple perfect-matching instances.

Source: openai/math@fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb,
preprints/Almost-Linear-Time-Maximum-Cardinality-Matching-in-Sparse-General-Graphs-
September-24-2026/build/sections/{09-uniformization,10-f-factors}.tex.
The dense mode is the classical incidence gadget; network mode substitutes
the paper's recursive Beneš network. Hybrid chooses the smaller local V+E.
No specialized zero/full-quota gadgets are used in any mode.
"""


def _integer(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _edge(u, v):
    return (u, v) if u < v else (v, u)


def reduce_graph(n, edges, quotas, mode="dense"):
    """Return a matching graph and a cross-edge decoder for an f-factor.

    Vertices in the input are 0..n-1; quotas has one integer per vertex.
    choices contains 'dense', 'network', or 'isolated' for each host vertex.
    """
    if not _integer(n) or n < 0:
        raise ValueError("n must be a nonnegative integer")
    if mode not in ("dense", "network", "hybrid"):
        raise ValueError("mode must be dense, network, or hybrid")
    quotas = list(quotas)
    if len(quotas) != n or any(not _integer(q) for q in quotas):
        raise ValueError("quotas must contain one integer per vertex")
    host_edges = []
    seen = set()
    incidences = [[] for _ in range(n)]
    for pair in edges:
        try:
            u, v = pair
        except (TypeError, ValueError) as exc:
            raise ValueError("every edge must have two endpoints") from exc
        if not _integer(u) or not _integer(v) or not (0 <= u < n and 0 <= v < n) or u == v:
            raise ValueError("edges must have distinct valid integer endpoints")
        e = _edge(u, v)
        if e in seen:
            raise ValueError("parallel edges are not supported")
        seen.add(e)
        host_edges.append(e)
    host_edges.sort()
    for i, (u, v) in enumerate(host_edges):
        incidences[u].append(i)
        incidences[v].append(i)
    if any(q < 0 or q > len(incidences[v]) for v, q in enumerate(quotas)):
        raise ValueError("quota must lie between zero and host degree")

    graph_edges = []
    vertex_count = 0

    def vertex():
        nonlocal vertex_count
        result = vertex_count
        vertex_count += 1
        return result

    def add(u, v):
        graph_edges.append(_edge(u, v))

    def position():
        p = (vertex(), vertex())
        add(*p)  # idle edge
        return p

    def network(s):
        if s == 1:
            p = position()
            return [p], [p]
        inputs = [position() for _ in range(s)]
        outputs = [position() for _ in range(s)]
        upper_in, upper_out = network(s // 2)
        lower_in, lower_out = network(s // 2)
        for i in range(s // 2):
            for outer in inputs[2 * i:2 * i + 2]:
                add(outer[1], upper_in[i][0])
                add(outer[1], lower_in[i][0])
            for outer in outputs[2 * i:2 * i + 2]:
                add(upper_out[i][1], outer[0])
                add(lower_out[i][1], outer[0])
        return inputs, outputs

    ports = [{} for _ in range(n)]
    for v in range(n):
        for i in incidences[v]:
            ports[v][i] = vertex()
    cross_edges = {}
    for i, (u, v) in enumerate(host_edges):
        e = _edge(ports[u][i], ports[v][i])
        add(*e)
        cross_edges[e] = (u, v)
    choices = []
    for v in range(n):
        d = len(incidences[v])
        if d == 0:
            choices.append("isolated")
            continue
        b = d - quotas[v]
        s = 1 << (d - 1).bit_length()
        depth = s.bit_length() - 1
        positions = s * (1 + 2 * depth)
        arcs = 4 * s * depth
        # Counts include local ports; cross edges are common to both choices.
        dense_size = (d + b) + d * b
        network_size = (d + 2 * positions + b) + positions + arcs + d + b
        choice = mode
        if mode == "hybrid":
            choice = "network" if network_size < dense_size else "dense"
        choices.append(choice)
        if choice == "dense":
            sinks = [vertex() for _ in range(b)]
            for p in ports[v].values():
                for sink in sinks:
                    add(p, sink)
        else:
            inputs, outputs = network(s)
            for j, i in enumerate(incidences[v]):
                add(ports[v][i], inputs[j][0])
            for j in range(b):
                add(outputs[j][1], vertex())
    return {"vertex_count": vertex_count, "edges": graph_edges,
            "cross_edges": cross_edges, "choices": choices}


def decode_matching(reduction, matching):
    """Validate a complete gadget perfect matching and decode host edges.

    This checks gadget validity; an independent host quota verifier should
    also check the returned witness against the original input.
    """
    n = reduction["vertex_count"]
    allowed = set(reduction["edges"])
    covered = set()
    decoded = []
    for pair in matching:
        try:
            u, v = pair
        except (TypeError, ValueError) as exc:
            raise ValueError("matching edges must have two endpoints") from exc
        if not _integer(u) or not _integer(v) or not (0 <= u < n and 0 <= v < n) or u == v:
            raise ValueError("matching has invalid endpoints")
        e = _edge(u, v)
        if e not in allowed or u in covered or v in covered:
            raise ValueError("matching uses an absent edge or repeated vertex")
        covered.update(e)
        if e in reduction["cross_edges"]:
            decoded.append(reduction["cross_edges"][e])
    if len(covered) != n:
        raise ValueError("matching does not cover all gadget vertices")
    return sorted(decoded)
