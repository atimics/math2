"""Complete binary flow enumeration and an independent counting formula.

Cycle coordinates use the earlier packet's graph and spanning-tree definitions.
The inclusion-exclusion count uses neither that tree nor the generated flows.

Copyright 2026 Alexander Richard Towell. Apache-2.0.
Substantial OpenAI Codex assistance, including independent AI review.
See ALL_FLOWS.md for scope, sources, and attribution.
"""
from collections import Counter
from itertools import combinations, product
import argparse
import hashlib
import json
from pathlib import Path
from time import monotonic

try:
    from .affine_lifts import (
        Graph, Lift, FIXTURE, classify, enumerate_lifts, load_fixture,
        spanning_tree, validate_flow, verify_coloring, verify_cover, verify_lift,
    )
except ImportError:
    from affine_lifts import (
        Graph, Lift, FIXTURE, classify, enumerate_lifts, load_fixture,
        spanning_tree, validate_flow, verify_coloring, verify_cover, verify_lift,
    )


def require(condition, message):
    if not condition:
        raise ValueError(message)


def enumerate_flows(graph, reverse=False):
    """Enumerate every nowhere-zero F2^3 flow once, with no search cutoff."""
    tree = spanning_tree(graph, reverse)
    tree_edges = {e for _, _, e in tree}
    chords = [e for e in range(len(graph.edges)) if e not in tree_edges]
    incident = graph.incident()
    for assignment in product(range(8), repeat=len(chords)):
        flow = [0] * len(graph.edges)
        for edge, value in zip(chords, assignment):
            flow[edge] = value
        for _, child, edge in reversed(tree):
            value = 0
            for other in incident[child]:
                if other != edge:
                    value ^= flow[other]
            flow[edge] = value
        if all(flow):
            yield tuple(flow)


def normalize_flow(flow):
    """Send the first independent values to 1,2,4; retain all labelled edges."""
    if any(type(v) is not int or not 0 <= v < 8 for v in flow):
        raise ValueError("expected F2^3 values")
    mapping = {0: 0}
    rank = 0
    for value in flow:
        if value not in mapping:
            mapping.update({old ^ value: new ^ (1 << rank)
                            for old, new in tuple(mapping.items())})
            rank += 1
    return tuple(mapping[v] for v in flow)


def count_by_subsets(graph, order):
    """Inclusion-exclusion of edge-zero conditions, independent of enumeration."""
    answer = 0
    for mask in range(1 << len(graph.edges)):
        parent = list(range(graph.vertex_count))

        def root(v):
            while parent[v] != v:
                v = parent[v]
            return v

        edges = 0
        components = graph.vertex_count
        for e, (u, v) in enumerate(graph.edges):
            if mask >> e & 1:
                edges += 1
                a, b = root(u), root(v)
                if a != b:
                    parent[a] = b
                    components -= 1
        cycle_rank = edges - graph.vertex_count + components
        answer += (-1) ** (len(graph.edges) - edges) * order**cycle_rank
    return answer


def orbit_counts(graph, reverse=False):
    return Counter(normalize_flow(flow) for flow in enumerate_flows(graph, reverse))


def linear_maps():
    """All 168 invertible linear maps, as lookup tables derived from bases."""
    return tuple(
        tuple((a if x & 1 else 0) ^ (b if x & 2 else 0) ^ (c if x & 4 else 0)
              for x in range(8))
        for a, b, c in product(range(1, 8), repeat=3)
        if a != b and c not in (a, b, a ^ b)
    )


def build_certificate(graph):
    """Discovery route. The verifier does not call this or enumerate_flows."""
    counts = orbit_counts(graph)
    records = []
    for flow in sorted(counts):
        result = classify(graph, flow)
        records.append({
            "flow": list(flow), "orbit_size": counts[flow],
            "lifts": [{"translations": list(row["translations"]),
                       "pairs": [list(pair) for pair in row["pairs"]],
                       "chromatic_number": row["chromatic_number"],
                       "clique": list(row["maximum_clique"]),
                       "coloring": {str(k): v for k, v in row["optimal_coloring"].items()}}
                      for row in result["records"]],
        })
    return {"schema_version": 1,
            "graph": {"vertex_count": graph.vertex_count,
                      "edges": [list(edge) for edge in graph.edges]},
            "records": records}


