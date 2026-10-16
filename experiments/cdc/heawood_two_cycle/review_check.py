"""Independent structural check of the pinned two-cycle impossibility.

Standard library only; no discovery or predecessor-checker imports.  This
checks a rank obstruction, not the discovery palette-chromatic histogram.
Alexander Richard Towell, with substantial OpenAI Codex assistance.
Separately authored AI review; not human review or proof-assistant verification.
"""

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


SOURCE_SHA256 = "fb8503f1cc92725d9981dd3320e2556fa1dcf74a0ade94f77cca04c88cf5b98f"
DEFAULT_SOURCE = Path(__file__).resolve().parent.parent / "heawood" / "certificate.json"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(items):
    result = {}
    for key, value in items:
        require(key not in result, "duplicate JSON object key")
        result[key] = value
    return result


def incidence(vertex_count, edges):
    require(type(vertex_count) is int and vertex_count > 0, "invalid vertex count")
    require(isinstance(edges, (list, tuple)), "invalid edge list")
    rows = [[] for _ in range(vertex_count)]
    seen = set()
    for index, edge in enumerate(edges):
        require(isinstance(edge, (list, tuple)) and len(edge) == 2, "invalid edge")
        u, v = edge
        require(type(u) is int and type(v) is int and 0 <= u < v < vertex_count,
                "invalid ordered edge endpoints")
        require((u, v) not in seen, "duplicate edge")
        seen.add((u, v))
        rows[u].append(index)
        rows[v].append(index)
    return rows


def components(vertex_count, edges, support):
    """Return the edge sets of all nonempty components of a support."""
    neighbors = [[] for _ in range(vertex_count)]
    for e in support:
        u, v = edges[e]
        neighbors[u].append((v, e))
        neighbors[v].append((u, e))
    unseen = {v for v, row in enumerate(neighbors) if row}
    result = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        pending, found = [root], set()
        while pending:
            u = pending.pop()
            for v, e in neighbors[u]:
                found.add(e)
                if v in unseen:
                    unseen.remove(v)
                    pending.append(v)
        result.append(tuple(sorted(found)))
    return tuple(sorted(result))


def cycle_space(vertex_count, edges):
    """Enumerate all even supports by arbitrary chord bits, then filter cycles.

    Tree edges are determined uniquely from leaves to the root by even parity.
    This is independent of the discovery implementation's cycle DFS.
    """
    rows = incidence(vertex_count, edges)
    require(all(len(row) == 3 for row in rows), "source graph is not cubic")
    parent = {0: None}
    order = [0]
    for u in order:
        for e in rows[u]:
            a, b = edges[e]
            v = b if a == u else a
            if v not in parent:
                parent[v] = (u, e)
                order.append(v)
    require(len(order) == vertex_count, "source graph is disconnected")
    tree_edges = {parent[v][1] for v in order[1:]}
    chords = [e for e in range(len(edges)) if e not in tree_edges]
    even_supports, cycles = [], []
    for assignment in range(1 << len(chords)):
        selected = {e for i, e in enumerate(chords) if assignment & (1 << i)}
        for v in reversed(order[1:]):
            _, parent_edge = parent[v]
            if sum(e in selected for e in rows[v]) % 2:
                selected.add(parent_edge)
        require(all(sum(e in selected for e in row) % 2 == 0 for row in rows),
                "cycle-space reconstruction violated even parity")
        support = tuple(sorted(selected))
        even_supports.append(support)
        if support and len(components(vertex_count, edges, support)) == 1:
            # Cubicity plus even parity gives degree two at every active vertex.
            cycles.append(support)
    require(len(set(even_supports)) == len(even_supports), "repeated even support")
    return (tuple(sorted(even_supports, key=lambda c: (len(c), c))),
            tuple(sorted(cycles, key=lambda c: (len(c), c))))


def perfect_matchings(vertex_count, edges):
    """Exhaust all perfect matchings by matching the least unmatched vertex."""
    rows = incidence(vertex_count, edges)
    result = []

    def visit(unmatched, selected):
        if not unmatched:
            result.append(tuple(sorted(selected)))
            return
        u = min(unmatched)
        for e in rows[u]:
            a, b = edges[e]
            v = b if a == u else a
            if v in unmatched:
                visit(unmatched - {u, v}, selected + (e,))

    visit(set(range(vertex_count)), ())
    require(len(result) == len(set(result)), "repeated perfect matching")
    return tuple(sorted(result))


def parity(functional, value):
    return (functional & value).bit_count() % 2


def validate_flow(vertex_count, edges, flow):
    rows = incidence(vertex_count, edges)
    require(all(len(row) == 3 for row in rows), "flow graph is not cubic")
    require(isinstance(flow, (list, tuple)) and len(flow) == len(edges), "invalid flow length")
    require(all(type(value) is int and 1 <= value <= 7 for value in flow),
            "flow is not nowhere-zero over F2^3")
    require(all(flow[a] ^ flow[b] ^ flow[c] == 0 for a, b, c in rows),
            "flow is not conservative")


