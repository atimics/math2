"""Exact finite-kernel and deterministic budget checks; no frequency claims."""
import itertools
import math
import random
import unittest
from decimal import Decimal, localcontext
from fractions import Fraction

from sampler import budget, prepare_graph, run_steps, sample_graph, trade
from experiments.curveball.benchmark import verify_degrees


def realizations(degrees):
    n = len(degrees)
    possible = list(itertools.combinations(range(n), 2))
    states = []
    for edges in itertools.combinations(possible, sum(degrees) // 2):
        counts = [0] * n
        for u, v in edges:
            counts[u] += 1
            counts[v] += 1
        if counts == list(degrees):
            states.append(frozenset(edges))
    return states


def edge_set(adj):
    return frozenset((u, v) for u, neighbors in enumerate(adj)
                     for v in neighbors if u < v)


class ScriptedRandom:
    """Choose one prescribed pair and one prescribed heat-bath subset."""
    def __init__(self, pair, subset):
        self.pair, self.subset = pair, subset
        self.calls = 0

    def sample(self, population, k):
        self.calls += 1
        result = self.pair if self.calls == 1 else self.subset
        if len(result) != k or len(set(result)) != k:
            raise AssertionError("invalid scripted sample")
        if not set(result) <= set(population):
            raise AssertionError("scripted sample outside population")
        if self.calls > 2:
            raise AssertionError("unexpected random choice")
        return list(result)


def oracle_row(state, states, n):
    """Enumerate every realization in each pair fiber, not local trade logic."""
    row = {target: Fraction(0) for target in states}
    pairs = list(itertools.combinations(range(n), 2))
    for u, v in pairs:
        fixed = frozenset(e for e in state if (u not in e and v not in e)
                          or e == (u, v))
        fiber = [target for target in states
                 if frozenset(e for e in target if (u not in e and v not in e)
                              or e == (u, v)) == fixed]
        for target in fiber:
            row[target] += Fraction(1, len(pairs) * len(fiber))
    return row


def implemented_row(state, states, n):
    row = {target: Fraction(0) for target in states}
    pairs = list(itertools.combinations(range(n), 2))
    for u, v in pairs:
        original = prepare_graph(n, state)
        # Enumerate all subsets of the incident single-neighbor union.
        singleton = sorted(w for w in range(n) if w not in (u, v)
                           and ((w in original[u]) != (w in original[v])))
        count_left = sum(w in original[u] for w in singleton)
        assignments = list(itertools.combinations(singleton, count_left))
        for subset in assignments:
            adj = [set(neighbors) for neighbors in original]
            changed = trade(adj, ScriptedRandom((u, v), subset))
            target = edge_set(adj)
            if target not in row:
                raise AssertionError("trade left the realization space")
            if changed != (target != state):
                raise AssertionError("incorrect changed flag")
            if [len(a) for a in adj] != [len(a) for a in original]:
                raise AssertionError("trade changed degrees")
            if any(i in a or any(i not in adj[j] for j in a)
                   for i, a in enumerate(adj)):
                raise AssertionError("trade broke simple undirected adjacency")
            row[target] += Fraction(1, len(pairs) * len(assignments))
    return row


class CurveballTests(unittest.TestCase):
    def test_independent_output_verifier_rejects_corruption(self):
        original = [[0, 1], [1, 2]]
        self.assertTrue(verify_degrees(3, original, original))
        for output in ([[0, 1]], [[0, 1], [0, 2]], [[0, 1], [0, 1]],
                       [[0, 1], [1, 1]], [[0, 1], [1, 3]], [[False, 1], [1, 2]]):
            with self.subTest(output=output), self.assertRaises(ValueError):
                verify_degrees(3, original, output)

    def test_exact_transition_kernel_on_regular_and_irregular_spaces(self):
        for degrees in ((2,) * 5, (2,) * 6, (2, 2, 2, 1, 1),
                        (3, 2, 2, 2, 1, 2)):
            states = realizations(degrees)
            self.assertGreater(len(states), 1)
            matrix = {}
            for state in states:
                row = implemented_row(state, states, len(degrees))
                self.assertEqual(row, oracle_row(state, states, len(degrees)))
                self.assertEqual(sum(row.values()), Fraction(1))
                self.assertGreater(row[state], 0)
                matrix[state] = row
            for source in states:
                for target in states:
                    self.assertEqual(matrix[source][target], matrix[target][source])
            # Check connectivity directly, without assuming the gap theorem.
            visited, pending = {states[0]}, [states[0]]
            while pending:
                source = pending.pop()
                for target, probability in matrix[source].items():
                    if probability and target not in visited:
                        visited.add(target)
                        pending.append(target)
            self.assertEqual(visited, set(states))

    def test_pair_orientation_has_identical_transition_law(self):
        state = frozenset([(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)])
        for u, v in itertools.combinations(range(5), 2):
            outcomes = []
            for pair in ((u, v), (v, u)):
                adj = prepare_graph(5, state)
                left = adj[pair[0]] - adj[pair[1]] - {pair[1]}
                right = adj[pair[1]] - adj[pair[0]] - {pair[0]}
                row = {}
                subsets = list(itertools.combinations(sorted(left | right), len(left)))
                for subset in subsets:
                    candidate = [set(a) for a in adj]
                    trade(candidate, ScriptedRandom(pair, subset))
                    target = edge_set(candidate)
                    row[target] = row.get(target, Fraction(0)) + Fraction(1, len(subsets))
                outcomes.append(row)
            self.assertEqual(*outcomes)

    def test_budget_satisfies_integer_and_decimal_certificate(self):
        with localcontext() as context:
            context.prec = 80
            for n in range(2, 21):
                pairs = math.comb(n, 2)
                for m in sorted({0, 1, pairs // 2, pairs - 1, pairs}):
                    universe = math.comb(pairs, m)
                    bits = (universe - 1).bit_length()
                    self.assertLessEqual(universe, 1 << bits)
                    for k in (1, 2, 7, 20):
                        steps = budget(n, m, k)
                        if universe == 1:
                            self.assertEqual(steps, 0)
                            continue
                        # Integer inequality establishing the conservative ceiling.
                        self.assertGreaterEqual(20 * steps,
                                                7 * pairs * (bits + 2 * k - 2))
                        bound = Decimal(universe).sqrt() / 2 * (
                            -Decimal(steps) / Decimal(pairs)).exp()
                        self.assertLessEqual(bound, Decimal(2) ** (-k))

    def test_run_steps_exact_count_and_degree_invariance(self):
        adj = prepare_graph(5, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)])
        original = [len(a) for a in adj]
        changed = run_steps(adj, 100, random.Random(17))
        self.assertTrue(0 <= changed <= 100)
        self.assertEqual([len(a) for a in adj], original)
        self.assertEqual(run_steps(adj, 0, random.Random(17)), 0)

    def test_full_budget_sample_and_diagnostic_metadata(self):
        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
        for seed in (None, 17):
            result = sample_graph(5, edges, k=7, seed=seed)
            adj = prepare_graph(5, result["edges"])
            self.assertEqual([len(a) for a in adj], [2] * 5)
            self.assertEqual(result["steps"], budget(5, 5, 7))
            cert = result["certificate"]
            self.assertTrue(cert["conditional"])
            self.assertEqual(cert["tv_bound"], "2^-7")
            self.assertEqual(cert["seeded_diagnostic"], seed is not None)
            self.assertIn("not joint independence", cert["scope"])
        self.assertEqual(sample_graph(5, edges, seed=17),
                         sample_graph(5, edges, seed=17))

    def test_trivial_spaces(self):
        for n, edges in ((0, []), (1, []), (2, []), (2, [(0, 1)]),
                         (4, list(itertools.combinations(range(4), 2)))):
            result = sample_graph(n, edges, seed=1)
            self.assertEqual(result["steps"], 0)
            self.assertEqual(edge_set(prepare_graph(n, result["edges"])),
                             edge_set(prepare_graph(n, edges)))

    def test_bad_graph_inputs(self):
        for n, edges in ((True, []), (-1, []), (2, [(0, 0)]),
                         (2, [(0, 2)]), (2, [(False, 1)]),
                         (2, [(0, 1), (1, 0)]), (2, [(0, 1, 2)]),
                         (2, [None]), (2, [(0.0, 1)])):
            with self.subTest(n=n, edges=edges), self.assertRaises(ValueError):
                prepare_graph(n, edges)

    def test_bad_budget_and_step_inputs(self):
        for args in ((-1, 0, 7), (True, 0, 7), (2, 2, 7),
                     (2, -1, 7), (2, True, 7), (2, 1, 0),
                     (2, 1, True), (2, 1, 1.5)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                budget(*args)
        for steps in (-1, True, 1.5):
            with self.subTest(steps=steps), self.assertRaises(ValueError):
                run_steps([], steps, random.Random(1))


if __name__ == "__main__":
    unittest.main()
