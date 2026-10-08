"""Undirected Curveball with a conditional finite-time marginal certificate.

The trade is the existing Curveball heat bath. The budget is a consequence
of the accepted family-131 gap premise, not a measured speed improvement.
"""

import math
import random


def _integer(value, name, minimum=0):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer at least {minimum}")
    return value


def prepare_graph(n, edges):
    """Return symmetric adjacency sets; reject invalid simple labeled graphs."""
    _integer(n, "n")
    adj = [set() for _ in range(n)]
    for edge in edges:
        try:
            u, v = edge
        except (TypeError, ValueError) as exc:
            raise ValueError("each edge must have exactly two endpoints") from exc
        _integer(u, "endpoint")
        _integer(v, "endpoint")
        if u >= n or v >= n:
            raise ValueError("endpoint outside the labeled vertex range")
        if u == v:
            raise ValueError("self-loops are forbidden")
        if v in adj[u]:
            raise ValueError("duplicate undirected edge")
        adj[u].add(v)
        adj[v].add(u)
    return adj


def _parameters(n, m, k):
    _integer(n, "n")
    _integer(m, "m")
    _integer(k, "k", 1)
    pairs = math.comb(n, 2)
    if m > pairs:
        raise ValueError("m exceeds the number of possible edges")
    universe = math.comb(pairs, m)
    bits = (universe - 1).bit_length()
    return pairs, universe, bits


def budget(n, m, k=7):
    """Integer number of trades sufficient for conditional TV <= 2**(-k).

    Every realization has m edges, so its universe has size at most
    U=comb(comb(n,2),m). Let B=ceil(log2(U)); the gap premise gives
    TV <= 1/2 sqrt(U) exp(-t/M). Since ln(2)<7/10, the integer
    ceiling of 7*M*(B+2*k-2)/20 is a sufficient budget.
    """
    pairs, universe, bits = _parameters(n, m, k)
    if n < 2 or universe == 1:
        return 0
    return (7 * pairs * (bits + 2 * k - 2) + 19) // 20


def trade(adj, rng):
    """Perform one uniform vertex-pair heat bath in place; return changed."""
    n = len(adj)
    if n < 2:
        return False
    u, v = rng.sample(range(n), 2)
    # The pair edge is held fixed, as are neighbors adjacent to both.
    left = adj[u] - adj[v] - {v}
    right = adj[v] - adj[u] - {u}
    if not left or not right:
        return False  # The fiber has a unique assignment.
    singleton = sorted(left | right)
    new_left = set(rng.sample(singleton, len(left)))
    departing = left - new_left
    arriving = new_left - left
    if not departing:
        return False
    for w in departing:
        adj[u].remove(w)
        adj[w].remove(u)
        adj[v].add(w)
        adj[w].add(v)
    for w in arriving:
        adj[v].remove(w)
        adj[w].remove(v)
        adj[u].add(w)
        adj[w].add(u)
    return True


def run_steps(adj, steps, rng):
    """Mutate adjacency through exactly steps trades; return changed count."""
    _integer(steps, "steps")
    changed = 0
    for _ in range(steps):
        changed += trade(adj, rng)
    return changed


def sample_graph(n, edges, k=7, seed=None):
    """Return one graph after the full conditional marginal-TV budget.

    Default randomness uses SystemRandom. A supplied seed selects Random
    only for reproducible experiments: a deterministic seeded output does
    not carry the ideal-random-bits distributional guarantee.
    """
    adj = prepare_graph(n, edges)
    m = sum(map(len, adj)) // 2
    pairs, universe, bits = _parameters(n, m, k)
    steps = budget(n, m, k)
    rng = random.SystemRandom() if seed is None else random.Random(seed)
    changed = run_steps(adj, steps, rng)
    final_edges = [[u, v] for u, neighbors in enumerate(adj)
                   for v in sorted(neighbors) if u < v]
    return {
        "edges": final_edges,
        "steps": steps,
        "changed_trades": changed,
        "certificate": {
            "conditional": True,
            "premise": "accepted family-131 Curveball gap >= 1/comb(n,2)",
            "source_commit": "fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb",
            "tv_bound": f"2^-{k}",
            "scope": "one output marginal; not joint independence",
            "randomness_required": "ideal independent uniform random choices",
            "randomness_mode": "SystemRandom" if seed is None else "seeded diagnostic Random",
            "seeded_diagnostic": seed is not None,
            "vertex_pairs": pairs,
            "edge_count": m,
            "universe_log2_ceiling": bits,
        },
    }
