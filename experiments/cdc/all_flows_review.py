"""Independent AI-review replay: flow propagation, translation CSP, subset DP.

No primary research implementation is imported. The reviewer's script is
adapted to read its graph from the certificate; the graph is independently
checked against the standard labelled Petersen construction.
"""
import argparse
import json
from collections import Counter
from functools import lru_cache
from itertools import product
from pathlib import Path

if not __debug__:
    raise SystemExit("Run this independent review script without -O.")
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--certificate", type=Path, default=Path(__file__).with_name("all_flows.json"))
certificate = json.loads(parser.parse_args().certificate.read_text())
edges = tuple(map(tuple, certificate["graph"]["edges"]))
n = certificate["graph"]["vertex_count"]
standard = {
    tuple(sorted(uv)) for i in range(5)
    for uv in [(i, (i+1)%5), (i, i+5), (i+5, 5+(i+2)%5)]
}
assert n == 10 and len(edges) == 15 and set(edges) == standard
inc = [[e for e, uv in enumerate(edges) if v in uv] for v in range(n)]

def flows(q):
    answer = set()
    def visit(f):
        while True:
            changed = False
            for row in inc:
                unknown = [e for e in row if f[e] is None]
                total = 0
                for e in row:
                    if f[e] is not None:
                        total ^= f[e]
                if not unknown and total:
                    return
                if len(unknown) == 1:
                    if total == 0:
                        return
                    f[unknown[0]], changed = total, True
            if not changed:
                break
        if None not in f:
            assert tuple(f) not in answer
            answer.add(tuple(f))
            return
        e = f.index(None)
        for x in range(1, q):
            child = f.copy()
            child[e] = x
            visit(child)
    visit([None] * len(edges))
    return answer

all_flows = flows(8)
assert len(all_flows) == 28560 and not flows(4)
maps = [
    tuple((a if x&1 else 0) ^ (b if x&2 else 0) ^ (c if x&4 else 0)
          for x in range(8))
    for a,b,c in product(range(1,8), repeat=3)
]
maps = [g for g in maps if len(set(g)) == 8]
assert len(maps) == len(set(maps)) == 168
unseen, reps = all_flows.copy(), []
while unseen:
    f = min(unseen)
    orbit = {tuple(g[x] for x in f) for g in maps}
    assert len(orbit) == 168 and orbit <= unseen
    unseen -= orbit
    reps.append(f)
assert len(reps) == 170

def lifts(f):
    local = {
        (v,e): {f[j] for j in row if j != e}
        for v,row in enumerate(inc) for e in row
    }
    allowed = [
        {x^y for x in local[u,e] for y in local[v,e]}
        for e,(u,v) in enumerate(edges)
    ]
    assert all(len(d) == 2 for d in allowed)
    answer = set()
    def visit(domains):
        while True:
            changed = False
            for e,(u,v) in enumerate(edges):
                du,dv = domains[u],domains[v]
                nu = {x for x in du if any(x^y in allowed[e] for y in dv)}
                nv = {y for y in dv if any(x^y in allowed[e] for x in du)}
                if not nu or not nv:
                    return
                if nu != du or nv != dv:
                    domains[u],domains[v],changed = nu,nv,True
            if not changed:
                break
        unresolved = [v for v in range(n) if len(domains[v]) > 1]
        if unresolved:
            v = min(unresolved, key=lambda v: len(domains[v]))
            for x in sorted(domains[v]):
                child = domains.copy()
                child[v] = {x}
                visit(child)
            return
        t = tuple(next(iter(d)) for d in domains)
        pairs = tuple(
            tuple(sorted(x^t[u] for x in local[u,e]))
            for e,(u,v) in enumerate(edges)
        )
        assert all(set(pairs[e]) == {x^t[v] for x in local[v,e]}
                   for e,(u,v) in enumerate(edges))
        assert (t,pairs) not in answer
        answer.add((t,pairs))
    visit([{0}] + [set(range(8)) for _ in range(n-1)])
    return answer

def chi(pairs):
    independent = [
        all(not (s>>a&1 and s>>b&1) for a,b in pairs)
        for s in range(256)
    ]
    @lru_cache(None)
    def solve(s):
        if s == 0:
            return 0
        best, sub, bit = 8, s, s & -s
        while sub:
            if sub & bit and independent[sub]:
                best = min(best, 1 + solve(s ^ sub))
            sub = (sub-1) & s
        return best
    return solve(255)

rows = {tuple(row["flow"]): row for row in certificate["records"]}
assert len(rows) == len(certificate["records"]) == 170
assert set(rows) == set(reps)
profiles, raw_sizes = Counter(), Counter()
for f in reps:
    actual = lifts(f)
    recorded = {(tuple(x["translations"]), tuple(map(tuple,x["pairs"])))
                for x in rows[f]["lifts"]}
    assert len(recorded) == len(rows[f]["lifts"]) and actual == recorded
    profile = []
    for t,pairs in actual:
        k = chi(pairs)
        labels = {x for pair in pairs for x in pair}
        assert len(labels) == k
        for row in inc:
            degree = Counter(x for e in row for x in pairs[e])
            assert all(d == 2 for d in degree.values())
        raw_sizes[k] += 1
        profile.append(k)
    profiles[tuple(sorted(profile))] += 1
assert profiles == Counter({(5,):80, (5,5):60, (5,6):20, (5,5,5,6):10})
print("direct flows:", len(all_flows), "; GL orbits:", len(reps))
print("direct translation-CSP / subset-DP profiles:", dict(sorted(profiles.items())))
print("literal palette sizes:", dict(raw_sizes), "; certificate exact-set match: PASS")
