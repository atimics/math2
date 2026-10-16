"""Direct verification of a three-cycle repair, without a search solver.

Alexander Richard Towell; substantial OpenAI Codex assistance. Apache-2.0.
"""
import argparse
from collections import Counter
from hashlib import sha256
from functools import reduce
import json
from operator import xor
from pathlib import Path

SOURCE_SHA256 = 'fb8503f1cc92725d9981dd3320e2556fa1dcf74a0ade94f77cca04c88cf5b98f'
HERE = Path(__file__).parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(items):
    result = {}
    for key, value in items:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def read_json(path):
    return json.loads(Path(path).read_text(), object_pairs_hook=unique_object)


def connected_cycle(edges, selected):
    require(type(selected) is list and selected, 'nonempty cycle list required')
    require(all(type(e) is int and 0 <= e < len(edges) for e in selected),
            'invalid cycle edge')
    require(len(set(selected)) == len(selected), 'repeated cycle edge')
    adjacent = {}
    for e in selected:
        u, v = edges[e]
        adjacent.setdefault(u, []).append(v)
        adjacent.setdefault(v, []).append(u)
    require(all(len(row) == 2 for row in adjacent.values()), 'not a 2-regular cycle')
    reached, todo = set(), [next(iter(adjacent))]
    while todo:
        u = todo.pop()
        if u not in reached:
            reached.add(u)
            todo.extend(adjacent[u])
    require(reached == set(adjacent), 'disconnected cycle')
    return len(reached)


def verify(data, source_path):
    raw = Path(source_path).read_bytes()
    require(sha256(raw).hexdigest() == SOURCE_SHA256, 'source pin mismatch')
    source = json.loads(raw, object_pairs_hook=unique_object)
    edges, n = source['graph']['edges'], source['graph']['vertex_count']
    incident = [[e for e, pair in enumerate(edges) if v in pair] for v in range(n)]
    require(all(len(row) == 3 for row in incident), 'source must be cubic')

    def check_flow(flow):
        require(type(flow) is list and len(flow) == len(edges), 'wrong flow shape')
        require(all(type(x) is int and 1 <= x <= 7 for x in flow), 'zero or invalid flow')
        require(all(reduce(xor, (flow[e] for e in row), 0) == 0 for row in incident),
                'nonconservative flow')

    current = source['flow']
    check_flow(current)
    steps = data['steps']
    require(type(steps) is list and len(steps) == 3, 'exactly three steps required')
    lengths, deltas = [], []
    for step in steps:
        cycle, delta = step['cycle_edges'], step['delta']
        lengths.append(connected_cycle(edges, cycle))
        require(type(delta) is int and 1 <= delta <= 7, 'nonzero XOR vector required')
        deltas.append(delta)
        support = set(cycle)
        calculated = [x ^ delta if e in support else x for e, x in enumerate(current)]
        check_flow(calculated)
        check_flow(step['flow'])
        require(calculated == step['flow'], 'incorrect intermediate flow')
        current = calculated
    check_flow(data['final_flow'])
    require(current == data['final_flow'], 'incorrect final flow')
    labels = sorted(set(current))
    require(len(labels) == 3 and reduce(xor, labels, 0) == 0, 'final flow is not rank two')

    # Zero translations: at each endpoint the pair is the other two flow labels.
    pairs = []
    for e, (u, v) in enumerate(edges):
        left = sorted(current[j] for j in incident[u] if j != e)
        right = sorted(current[j] for j in incident[v] if j != e)
        require(left == right and len(set(left)) == 2, 'affine endpoint mismatch')
        require(left[0] ^ left[1] == current[e], 'wrong induced flow')
        pairs.append(left)
    for row in incident:
        counts = Counter(a for e in row for a in pairs[e])
        require(set(counts) == set(labels) and set(counts.values()) == {2},
                'label degrees are not two')
    cover_lengths = [connected_cycle(edges, [e for e, pair in enumerate(pairs) if a in pair])
                     for a in labels]
    require(cover_lengths == [n]*3, 'label cover is not three Hamiltonian cycles')
    return {'status': 'verified', 'steps': len(steps), 'cycle_lengths': lengths,
            'deltas': deltas, 'final_labels': labels, 'translations': [0]*n,
            'cover_cycle_lengths': cover_lengths, 'edge_pairs': pairs}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path,
                        default=HERE.parent/'heawood'/'certificate.json')
    parser.add_argument('--witness', type=Path, default=HERE/'three-step-experiment.json')
    args = parser.parse_args()
    try:
        result = verify(read_json(args.witness), args.source)
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(json.dumps({'status': 'not_verified', 'error': str(error)}))
        raise SystemExit(1) from error
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
