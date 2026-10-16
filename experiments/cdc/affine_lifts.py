#!/usr/bin/env python3
"""Independent direct checker for the Petersen affine-lift experiment.

No elimination, optimizer, graph library, or construction code is imported.
Every root-fixed lift is reached by two choices per spanning-tree edge; all
remaining edges are then checked by literal equality of translated pairs.
Coloring enumerates canonical set partitions in fixed label order.

Copyright 2026 Alexander Richard Towell. Apache-2.0.
Substantial OpenAI Codex assistance, including a separate AI reviewer.
See AFFINE_LIFTS.md for scope, predecessor credit, and source pins.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
from dataclasses import dataclass
from itertools import combinations, product
import json
from pathlib import Path
import sys
import unittest


@dataclass(frozen=True)
class Graph:
    vertex_count: int
    edges: tuple[tuple[int, int], ...]

    @classmethod
    def read(cls, data: dict) -> Graph:
        n = data["vertex_count"]
        if type(n) is not int or n < 1:
            raise ValueError("vertex_count must be a positive integer")
        edges = tuple(tuple(edge) for edge in data["edges"])
        for edge in edges:
            if len(edge) != 2 or any(type(v) is not int for v in edge):
                raise ValueError("an edge must have two integer endpoints")
            u, v = edge
            if not (0 <= u < n and 0 <= v < n) or u == v:
                raise ValueError("invalid or loop edge")
        graph = cls(n, edges)
        if any(len(row) != 3 for row in graph.incident()):
            raise ValueError("graph must be cubic")
        return graph

    def incident(self) -> tuple[tuple[int, ...], ...]:
        rows: list[list[int]] = [[] for _ in range(self.vertex_count)]
        for edge_id, (u, v) in enumerate(self.edges):
            rows[u].append(edge_id)
            rows[v].append(edge_id)
        return tuple(tuple(row) for row in rows)


@dataclass(frozen=True)
class Lift:
    translations: tuple[int, ...]
    pairs: tuple[tuple[int, int], ...]


def validate_flow(graph: Graph, flow: tuple[int, ...]) -> None:
    if len(flow) != len(graph.edges):
        raise ValueError("wrong number of flow values")
    if any(type(value) is not int or not 1 <= value <= 7 for value in flow):
        raise ValueError("flow values must be nonzero F2^3 vectors")
    for incident in graph.incident():
        a, b, c = (flow[i] for i in incident)
        if a ^ b ^ c:
            raise ValueError("flow conservation fails")


def local_pairs(graph: Graph, flow: tuple[int, ...]) -> dict[tuple[int, int], tuple[int, int]]:
    """The edge of the local triangle consists of the other two flows."""
    validate_flow(graph, flow)
    return {
        (v, edge_id): tuple(sorted(flow[j] for j in incident if j != edge_id))
        for v, incident in enumerate(graph.incident())
        for edge_id in incident
    }


def spanning_tree(graph: Graph, reverse: bool = False) -> tuple[tuple[int, int, int], ...]:
    incident = graph.incident()
    reached = {0}
    queue = deque([0])
    result = []
    while queue:
        u = queue.popleft()
        for edge_id in sorted(incident[u], reverse=reverse):
            a, b = graph.edges[edge_id]
            v = b if a == u else a
            if v not in reached:
                reached.add(v)
                queue.append(v)
                result.append((u, v, edge_id))
    if len(reached) != graph.vertex_count:
        raise ValueError("enumeration requires a connected graph")
    return tuple(result)


def translated(pair: tuple[int, int], value: int) -> tuple[int, int]:
    return tuple(sorted(x ^ value for x in pair))


def enumerate_lifts(graph: Graph, flow: tuple[int, ...], reverse: bool = False) -> tuple[Lift, ...]:
    local = local_pairs(graph, flow)
    tree = spanning_tree(graph, reverse)
    result = []
    for choices in product((0, 1), repeat=len(tree)):
        translations = [0] * graph.vertex_count
        for (u, v, edge_id), choice in zip(tree, choices):
            # Map one fixed endpoint at u to either endpoint at v. The second
            # endpoint then agrees because both pairs have XOR equal to f_e.
            translations[v] = translations[u] ^ local[u, edge_id][0] ^ local[v, edge_id][choice]
        pairs = []
        for edge_id, (u, v) in enumerate(graph.edges):
            pair = translated(local[u, edge_id], translations[u])
            if pair != translated(local[v, edge_id], translations[v]):
                break
            pairs.append(pair)
        else:
            result.append(Lift(tuple(translations), tuple(pairs)))
    if len(set(result)) != len(result):
        raise AssertionError("tree enumeration unexpectedly repeated a lift")
    return tuple(sorted(result, key=lambda lift: lift.translations))


def verify_cover(graph: Graph, pairs: tuple[tuple[int, int], ...], labels: int = 8) -> dict:
    if type(labels) is not int or labels < 2 or len(pairs) != len(graph.edges):
        raise ValueError("invalid label bound or pair count")
    degree: Counter = Counter()
    sizes: Counter = Counter()
    for (u, v), pair in zip(graph.edges, pairs):
        if len(pair) != 2 or pair[0] == pair[1]:
            raise ValueError("each edge must carry two distinct labels")
        if any(type(a) is not int or not 0 <= a < labels for a in pair):
            raise ValueError("label outside palette")
        for a in pair:
            degree[u, a] += 1
            degree[v, a] += 1
            sizes[a] += 1
    if any(count % 2 for count in degree.values()):
        raise ValueError("a label has odd degree at a vertex")
    return {"used_labels": len(sizes), "label_edge_counts": dict(sorted(sizes.items()))}


def verify_lift(graph: Graph, flow: tuple[int, ...], lift: Lift) -> dict:
    local = local_pairs(graph, flow)
    if len(lift.translations) != graph.vertex_count or lift.translations[0] != 0:
        raise ValueError("invalid root-fixed translations")
    if any(type(t) is not int or not 0 <= t <= 7 for t in lift.translations):
        raise ValueError("translation outside F2^3")
    result = verify_cover(graph, lift.pairs)
    for edge_id, ((u, v), pair) in enumerate(zip(graph.edges, lift.pairs)):
        if pair[0] ^ pair[1] != flow[edge_id]:
            raise ValueError("pair does not induce specified flow")
        if tuple(sorted(pair)) != translated(local[u, edge_id], lift.translations[u]):
            raise ValueError("pair disagrees with first endpoint translation")
        if tuple(sorted(pair)) != translated(local[v, edge_id], lift.translations[v]):
            raise ValueError("pair disagrees with second endpoint translation")
    return result


def verify_cycle_certificate(
    graph: Graph,
    pairs: tuple[tuple[int, int], ...],
    cycles: dict[int, tuple[int, ...]],
) -> dict[int, int]:
    """Check one written closed vertex sequence per active label against pairs."""
    counts = verify_cover(graph, pairs)
    if set(cycles) != set(counts["label_edge_counts"]):
        raise ValueError("cycle labels do not match active labels")
    combined: Counter = Counter()
    lengths = {}
    for label, vertices in cycles.items():
        if (len(vertices) < 3 or vertices[0] != vertices[-1]
                or len(set(vertices[:-1])) != len(vertices) - 1):
            raise ValueError("certificate sequence is not a closed simple cycle")
        actual = Counter(tuple(sorted((u, v))) for u, v in zip(vertices, vertices[1:]))
        expected = Counter(tuple(sorted(edge)) for edge, pair in zip(graph.edges, pairs) if label in pair)
        if actual != expected:
            raise ValueError("cycle edges do not match the label subgraph")
        combined.update(actual)
        lengths[label] = sum(actual.values())
    expected_double = Counter({edge: 2 * count for edge, count in Counter(tuple(sorted(edge)) for edge in graph.edges).items()})
    if combined != expected_double:
        raise ValueError("cycles do not double-cover every edge")
    return lengths


def reconstruct_from_cover(graph: Graph, pairs: tuple[tuple[int, int], ...]) -> tuple[tuple[int, ...], Lift]:
    """Read a flow and root-normalized lift back from labels in F2^3."""
    verify_cover(graph, pairs)
    flow = tuple(a ^ b for a, b in pairs)
    translations = []
    for incident in graph.incident():
        triangle = set(a for edge_id in incident for a in pairs[edge_id])
        if len(triangle) != 3:
            raise AssertionError("cubic even-cover incidence is not a triangle")
        a, b, c = triangle
        translations.append(a ^ b ^ c)
    gauge = translations[0]
    lift = Lift(tuple(t ^ gauge for t in translations), tuple(translated(pair, gauge) for pair in pairs))
    verify_lift(graph, flow, lift)
    return flow, lift


def coloring(pairs: tuple[tuple[int, int], ...], k: int) -> dict[int, int] | None:
    """Enumerate all partitions into at most k classes via restricted growth."""
    if type(k) is not int or k < 1:
        raise ValueError("color bound must be positive")
    labels = sorted({a for pair in pairs for a in pair})
    neighbors = {a: set() for a in labels}
    for a, b in pairs:
        if a == b:
            return None
        neighbors[a].add(b)
        neighbors[b].add(a)
    assigned: dict[int, int] = {}

    def visit(index: int, used: int) -> dict[int, int] | None:
        if index == len(labels):
            return assigned.copy()
        label = labels[index]
        forbidden = {assigned[v] for v in neighbors[label] if v in assigned}
        for color in range(min(used + 1, k)):
            if color not in forbidden:
                assigned[label] = color
                answer = visit(index + 1, max(used, color + 1))
                if answer is not None:
                    return answer
                del assigned[label]
        return None

    return visit(0, 0)


def verify_coloring(pairs: tuple[tuple[int, int], ...], colors: dict[int, int], k: int) -> None:
    for a, b in pairs:
        if a not in colors or b not in colors:
            raise ValueError("coloring omits an active label")
        if any(type(colors[x]) is not int or not 0 <= colors[x] < k for x in (a, b)):
            raise ValueError("color outside target palette")
        if colors[a] == colors[b]:
            raise ValueError("interaction endpoints share a color")


def maximum_clique(pairs: tuple[tuple[int, int], ...]) -> tuple[int, ...]:
    labels = sorted({a for pair in pairs for a in pair})
    interactions = {tuple(sorted(pair)) for pair in pairs}
    for size in range(len(labels), 0, -1):
        for vertices in combinations(labels, size):
            if all(pair in interactions for pair in combinations(vertices, 2)):
                return vertices
    return ()


def classify(graph: Graph, flow: tuple[int, ...]) -> dict:
    lifts = enumerate_lifts(graph, flow)
    records = []
    for lift in lifts:
        counts = verify_lift(graph, flow, lift)
        clique = maximum_clique(lift.pairs)
        for k in range(max(1, len(clique)), 9):
            colors = coloring(lift.pairs, k)
            if colors is not None:
                verify_coloring(lift.pairs, colors, k)
                verify_cover(graph, tuple((colors[a], colors[b]) for a, b in lift.pairs), k)
                break
        else:
            raise AssertionError("eight-label palette has no eight-coloring")
        records.append({
            "translations": lift.translations,
            "pairs": lift.pairs,
            **counts,
            "palette_edges": len(set(lift.pairs)),
            "maximum_clique": clique,
            "chromatic_number": k,
            "admits_five_colors": coloring(lift.pairs, 5) is not None,
            "optimal_coloring": colors,
        })
    return {
        "method": "direct_spanning_tree_assignments_and_set_partition_coloring",
        "root_translation": 0,
        "tree_edges": spanning_tree(graph),
        "complete_tree_assignments": 2 ** (graph.vertex_count - 1),
        "compatible_translations": len(lifts),
        "histogram": dict(sorted(Counter(record["chromatic_number"] for record in records).items())),
        "records": records,
    }


def read_record(path: Path) -> dict:
    source = json.loads(path.read_text())
    matches = [record for record in source["records"]
               if record["graph"]["name"] == "petersen-k6-palette"]
    if len(matches) != 1:
        raise ValueError("expected exactly one petersen-k6-palette record")
    return matches[0]


def load_fixture(path: Path) -> tuple[Graph, tuple[int, ...], Lift]:
    fixture = read_record(path)
    graph = Graph.read(fixture["graph"])
    witness = fixture["construction"]["witness"]
    flow = tuple(witness["flow"])
    lift = Lift(tuple(witness["translations"]), tuple(tuple(pair) for pair in witness["pairs"]))
    return graph, flow, lift


FIXTURE = Path(__file__).with_name("results.json")


class IndependentTests(unittest.TestCase):
    # Explicit certificate copied from the written table, not generated by
    # the checker being tested. The negative control substitutes a different
    # valid Petersen cycle, so merely checking closed walks cannot pass it.
    written_cycles = {
        2: (3, 4, 9, 7, 5, 8, 3),
        3: (0, 1, 2, 3, 4, 0),
        4: (1, 2, 7, 9, 6, 1),
        5: (0, 1, 6, 8, 5, 0),
        6: (0, 4, 9, 6, 8, 3, 2, 7, 5, 0),
    }

    @classmethod
    def setUpClass(cls):
        cls.graph, cls.flow, cls.fixture_lift = load_fixture(FIXTURE)
        cls.lifts = enumerate_lifts(cls.graph, cls.flow)

    def test_fixture_and_every_enumerated_lift(self):
        verify_lift(self.graph, self.flow, self.fixture_lift)
        self.assertIn(self.fixture_lift, self.lifts)
        for lift in self.lifts:
            verify_lift(self.graph, self.flow, lift)

    def test_exact_classification(self):
        result = classify(self.graph, self.flow)
        self.assertEqual(result["complete_tree_assignments"], 512)
        self.assertEqual(result["compatible_translations"], 2)
        self.assertEqual(result["histogram"], {5: 1, 6: 1})
        self.assertEqual([row["used_labels"] for row in result["records"]], [5, 6])
        self.assertEqual([row["palette_edges"] for row in result["records"]], [10, 15])

    def test_written_cycles_match_pairs_and_exact_double_edge_multiplicity(self):
        repaired = next(lift for lift in self.lifts if len({a for pair in lift.pairs for a in pair}) == 5)
        self.assertEqual(verify_cycle_certificate(self.graph, repaired.pairs, self.written_cycles),
                         {2: 6, 3: 5, 4: 5, 5: 5, 6: 9})

    def test_mutation_replaces_one_cycle_with_a_different_valid_cycle(self):
        repaired = next(lift for lift in self.lifts if len({a for pair in lift.pairs for a in pair}) == 5)
        changed = dict(self.written_cycles)
        changed[2] = changed[3]
        with self.assertRaisesRegex(ValueError, "cycle edges do not match"):
            verify_cycle_certificate(self.graph, repaired.pairs, changed)

    def test_cover_converse_and_all_global_translation_gauges(self):
        fixture = read_record(FIXTURE)
        arbitrary_five_cover = tuple(tuple(pair) for pair in fixture["unrestricted"]["5"]["witness"]["pairs"])
        all_pairs = [lift.pairs for lift in self.lifts] + [arbitrary_five_cover]
        for pairs in all_pairs:
            expected_flow, expected_lift = reconstruct_from_cover(self.graph, pairs)
            self.assertIn(expected_lift, enumerate_lifts(self.graph, expected_flow))
            for gauge in range(8):
                shifted = tuple(translated(pair, gauge) for pair in pairs)
                self.assertEqual(reconstruct_from_cover(self.graph, shifted), (expected_flow, expected_lift))

    def test_different_spanning_tree_same_complete_set(self):
        self.assertNotEqual(spanning_tree(self.graph), spanning_tree(self.graph, True))
        self.assertEqual(self.lifts, enumerate_lifts(self.graph, self.flow, True))

    def test_mutation_single_flow_edge(self):
        changed = list(self.flow)
        changed[0] ^= 1
        with self.assertRaisesRegex(ValueError, "conservation"):
            enumerate_lifts(self.graph, tuple(changed))

    def test_mutation_zero_flow(self):
        changed = list(self.flow)
        changed[0] = 0
        with self.assertRaisesRegex(ValueError, "nonzero"):
            enumerate_lifts(self.graph, tuple(changed))

    def test_mutation_single_vertex_translation(self):
        changed = list(self.fixture_lift.translations)
        changed[1] ^= 1
        with self.assertRaisesRegex(ValueError, "translation"):
            verify_lift(self.graph, self.flow, Lift(tuple(changed), self.fixture_lift.pairs))

    def test_mutation_equal_pair_labels(self):
        changed = list(self.fixture_lift.pairs)
        changed[0] = (changed[0][0], changed[0][0])
        with self.assertRaisesRegex(ValueError, "distinct"):
            verify_cover(self.graph, tuple(changed))

    def test_mutation_pair_breaks_parity(self):
        changed = list(self.fixture_lift.pairs)
        changed[0] = (0, changed[0][1])
        with self.assertRaisesRegex(ValueError, "odd degree"):
            verify_cover(self.graph, tuple(changed))

    def test_mutation_coloring_collision(self):
        colors = {label: label for pair in self.fixture_lift.pairs for label in pair}
        a, b = self.fixture_lift.pairs[0]
        colors[a] = colors[b]
        with self.assertRaisesRegex(ValueError, "share a color"):
            verify_coloring(self.fixture_lift.pairs, colors, 8)

    def test_mutation_graph_loop_and_wrong_degree(self):
        data = {"vertex_count": self.graph.vertex_count, "edges": list(self.graph.edges)}
        data["edges"][0] = (0, 0)
        with self.assertRaisesRegex(ValueError, "loop"):
            Graph.read(data)
        data["edges"] = list(self.graph.edges[1:])
        with self.assertRaisesRegex(ValueError, "cubic"):
            Graph.read(data)

    def test_mutation_wrong_flow_for_a_valid_cover(self):
        fixture = read_record(FIXTURE)
        pairs = tuple(tuple(pair) for pair in fixture["unrestricted"]["5"]["witness"]["pairs"])
        _, lift = reconstruct_from_cover(self.graph, pairs)
        with self.assertRaisesRegex(ValueError, "specified flow"):
            verify_lift(self.graph, self.flow, lift)

    def test_mutation_root_and_label_bounds(self):
        translations = list(self.fixture_lift.translations)
        translations[0] = 1
        with self.assertRaisesRegex(ValueError, "root-fixed"):
            verify_lift(self.graph, self.flow, Lift(tuple(translations), self.fixture_lift.pairs))
        pairs = list(self.fixture_lift.pairs)
        pairs[0] = (8, pairs[0][1])
        with self.assertRaisesRegex(ValueError, "outside palette"):
            verify_cover(self.graph, tuple(pairs))

    def test_coloring_canonical_positive_and_negative_controls(self):
        triangle = ((0, 1), (1, 2), (0, 2))
        pentagon = ((0, 1), (1, 2), (2, 3), (3, 4), (4, 0))
        complete6 = tuple(combinations(range(6), 2))
        self.assertIsNone(coloring(triangle, 2))
        self.assertIsNotNone(coloring(triangle, 3))
        self.assertIsNone(coloring(pentagon, 2))
        verify_coloring(pentagon, coloring(pentagon, 3), 3)
        self.assertIsNone(coloring(complete6, 5))
        verify_coloring(complete6, coloring(complete6, 6), 6)
        self.assertEqual(maximum_clique(complete6), tuple(range(6)))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--flow-json", type=Path, help="JSON array overriding the fixture flow")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(IndependentTests)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        sys.exit(not result.wasSuccessful())
    graph, flow, fixture_lift = load_fixture(args.fixture)
    if args.flow_json:
        flow = tuple(json.loads(args.flow_json.read_text()))
    else:
        verify_lift(graph, flow, fixture_lift)
    report = classify(graph, flow)
    if enumerate_lifts(graph, flow) != enumerate_lifts(graph, flow, True):
        raise ValueError("the two spanning-tree enumerations disagree")
    report["independent_second_tree_agrees"] = True
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
