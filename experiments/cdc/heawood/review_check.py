"""Independent finite-domain verification of the Heawood fixed-flow claim.

Read-only reviewer supplied this source; parent saved it without changing
the algorithm. Substantial OpenAI Codex assistance; not human peer review.
"""

if not __debug__:
    raise RuntimeError("Run this certificate checker without Python -O")

import json
from pathlib import Path
from itertools import combinations
from collections import Counter

p = Path(__file__).resolve().parent
b = json.loads((p / "benchmark.json").read_text())
n = b["graph"]["vertex_count"]
edges = [tuple(e) for e in b["graph"]["edges"]]

assert n == 14 and len(edges) == 21
assert len(set(map(frozenset, edges))) == 21
assert all(0 <= u < n and 0 <= v < n and u != v for u, v in edges)
inc = [[i for i, e in enumerate(edges) if v in e] for v in range(n)]
assert all(len(row) == 3 for row in inc)
assert edges == [
    (point - 1, normal + 6)
    for point in range(1, 8)
    for normal in range(1, 8)
    if sum(((point >> k) & 1) * ((normal >> k) & 1)
           for k in range(3)) % 2 == 0
]


def connected(omit=None):
    seen = {0}
    while True:
        nxt = (seen | {v for i, (u, v) in enumerate(edges) if i != omit and u in seen}
               | {u for i, (u, v) in enumerate(edges) if i != omit and v in seen})
        if nxt == seen:
            return len(seen) == n
        seen = nxt


assert connected()
assert all(connected(i) for i in range(len(edges)))
f = b["records"][0]["flow"]
assert len(f) == len(edges)
assert all(type(x) is int and 1 <= x <= 7 for x in f)
assert all(f[a] ^ f[c] ^ f[d] == 0 for a, c, d in inc)
local = {(v, i): frozenset(f[j] for j in inc[v] if j != i)
         for v in range(n) for i in inc[v]}
allowed = {}
for i, (u, v) in enumerate(edges):
    allowed[u, v] = {(x, y) for x in range(8) for y in range(8)
                     if {a ^ x for a in local[u, i]} == {a ^ y for a in local[v, i]}}
    allowed[v, u] = {(y, x) for x, y in allowed[u, v]}
nodes = [0]


def enumerate_domains(domains):
    """Exhaustive branching with solution-preserving arc consistency."""
    nodes[0] += 1
    domains = [set(d) for d in domains]
    changed = True
    while changed:
        changed = False
        for (u, v), relation in allowed.items():
            keep = {x for x in domains[u] if any((x, y) in relation for y in domains[v])}
            if not keep:
                return []
            if keep != domains[u]:
                domains[u] = keep
                changed = True
    undecided = [v for v in range(n) if len(domains[v]) > 1]
    if not undecided:
        return [tuple(next(iter(d)) for d in domains)]
    v = min(undecided, key=lambda u: (len(domains[u]), u))
    answers = []
    for x in sorted(domains[v]):
        child = [d.copy() for d in domains]
        child[v] = {x}
        answers.extend(enumerate_domains(child))
    return answers


sol = enumerate_domains([{0}] + [set(range(8)) for _ in range(n - 1)])
root_search_nodes = nodes[0]
assert len(sol) == len(set(sol)) == 2
assert set(sol) == {tuple(r["translations"]) for r in b["records"][0]["lifts"]}
tree = json.loads((p / "tree-result.json").read_text())
assert set(sol) == {tuple(r["translations"]) for r in tree["records"]}
for t in sol:
    pairs = [tuple(sorted(a ^ t[u] for a in local[u, i])) for i, (u, v) in enumerate(edges)]
    labels = sorted({x for pair in pairs for x in pair})
    assert len(labels) == 7
    assert set(pairs) == set(combinations(labels, 2))
    assert all({a ^ t[u] for a in local[u, i]} == {a ^ t[v] for a in local[v, i]}
               for i, (u, v) in enumerate(edges))
    assert all(pair[0] ^ pair[1] == f[i] for i, pair in enumerate(pairs))
    assert all(all(count == 2 for count in Counter(a for i in inc[v] for a in pairs[i]).values())
               for v in range(n))
    recorded = next(r for r in b["records"][0]["lifts"] if tuple(r["translations"]) == t)
    assert pairs == list(map(tuple, recorded["pairs"]))
all_sol = enumerate_domains([set(range(8)) for _ in range(n)])
assert len(all_sol) == len(set(all_sol)) == 16
assert set(all_sol) == {tuple(x ^ gauge for x in t) for t in sol for gauge in range(8)}
c = json.loads((p / "comparator.json").read_text())
cf, cp = c["flow"], c["pairs"]
assert len(cf) == len(cp) == 21
assert c["translations"] == [0] * 14
assert all(type(x) is int and x in (1, 2, 3) for x in cf)
assert cf != f
assert all({cf[i] for i in row} == {1, 2, 3} for row in inc)
assert all(len(pair) == 2 and len(set(pair)) == 2
           and set(pair) == {1, 2, 3} - {cf[i]} for i, pair in enumerate(cp))
assert all(a ^ b == cf[i] for i, (a, b) in enumerate(cp))
assert all(Counter(a for i in row for a in cp[i]) == Counter({1: 2, 2: 2, 3: 2}) for row in inc)
assert Counter(a for pair in cp for a in pair) == Counter({1: 14, 2: 14, 3: 14})
print(json.dumps({
    "graph": "Fano incidence: simple, cubic, connected, bridgeless",
    "root_fixed_lifts": sol, "palette_chromatic_numbers": [7, 7],
    "root_propagation_search_nodes": root_search_nodes,
    "unfixed_lifts": len(all_sol),
    "comparator": "three-label Eulerian double cover, different flow",
}, indent=2))
