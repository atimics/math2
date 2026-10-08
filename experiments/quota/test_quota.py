"""Independent exhaustive and adversarial checks of the quota reductions."""
import itertools
import random
import unittest

import networkx as nx

from gadgets import decode_matching, reduce_graph


def brute_factor(n, edges, quotas):
    """Enumerate host edge subsets; never consult the gadget construction."""
    for mask in range(1 << len(edges)):
        degrees = [0] * n
        selected = []
        for i, (u, v) in enumerate(edges):
            if mask & (1 << i):
                degrees[u] += 1
                degrees[v] += 1
                selected.append((u, v))
        if degrees == list(quotas):
            return selected
    return None


def check_host(n, edges, quotas, selected):
    allowed = {tuple(sorted(e)) for e in edges}
    seen = set()
    degrees = [0] * n
    for u, v in selected:
        edge = tuple(sorted((u, v)))
        if edge not in allowed or edge in seen:
            raise AssertionError("absent or repeated host edge")
        seen.add(edge)
        degrees[u] += 1
        degrees[v] += 1
    if degrees != list(quotas):
        raise AssertionError("decoded host degrees differ from quotas")


class QuotaTests(unittest.TestCase):
    def solve_and_check(self, n, edges, quotas, mode):
        reduced = reduce_graph(n, edges, quotas, mode)
        size = reduced["vertex_count"]
        gadget_edges = reduced["edges"]
        self.assertEqual(len(gadget_edges), len(set(gadget_edges)))
        self.assertTrue(all(0 <= u < v < size for u, v in gadget_edges))
        graph = nx.Graph()
        graph.add_nodes_from(range(size))
        graph.add_edges_from(gadget_edges)
        matching = nx.max_weight_matching(graph, maxcardinality=True)
        feasible = len(matching) * 2 == size
        expected = brute_factor(n, edges, quotas)
        self.assertEqual(feasible, expected is not None, (n, edges, quotas, mode))
        if feasible:
            # Explicitly validate perfect coverage before trusting the decoder.
            coverage = [0] * size
            for u, v in matching:
                self.assertIn(tuple(sorted((u, v))), set(gadget_edges))
                coverage[u] += 1
                coverage[v] += 1
            self.assertEqual(coverage, [1] * size)
            selected = decode_matching(reduced, matching)
            check_host(n, edges, quotas, selected)
        else:
            with self.assertRaises(ValueError):
                decode_matching(reduced, matching)

    def test_all_graphs_and_quotas_through_three_vertices(self):
        for n in range(4):
            possible = list(itertools.combinations(range(n), 2))
            for mask in range(1 << len(possible)):
                edges = [e for i, e in enumerate(possible) if mask & (1 << i)]
                degrees = [sum(v in e for e in edges) for v in range(n)]
                for quotas in itertools.product(*(range(d + 1) for d in degrees)):
                    for mode in ("dense", "network", "hybrid"):
                        with self.subTest(n=n, edges=edges, quotas=quotas, mode=mode):
                            self.solve_and_check(n, edges, quotas, mode)

    def test_seeded_graphs_against_brute_force(self):
        rng = random.Random(20261008)
        for case in range(30):
            n = rng.randrange(4, 8)
            possible = list(itertools.combinations(range(n), 2))
            rng.shuffle(possible)
            edges = sorted(possible[:rng.randrange(min(12, len(possible)) + 1)])
            degrees = [sum(v in e for e in edges) for v in range(n)]
            if case % 2 == 0:
                chosen = [e for e in edges if rng.randrange(2)]
                quotas = [sum(v in e for e in chosen) for v in range(n)]
            else:
                quotas = [rng.randrange(d + 1) for d in degrees]
            for mode in ("dense", "network", "hybrid"):
                with self.subTest(case=case, mode=mode):
                    self.solve_and_check(n, edges, quotas, mode)

    def test_network_single_position_zero_and_full_quota(self):
        for quotas in ([0, 0], [1, 1], [0, 1]):
            self.solve_and_check(2, [(0, 1)], quotas, "network")

    def test_non_power_of_two_network_degree(self):
        edges = [(0, 1), (0, 2), (0, 3)]
        for leaves in itertools.product(range(2), repeat=3):
            for center in range(4):
                self.solve_and_check(4, edges, (center,) + leaves, "network")

    def test_triangle_odd_quotas_infeasible(self):
        for mode in ("dense", "network", "hybrid"):
            self.solve_and_check(3, [(0, 1), (0, 2), (1, 2)], [1, 1, 1], mode)

    def test_hybrid_uses_both_gadgets_and_minimizes_local_size(self):
        # Degree 128, zero quota: dense center costs more than the network;
        # degree-one leaves use dense gadgets. Compare aggregate V+E too.
        edges = [(0, v) for v in range(1, 129)]
        quotas = [0] * 129
        results = {mode: reduce_graph(129, edges, quotas, mode)
                   for mode in ("dense", "network", "hybrid")}
        self.assertEqual(results["hybrid"]["choices"][0], "network")
        self.assertEqual(set(results["hybrid"]["choices"][1:]), {"dense"})
        cost = lambda r: r["vertex_count"] + len(r["edges"])
        self.assertLess(cost(results["hybrid"]), cost(results["dense"]))
        self.assertLess(cost(results["hybrid"]), cost(results["network"]))

    def test_reject_invalid_graphs(self):
        bad = [(True, [], []), (-1, [], []), (2, [(0, 0)], [0, 0]),
               (2, [(0, 2)], [0, 0]), (2, [(False, 1)], [0, 0]),
               (2, [(0, 1), (1, 0)], [1, 1]),
               (2, [(0, 1, 2)], [1, 1]), (2, [None], [0, 0])]
        for n, edges, quotas in bad:
            with self.subTest(n=n, edges=edges), self.assertRaises(ValueError):
                reduce_graph(n, edges, quotas)

    def test_reject_invalid_quotas_and_mode(self):
        for quotas in ([1], [True, 0], [-1, 0], [2, 0], [0.0, 0]):
            with self.subTest(quotas=quotas), self.assertRaises(ValueError):
                reduce_graph(2, [(0, 1)], quotas)
        with self.assertRaises(ValueError):
            reduce_graph(2, [(0, 1)], [1, 1], "unknown")

    def test_decoder_rejects_invalid_witnesses(self):
        reduced = reduce_graph(2, [(0, 1)], [1, 1], "dense")
        for matching in ([], [(0, 1), (1, 0)], [(0, 0)], [(0, 2)],
                         [(False, 1)], [(0, 1, 2)], [None]):
            with self.subTest(matching=matching), self.assertRaises(ValueError):
                decode_matching(reduced, matching)
        self.assertEqual(decode_matching(reduced, [(1, 0)]), [(0, 1)])

    def test_independent_host_checker_rejects_bad_outputs(self):
        for selected in ([], [(0, 1), (0, 1)], [(0, 2)]):
            with self.subTest(selected=selected), self.assertRaises(AssertionError):
                check_host(2, [(0, 1)], [1, 1], selected)


if __name__ == "__main__":
    unittest.main()