def verify_certificate(graph, certificate):
    """Check positive witnesses, all lifts, and coverage without the generator.

Coverage uses explicit disjoint GL images and inclusion-exclusion. Chromatic
numbers use matching clique/coloring certificates, never failed search.
"""
    require(certificate.get("schema_version") == 1, "unsupported certificate schema")
    require(Graph.read(certificate["graph"]) == graph, "certificate graph differs from source")
    maps = linear_maps()
    seen = set()
    profiles = Counter()
    total_lifts = 0
    lift_histogram = Counter()
    used_label_histogram = Counter()
    for row in certificate["records"]:
        flow = tuple(row["flow"])
        validate_flow(graph, flow)
        require(normalize_flow(flow) == flow, "flow is not normalized")
        orbit = {tuple(mapping[x] for x in flow) for mapping in maps}
        require(len(orbit) == row["orbit_size"] == 168,
                "certificate requires full-rank flow orbits of size 168")
        require(not seen.intersection(orbit), "flow orbits overlap")
        seen.update(orbit)
        lifts = []
        palette_sizes = []
        used_label_counts = []
        for item in row["lifts"]:
            lift = Lift(tuple(item["translations"]), tuple(tuple(p) for p in item["pairs"]))
            verify_lift(graph, flow, lift)
            colors = {int(k): v for k, v in item["coloring"].items()}
            k = item["chromatic_number"]
            verify_coloring(lift.pairs, colors, k)
            verify_cover(graph, tuple((colors[a], colors[b]) for a, b in lift.pairs), k)
            clique = item["clique"]
            interactions = {tuple(sorted(p)) for p in lift.pairs}
            require(type(k) is int and len(set(clique)) == len(clique) == k
                    and all(tuple(sorted(p)) in interactions for p in combinations(clique, 2)),
                    "invalid matching clique certificate")
            lifts.append(lift)
            palette_sizes.append(k)
            used = len({a for pair in lift.pairs for a in pair})
            used_label_counts.append(used)
            used_label_histogram[used] += 1
        # Reverse BFS differs from the construction tree. It checks every one
        # of its 512 possible choices, including all non-tree compatibility.
        expected_lifts = enumerate_lifts(graph, flow, reverse=True)
        require(len(set(lifts)) == len(lifts) and set(lifts) == set(expected_lifts),
                "saved lifts are duplicated, omitted, or incompatible")
        require(any(k <= 5 for k in palette_sizes), "flow has no certified five-colorable lift")
        require(any(n <= 5 for n in used_label_counts), "flow has no literal five-label lift")
        profiles[tuple(sorted(palette_sizes))] += 1
        lift_histogram.update(palette_sizes)
        total_lifts += len(lifts)
    expected_count = count_by_subsets(graph, 8)
    require(len(seen) == expected_count, "orbit coverage differs from independent flow count")
    digest = hashlib.sha256(json.dumps(certificate, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {"status": "verified", "flows": len(seen),
            "independent_inclusion_exclusion_count": expected_count,
            "orbits": len(certificate["records"]), "orbit_size": 168,
            "root_fixed_lifts_across_representatives": total_lifts,
            "palette_profiles": [{"chromatic_numbers": list(p), "orbits": n}
                                 for p, n in sorted(profiles.items())],
            "lift_chromatic_histogram": dict(sorted(lift_histogram.items())),
            "lift_used_label_histogram": dict(sorted(used_label_histogram.items())),
            "all_flows_have_five_colorable_lift": True,
            "all_flows_have_five_label_lift": True,
            "certificate_sha256": digest,
            "scope": "fixed labelled Petersen graph; finite exact computation, not Lean"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=Path(__file__).with_name("all_flows.json"))
    parser.add_argument("--write", action="store_true", help="regenerate and verify the certificate")
    args = parser.parse_args()
    start = monotonic()
    try:
        graph, _, _ = load_fixture(FIXTURE)
        data = build_certificate(graph) if args.write else json.loads(args.certificate.read_text())
        report = verify_certificate(graph, data)
        if args.write:
            args.certificate.write_text(json.dumps(data, separators=(",", ":")) + "\n")
        report["elapsed_seconds"] = round(monotonic() - start, 6)
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(json.dumps({"status": "not_verified", "reason": str(error)}))
        return 1
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
