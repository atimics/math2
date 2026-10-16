"""Independent cycle-space, finite-domain, and subset-DP certificate checker.

Standard library only. No imports from discovery or predecessor checkers.
Validation remains active under Python -O. Separately authored AI review;
Alexander Richard Towell, substantial OpenAI Codex assistance.
"""
import argparse
from collections import Counter, deque
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

SOURCE_SHA256 = 'fb8503f1cc92725d9981dd3320e2556fa1dcf74a0ade94f77cca04c88cf5b98f'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def same(actual, expected, message):
    require(json.dumps(actual, sort_keys=True) == json.dumps(expected, sort_keys=True), message)


def unique_object(items):
    obj = {}
    for key, value in items:
        require(key not in obj, 'duplicate JSON object key')
        obj[key] = value
    return obj


def read_json(path):
    return json.loads(Path(path).read_text(), object_pairs_hook=unique_object)


def incident(n, edges):
    return [[i for i, edge in enumerate(edges) if v in edge] for v in range(n)]


def cycle_domain(n, edges, inc):
    reached, pending, tree = {0}, deque([0]), []
    while pending:
        u = pending.popleft()
        for e in inc[u]:
            a, b = edges[e]
            v = b if a == u else a
            if v not in reached:
                reached.add(v)
                pending.append(v)
                tree.append((u, v, e))
    require(len(reached) == n, 'disconnected source')
    tree_edges = {e for _, _, e in tree}
    chords = [e for e in range(len(edges)) if e not in tree_edges]
    cycles = []
    for bits in range(1 << len(chords)):
        selected = [0]*len(edges)
        for i, e in enumerate(chords):
            selected[e] = (bits >> i) & 1
        for _, v, e in reversed(tree):
            selected[e] = sum(selected[j] for j in inc[v] if j != e) % 2
        require(all(sum(selected[e] for e in row) % 2 == 0 for row in inc),
                'cycle-space parity reconstruction failed')
        support = tuple(e for e, value in enumerate(selected) if value)
        if not support:
            continue
        degree = [sum(selected[e] for e in row) for row in inc]
        if any(d not in (0, 2) for d in degree):
            continue
        active = {v for v, d in enumerate(degree) if d}
        seen = {min(active)}
        pending = list(seen)
        while pending:
            u = pending.pop()
            for e in inc[u]:
                if selected[e]:
                    a, b = edges[e]
                    v = b if a == u else a
                    if v not in seen:
                        seen.add(v)
                        pending.append(v)
        if seen == active:
            cycles.append(support)
    require(len(cycles) == len(set(cycles)), 'repeated cycle-space support')
    return sorted(cycles, key=lambda c: (len(c), c)), len(chords)


def validate_flow(flow, edges, inc):
    require(len(flow) == len(edges), 'wrong flow length')
    require(all(type(x) is int and 1 <= x <= 7 for x in flow), 'invalid flow value')
    require(all(flow[a] ^ flow[b] ^ flow[c] == 0 for a, b, c in inc), 'nonconservative flow')


def lifts(n, edges, inc, flow):
    validate_flow(flow, edges, inc)
    local = {(v, e): tuple(flow[j] for j in inc[v] if j != e)
             for v in range(n) for e in inc[v]}
    relations = {}
    for e, (u, v) in enumerate(edges):
        relations[u, v] = {(x, y) for x in range(8) for y in range(8)
                           if {a ^ x for a in local[u, e]} == {a ^ y for a in local[v, e]}}
        relations[v, u] = {(y, x) for x, y in relations[u, v]}

    def visit(domains):
        domains = [set(d) for d in domains]
        changed = True
        while changed:
            changed = False
            for (u, v), relation in relations.items():
                keep = {x for x in domains[u] if any((x, y) in relation for y in domains[v])}
                if not keep:
                    return []
                if keep != domains[u]:
                    domains[u] = keep
                    changed = True
        free = [v for v in range(n) if len(domains[v]) > 1]
        if not free:
            return [tuple(next(iter(d)) for d in domains)]
        v = min(free, key=lambda u: (len(domains[u]), u))
        result = []
        for x in sorted(domains[v]):
            child = [d.copy() for d in domains]
            child[v] = {x}
            result.extend(visit(child))
        return result

    result = {}
    for t in visit([{0}] + [set(range(8)) for _ in range(n-1)]):
        pairs = tuple(tuple(sorted(a ^ t[u] for a in local[u, e]))
                      for e, (u, v) in enumerate(edges))
        require(t not in result, 'repeated translation')
        require(all(set(pairs[e]) == {a ^ t[v] for a in local[v, e]}
                    for e, (u, v) in enumerate(edges)), 'invalid endpoint agreement')
        require(all(a != b and a ^ b == flow[e] for e, (a, b) in enumerate(pairs)),
                'invalid induced flow')
        require(all(all(count == 2 for count in Counter(a for e in row for a in pairs[e]).values())
                    for row in inc), 'invalid cover parity')
        result[t] = pairs
    return result


@lru_cache(None)
def chromatic(palette):
    labels = sorted({a for pair in palette for a in pair})
    index = {a: i for i, a in enumerate(labels)}
    edge_masks = [(1 << index[a]) | (1 << index[b]) for a, b in palette]
    size = 1 << len(labels)
    independent = [all(mask & edge != edge for edge in edge_masks) for mask in range(size)]
    dp = [0] + [len(labels)+1]*(size-1)
    for mask in range(1, size):
        anchor, sub = mask & -mask, mask
        while sub:
            if sub & anchor and independent[sub]:
                dp[mask] = min(dp[mask], 1+dp[mask ^ sub])
            sub = (sub-1) & mask
    return dp[-1]