def projection_barriers(vertex_count, edges, flow, cycles):
    """Check the obstruction after each legal first move, for every functional.

    A second move can kill a nonzero projection only if its simple cycle is
    exactly the projection support and its delta has functional value one.
    Such a delta is illegal when every vector in that affine half-space
    already occurs on the support.  All checks are explicit under Python -O.
    """
    validate_flow(vertex_count, edges, flow)
    require(isinstance(cycles, (list, tuple)), "invalid cycle domain")
    require(all(isinstance(c, (list, tuple))
                and all(type(e) is int and 0 <= e < len(edges) for e in c)
                and len(c) == len(set(c)) for c in cycles), "invalid cycle support")
    cycle_set = {frozenset(c) for c in cycles}
    require(len(cycle_set) == len(cycles), "duplicate simple cycle")
    _, complete_cycles = cycle_space(vertex_count, edges)
    require(cycle_set == {frozenset(c) for c in complete_cycles},
            "missing or invalid simple cycle in first-move domain")
    original_supports = {
        p: frozenset(e for e, value in enumerate(flow) if parity(p, value))
        for p in range(1, 8)
    }
    require(all(original_supports.values()), "original flow has rank at most two")
    original_simple = 0
    for p, support in original_supports.items():
        if support in cycle_set:
            original_simple += 1
            require({flow[e] for e in support} == {d for d in range(1, 8) if parity(p, d)},
                    "a legal single-cycle rank reduction is possible")

    first_moves, projection_count, blocked_count = 0, 0, 0
    per_functional = Counter()
    simple_lengths, disconnected_shapes = Counter(), Counter()
    first_flows = set()
    for cycle in cycles:
        support = frozenset(cycle)
        for delta in range(1, 8):
            if any(flow[e] == delta for e in cycle):
                continue
            first_moves += 1
            changed = tuple(value ^ delta if e in support else value
                            for e, value in enumerate(flow))
            validate_flow(vertex_count, edges, changed)
            require(changed not in first_flows, "two first moves give the same flow")
            first_flows.add(changed)
            for p in range(1, 8):
                projection_count += 1
                projected = frozenset(e for e, value in enumerate(changed) if parity(p, value))
                require(bool(projected), "a legal first move reaches rank at most two")
                if projected in cycle_set:
                    values = {changed[e] for e in projected}
                    eligible = {d for d in range(1, 8) if parity(p, d)}
                    require(values == eligible,
                            "an unblocked simple projection permits a second rank-reducing move")
                    blocked_count += 1
                    per_functional[p] += 1
                    simple_lengths[len(projected)] += 1
                else:
                    pieces = components(vertex_count, edges, projected)
                    require(len(pieces) > 1, "a connected even projection is missing from cycle domain")
                    disconnected_shapes[tuple(sorted(map(len, pieces)))] += 1
    return {
        "legal_first_moves": first_moves,
        "distinct_first_flows": len(first_flows),
        "original_nonempty_projections": len(original_supports),
        "original_simple_projection_barriers": original_simple,
        "first_flow_nonempty_projections": projection_count,
        "simple_projection_barriers": blocked_count,
        "disconnected_projections": projection_count - blocked_count,
        "simple_projection_barriers_by_functional": dict(sorted(per_functional.items())),
        "simple_projection_lengths": dict(sorted(simple_lengths.items())),
        "disconnected_projection_component_lengths": [
            {"component_lengths": list(shape), "count": count}
            for shape, count in sorted(disconnected_shapes.items())
        ],
    }


def verify(source_path=DEFAULT_SOURCE):
    """Pin the original certificate and return a recomputed structural receipt.

    No fields of search-result.json are trusted or checked.  In particular,
    this does not verify its chromatic histogram, final-flow counts, or time.
    The parent's witness checker separately handles any three-step witness.
    """
    raw = Path(source_path).read_bytes()
    require(sha256(raw).hexdigest() == SOURCE_SHA256, "source bytes do not match pin")
    source = json.loads(raw, object_pairs_hook=unique_object)
    graph, flow = source["graph"], source["flow"]
    vertex_count, edges = graph["vertex_count"], graph["edges"]
    # Derive this graph from the defining Fano incidence relation; no edge table.
    expected_edges = [[p - 1, n + 6] for p in range(1, 8) for n in range(1, 8)
                      if parity(p, n) == 0]
    require(type(vertex_count) is int and vertex_count == 14 and edges == expected_edges,
            "pinned graph is not the specified ordered Fano incidence graph")
    validate_flow(vertex_count, edges, flow)
    even_supports, cycles = cycle_space(vertex_count, edges)
    matchings = perfect_matchings(vertex_count, edges)
    require(bool(matchings), "no perfect matchings")
    all_edges = set(range(len(edges)))
    for matching in matchings:
        complement = all_edges - set(matching)
        require(len(complement) == vertex_count, "matching complement is not spanning")
        require(len(components(vertex_count, edges, complement)) == 1,
                "a 2-factor is not Hamiltonian; three-color/rank reduction is unavailable")
    receipt = {
        "status": "verified",
        "source_certificate_sha256": SOURCE_SHA256,
        "method": "Hamiltonian 2-factors and seven binary projection barriers",
        "even_supports": len(even_supports),
        "simple_cycles": len(cycles),
        "simple_cycle_length_counts": dict(sorted(Counter(map(len, cycles)).items())),
        "perfect_matchings": len(matchings),
        "hamiltonian_matching_complements": len(matchings),
        **projection_barriers(vertex_count, edges, flow, cycles),
        "conclusion": "No flow obtainable by at most two legal simple-cycle XOR changes has a three-colorable affine palette.",
        "discovery_palette_histogram_verified": False,
    }
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    args = parser.parse_args()
    try:
        receipt = verify(args.source)
    except (ValueError, KeyError, TypeError, IndexError, OSError) as exc:
        print(json.dumps({"status": "not_verified", "reason": str(exc)}))
        return 1
    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
