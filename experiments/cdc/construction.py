"""Bounded F2^3-flow search and exact affine eight-label construction.

A successful output is a witness, not a general existence proof. A bounded
flow search that reaches its state limit makes no existence claim.
Integers 0..7 encode vectors; vector addition is bitwise XOR.
"""
from __future__ import annotations
from .graphs import validate_graph


def binary_solve(rows: list[tuple[int, int]], variable_count: int) -> list[int] | None:
    """Solve mask-dot-x = rhs over F2; choose all free variables zero."""
    pivots = {}
    for mask, rhs in rows:
        while mask:
            pivot = mask.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = (mask, rhs)
                break
            other_mask, other_rhs = pivots[pivot]
            mask ^= other_mask
            rhs ^= other_rhs
        if not mask and rhs:
            return None
    solution = 0
    for pivot in sorted(pivots):
        mask, rhs = pivots[pivot]
        if ((mask & solution).bit_count() & 1) != rhs:
            solution |= 1 << pivot
    return [(solution >> i) & 1 for i in range(variable_count)]


def affine_witness(graph: dict, flow: list[int]) -> dict:
    """Return an eight-label witness for a valid flow.

    For each incidence choose the flow of another incident edge as c_v,e.
    The three resulting pairs form the triangle of nonzero incident flows. Solve
    t_u + t_v + epsilon_e*f_e = c_u,e + c_v,e exactly over F2.
    """
    validate_graph(graph)
    n, edges = graph["vertex_count"], graph["edges"]
    if len(flow) != len(edges) or any(type(x) is not int or not 1 <= x <= 7 for x in flow):
        raise ValueError("flow must assign a nonzero F2^3 vector to each edge")
    incident = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        incident[u].append(i)
        incident[v].append(i)
    corners = {}
    for u, edge_ids in enumerate(incident):
        if flow[edge_ids[0]] ^ flow[edge_ids[1]] ^ flow[edge_ids[2]]:
            raise ValueError("flow conservation fails")
        for i, corner in zip(edge_ids, (flow[edge_ids[1]], flow[edge_ids[0]], flow[edge_ids[0]])):
            corners[u, i] = corner
    rows = []
    variable_count = 3 * n + len(edges)
    for i, (u, v) in enumerate(edges):
        rhs = corners[u, i] ^ corners[v, i]
        for bit in range(3):
            mask = (1 << (3 * u + bit)) ^ (1 << (3 * v + bit))
            if (flow[i] >> bit) & 1:
                mask ^= 1 << (3 * n + i)
            rows.append((mask, (rhs >> bit) & 1))
    rows.extend((1 << bit, 0) for bit in range(3))  # global translation gauge
    solved = binary_solve(rows, variable_count)
    if solved is None:
        raise RuntimeError("affine compatibility invariant failed for a valid cubic flow")
    translations = [sum(solved[3 * u + bit] << bit for bit in range(3)) for u in range(n)]
    pairs = []
    for i, (u, _v) in enumerate(edges):
        a = translations[u] ^ corners[u, i]
        pairs.append(sorted([a, a ^ flow[i]]))
    return {"vertex_count": n, "edges": [list(edge) for edge in edges],
            "labels": 8, "pairs": pairs, "flow": list(flow),
            "translations": translations, "edge_flips": solved[3 * n:]}


def construct_cover(graph: dict, node_limit: int = 100_000) -> dict:
    """Search deterministic flows until an affine witness is found.

    Return status 'found', 'exhausted', or 'limit', plus state/flow counts and
    witness when found. The limit counts recursive search states, not time.
    Fix the first flow vector to 1 by a valid global GL(3,2) symmetry.
    """
    validate_graph(graph)
    if type(node_limit) is not int or node_limit < 1:
        raise ValueError("node_limit must be a positive integer")
    edges, n = graph["edges"], graph["vertex_count"]
    incident = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        incident[u].append(i)
        incident[v].append(i)
    stats = {"states": 0, "flows_tested": 0}
    limited = False
    answer = None

    def search(values):
        nonlocal limited, answer
        if stats["states"] >= node_limit:
            limited = True
            return
        stats["states"] += 1
        values = values[:]
        changed = True
        while changed:
            changed = False
            for edge_ids in incident:
                missing = [i for i in edge_ids if not values[i]]
                total = 0
                for i in edge_ids:
                    total ^= values[i]
                if not missing:
                    if total:
                        return
                elif len(missing) == 1:
                    if not total:
                        return
                    values[missing[0]] = total
                    changed = True
        unknown = [i for i, value in enumerate(values) if not value]
        if not unknown:
            stats["flows_tested"] += 1
            answer = affine_witness(graph, values)
            return
        # Expand edges adjacent to the largest number of assigned edges first.
        i = max(unknown, key=lambda e: (sum(bool(values[j]) for u in edges[e]
                                            for j in incident[u]), -e))
        choices = (1,) if not any(values) else range(1, 8)
        for value in choices:
            next_values = values[:]
            next_values[i] = value
            search(next_values)
            if answer is not None or limited:
                return

    search([0] * len(edges))
    result = {"status": "found" if answer is not None else "limit" if limited else "exhausted",
              **stats, "node_limit": node_limit}
    if answer is not None:
        result["witness"] = answer
    return result


def construct_eight_cover(graph: dict, max_states: int = 100_000) -> dict:
    """Compatibility alias for construct_cover(graph, node_limit)."""
    return construct_cover(graph, node_limit=max_states)