def verify(data, source_path):
    raw = Path(source_path).read_bytes()
    require(sha256(raw).hexdigest() == SOURCE_SHA256, 'source bytes do not match pin')
    source = json.loads(raw, object_pairs_hook=unique_object)
    same(data['schema_version'], 1, 'unsupported schema')
    same(data['source_certificate_sha256'], SOURCE_SHA256, 'wrong source pin')
    same(data['graph'], source['graph'], 'graph differs from pinned source')
    same(data['original_flow'], source['flow'], 'flow differs from pinned source')
    n = source['graph']['vertex_count']
    edges = list(map(tuple, source['graph']['edges']))
    flow = source['flow']
    inc = incident(n, edges)
    require(all(len(row) == 3 for row in inc), 'source is not cubic')
    validate_flow(flow, edges, inc)
    cycles, dimension = cycle_domain(n, edges, inc)
    same(data['simple_cycles'], cycles, 'missing, repeated, or wrong cycle')
    same(data['simple_cycle_length_counts'],
         {str(k): v for k, v in Counter(map(len, cycles)).items()}, 'cycle histogram mismatch')
    expected_keys = {(cycle, delta) for cycle in cycles for delta in range(1, 8)
                     if all(flow[e] != delta for e in cycle)}
    records = data['records']
    require(type(records) is list, 'records must be a list')
    same(data['total_admissible_changes'], len(expected_keys), 'wrong domain size')
    same(data['completed_changes'], len(records), 'wrong completed count')
    require(data['complete'] is True, 'incomplete certificate')
    require(len(records) == len(expected_keys), 'missing or extra records')
    seen, histogram, successes, lift_counts = set(), Counter(), [], Counter()
    for record in records:
        cycle, delta = record['cycle_edges'], record['delta']
        require(type(cycle) is list and all(type(e) is int for e in cycle), 'invalid cycle indices')
        require(type(delta) is int, 'invalid delta')
        key = (tuple(cycle), delta)
        require(key in expected_keys and key not in seen, 'unknown or repeated change')
        seen.add(key)
        support = set(cycle)
        modified = [x ^ delta if e in support else x for e, x in enumerate(flow)]
        same(record['flow'], modified, 'incorrect modified flow')
        actual = lifts(n, edges, inc, modified)
        require(bool(actual), 'no compatible lifts')
        chis = {t: chromatic(tuple(sorted(set(pairs)))) for t, pairs in actual.items()}
        translations, numbers = record['root_fixed_translations'], record['palette_chromatic_numbers']
        require(type(translations) is list and type(numbers) is list, 'invalid lift lists')
        require(len(translations) == len(numbers) == len(actual), 'missing or extra lifts')
        listed = []
        for t, k in zip(translations, numbers):
            require(type(t) is list and len(t) == n
                    and all(type(x) is int and 0 <= x <= 7 for x in t), 'invalid translation')
            t = tuple(t)
            require(t in actual and t not in listed, 'wrong or repeated lift')
            listed.append(t)
            same(k, chis[t], 'wrong palette chromatic number')
        minimum = min(chis.values())
        same(record['minimum_palette_chromatic_number'], minimum, 'wrong minimum')
        best = record['best_lift']
        best_t = min(actual, key=lambda t: (chis[t], t))
        same(best['translations'], best_t, 'wrong best translation')
        same(best['pairs'], actual[best_t], 'wrong best pairs')
        same(best['chromatic_number'], minimum, 'wrong best chromatic number')
        palette = set(actual[best_t])
        labels = sorted({a for pair in palette for a in pair})
        clique = best['clique']
        require(type(clique) is list and all(type(a) is int for a in clique)
                and len(clique) == len(set(clique)) and set(clique) <= set(labels), 'invalid clique labels')
        require(all(tuple(sorted(pair)) in palette for pair in combinations(clique, 2)),
                'clique contains nonedge')
        omega = max(len(c) for k in range(1, len(labels)+1) for c in combinations(labels, k)
                    if all(pair in palette for pair in combinations(c, 2)))
        same(len(clique), omega, 'clique is not maximum')
        colors = best['coloring']
        require(type(colors) is dict and set(colors) == {str(a) for a in labels}, 'coloring label mismatch')
        require(all(type(value) is int and 0 <= value < minimum for value in colors.values()), 'invalid color')
        require(all(colors[str(a)] != colors[str(b)] for a, b in palette), 'coloring collision')
        histogram[minimum] += 1
        lift_counts[len(actual)] += 1
        if minimum <= 5:
            successes.append(len(cycle))
    require(seen == expected_keys, 'incomplete change domain')
    same(data['minimum_palette_histogram'], {str(k): v for k, v in histogram.items()},
         'wrong aggregate histogram')
    same(data['successful_changes_to_five'], len(successes), 'wrong success count')
    same(data['shortest_successful_cycle_length'], min(successes, default=None), 'wrong shortest repair')
    return {'status': 'verified', 'cycle_space_dimension': dimension, 'simple_cycles': len(cycles),
            'admissible_changes': len(seen), 'minimum_palette_histogram': dict(sorted(histogram.items())),
            'root_fixed_lift_count_histogram': dict(sorted(lift_counts.items())),
            'successful_changes_to_five': len(successes),
            'shortest_successful_cycle_length': min(successes, default=None)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    here = Path(__file__).resolve().parent
    parser.add_argument('--certificate', type=Path, default=here/'certificate.json')
    parser.add_argument('--source', type=Path,
                        default=here.parent/'heawood'/'certificate.json')
    args = parser.parse_args()
    try:
        result = verify(read_json(args.certificate), args.source)
    except (ValueError, KeyError, TypeError, IndexError, OSError) as exc:
        print(json.dumps({'status': 'not_verified', 'reason': str(exc)}))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
