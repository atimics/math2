"""Exact all-lifts Heawood obstruction and a different-flow three-cover.

Copyright 2026 Alexander Richard Towell. Apache-2.0.
Substantial OpenAI Codex assistance; finite computation, not Lean proof.
"""
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json

from ..affine_lifts import (
    Graph, Lift, enumerate_lifts, validate_flow, verify_lift, verify_coloring,
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def expected_graph():
    return Graph.read({'vertex_count': 14, 'edges': [
        [p - 1, n + 6] for p in range(1, 8) for n in range(1, 8)
        if (p & n).bit_count() % 2 == 0]})


def connected(graph, omit=None):
    reached, pending = {0}, [0]
    while pending:
        u = pending.pop()
        for e, (a, b) in enumerate(graph.edges):
            if e != omit and u in (a, b):
                v = b if u == a else a
                if v not in reached:
                    reached.add(v)
                    pending.append(v)
    return len(reached) == graph.vertex_count


def verify(data):
    require(data.get('schema_version') == 1, 'unsupported schema')
    graph = Graph.read(data['graph'])
    require(graph == expected_graph(), 'graph differs from Fano incidence definition')
    require(len(set(graph.edges)) == 21 and connected(graph)
            and all(connected(graph, e) for e in range(21)), 'graph is not simple connected bridgeless')
    flow = tuple(data['flow'])
    validate_flow(graph, flow)
    saved = []
    for row in data['lifts']:
        lift = Lift(tuple(row['translations']), tuple(tuple(p) for p in row['pairs']))
        verify_lift(graph, flow, lift)
        labels = {a for p in lift.pairs for a in p}
        clique = row['clique']
        require(len(clique) == len(set(clique)) == 7 and set(clique) == labels,
                'clique must contain exactly the seven active labels')
        require({tuple(sorted(p)) for p in lift.pairs} == set(combinations(sorted(labels), 2)),
                'palette is not the complete graph K7')
        require(row['chromatic_number'] == 7, 'incorrect chromatic number')
        verify_coloring(lift.pairs, {int(k): v for k, v in row['coloring'].items()}, 7)
        saved.append(lift)
    require(len(saved) == len(set(saved)) == 2, 'expected two distinct saved lifts')
    # Both trees enumerate every compatible root-fixed lift, including all
    # non-tree constraints. Neither route calls binary elimination or search.
    for reverse in (False, True):
        require(set(saved) == set(enumerate_lifts(graph, flow, reverse)),
                'saved lifts do not cover the complete affine space')
    other = data['comparator']
    other_flow = tuple(other['flow'])
    other_lift = Lift(tuple(other['translations']), tuple(tuple(p) for p in other['pairs']))
    validate_flow(graph, other_flow)
    verify_lift(graph, other_flow, other_lift)
    require(other_flow != flow and set(other_flow) == {1, 2, 3}, 'comparator must use a different rank-two flow')
    require({a for p in other_lift.pairs for a in p} == {1, 2, 3}, 'comparator must use three labels')
    require(all({other_flow[e] for e in row} == {1, 2, 3} for row in graph.incident()),
            'comparator is not a proper three-edge-coloring')
    digest = hashlib.sha256(json.dumps(data, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    return {'status': 'verified', 'vertices': 14, 'edges': 21,
            'root_fixed_lifts': 2, 'all_lifts_including_global_translates': 16,
            'palette_chromatic_numbers': [7, 7], 'tree_assignments_per_replay': 8192,
            'independent_tree_orders': 2, 'different_flow_cover_labels': 3,
            'certificate_sha256': digest,
            'scope': 'Specified Heawood flow only; no obstruction to unrestricted five-covers'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path, default=Path(__file__).with_name('certificate.json'))
    args = parser.parse_args()
    try:
        result = verify(json.loads(args.certificate.read_text()))
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(json.dumps({'status': 'not_verified', 'reason': str(error)}))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
