"""Controls for the independent structural proof, including a repairable flow."""
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from . import review_check as check

HERE = Path(__file__).parent
SOURCE = HERE.parent/'heawood'/'certificate.json'


class StructuralTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads(SOURCE.read_text())
        cls.n = cls.source['graph']['vertex_count']
        cls.edges = cls.source['graph']['edges']
        cls.even, cls.cycles = check.cycle_space(cls.n, cls.edges)

    def test_complete_receipt(self):
        result = check.verify(SOURCE)
        self.assertEqual(result['even_supports'], 256)
        self.assertEqual(result['simple_cycles'], 213)
        self.assertEqual(result['perfect_matchings'], 24)
        self.assertEqual(result['hamiltonian_matching_complements'], 24)
        self.assertEqual(result['legal_first_moves'], 199)
        self.assertEqual(result['first_flow_nonempty_projections'], 1393)
        self.assertEqual(result['simple_projection_barriers'], 739)
        self.assertEqual(result['simple_projection_barriers_by_functional'],
                         {1: 92, 2: 95, 3: 95, 4: 178, 5: 95, 6: 92, 7: 92})
        self.assertFalse(result['discovery_palette_histogram_verified'])

    def test_cycle_space_and_matchings_against_literal_subsets(self):
        edges = list(combinations(range(4), 2))
        even, cycles = check.cycle_space(4, edges)
        expected_even, expected_matchings = set(), set()
        for mask in range(1 << len(edges)):
            selected = tuple(e for e in range(len(edges)) if mask & (1 << e))
            degrees = [sum(v in edges[e] for e in selected) for v in range(4)]
            if all(d % 2 == 0 for d in degrees):
                expected_even.add(selected)
            if degrees == [1]*4:
                expected_matchings.add(selected)
        self.assertEqual(set(even), expected_even)
        self.assertEqual(set(cycles), expected_even-{()})
        self.assertEqual(set(check.perfect_matchings(4, edges)), expected_matchings)

    def test_hamiltonian_hypothesis_has_a_failure_control(self):
        # The triangular prism has a 2-factor consisting of two disjoint triangles.
        edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 4),
                 (2, 5), (3, 4), (3, 5), (4, 5)]
        matchings = check.perfect_matchings(6, edges)
        counts = [len(check.components(6, edges, set(range(9))-set(m))) for m in matchings]
        self.assertIn(2, counts)

    def test_missing_or_duplicate_cycles_are_rejected(self):
        for cycles in (self.cycles[1:], self.cycles+(self.cycles[0],)):
            with self.subTest(length=len(cycles)), self.assertRaises(ValueError):
                check.projection_barriers(self.n, self.edges, self.source['flow'], cycles)

    def test_rank_two_and_repairable_flows_fail_barrier(self):
        with self.assertRaisesRegex(ValueError, 'original flow has rank at most two'):
            check.projection_barriers(self.n, self.edges, self.source['comparator']['flow'], self.cycles)
        witness = json.loads((HERE/'three-step-experiment.json').read_text())
        # The first intermediate needs exactly the two remaining legal moves.
        with self.assertRaisesRegex(ValueError, 'unblocked simple projection'):
            check.projection_barriers(self.n, self.edges, witness['steps'][0]['flow'], self.cycles)
        # The second intermediate has a legal one-cycle rank reduction.
        with self.assertRaisesRegex(ValueError, 'single-cycle rank reduction'):
            check.projection_barriers(self.n, self.edges, witness['steps'][1]['flow'], self.cycles)

    def test_flow_and_graph_validation(self):
        for value in (0, True, 8, 2):
            flow = self.source['flow'].copy()
            flow[0] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                check.validate_flow(self.n, self.edges, flow)
        for n, edges in ((0, []), (2, [(0, 0)]), (2, [(1, 0)]),
                         (2, [(0, 1), (0, 1)]), (2, [(0, 2)]), (2, [(0, True)])):
            with self.subTest(edges=edges), self.assertRaises(ValueError):
                check.incidence(n, edges)
        with self.assertRaisesRegex(ValueError, 'not cubic'):
            check.cycle_space(2, [(0, 1)])

    def test_source_pin_duplicate_keys_and_optimized_failure(self):
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            json.loads('{"a":1,"a":2}', object_pairs_hook=check.unique_object)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'source.json'
            path.write_bytes(SOURCE.read_bytes()+b'\n')
            with self.assertRaisesRegex(ValueError, 'pin'):
                check.verify(path)
            result = subprocess.run([sys.executable, '-O', str(HERE/'review_check.py'),
                                     '--source', str(path)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(json.loads(result.stdout)['status'], 'not_verified')


if __name__ == '__main__':
    unittest.main()
