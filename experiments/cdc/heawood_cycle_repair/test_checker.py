"""Independent replay and corrupted-certificate controls, including Python -O."""
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from .checker import chromatic, read_json, verify


HERE = Path(__file__).parent
SOURCE = HERE.parent/'heawood'/'certificate.json'


class CheckerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = read_json(HERE/'certificate.json')

    def test_complete_independent_replay(self):
        result = verify(self.data, SOURCE)
        self.assertEqual(result['admissible_changes'], 199)
        self.assertEqual(result['minimum_palette_histogram'], {4: 72, 5: 96, 7: 31})
        self.assertEqual(result['root_fixed_lift_count_histogram'], {1: 96, 2: 67, 4: 36})

    def test_coloring_is_not_just_clique_number(self):
        self.assertEqual(chromatic(tuple(combinations(range(7), 2))), 7)
        self.assertEqual(chromatic(((0, 1), (0, 4), (1, 2), (2, 3), (3, 4))), 3)
        self.assertEqual(chromatic(((0, 1), (1, 2), (2, 3))), 2)

    def test_minimum_repair_artifact_matches_full_certificate(self):
        artifact = read_json(HERE/'minimum-repair.json')
        self.assertIn(artifact['record'], self.data['records'])
        self.assertEqual(len(artifact['record']['cycle_edges']), 6)
        self.assertEqual(artifact['record']['minimum_palette_chromatic_number'], 4)
        self.assertEqual(artifact['girth'], min(map(len, self.data['simple_cycles'])))
        self.assertEqual(artifact['minimum_changed_edges_among_distinct_conservative_flows'], 6)

    def test_mutations_reject(self):
        mutations = [
            (('complete',), False),
            (('total_admissible_changes',), 198),
            (('completed_changes',), 198),
            (('simple_cycles',), self.data['simple_cycles'][:-1]),
            (('records',), self.data['records'][:-1]),
            (('records', 1), self.data['records'][0]),
            (('original_flow', 0), 0),
            (('records', 0, 'delta'), 0),
            (('records', 0, 'delta'), True),
            (('records', 0, 'flow', 0), 0),
            (('records', 0, 'root_fixed_translations'), []),
            (('records', 0, 'root_fixed_translations', 0, 0), 1),
            (('records', 0, 'palette_chromatic_numbers', 0), 1),
            (('records', 0, 'minimum_palette_chromatic_number'), 1),
            (('records', 0, 'best_lift', 'pairs', 0), [0, 0]),
            (('records', 0, 'best_lift', 'clique'), [0, 0]),
            (('records', 0, 'best_lift', 'coloring'), {}),
            (('minimum_palette_histogram', '4'), 73),
            (('successful_changes_to_five',), 199),
            (('shortest_successful_cycle_length',), 4),
        ]
        for path, value in mutations:
            with self.subTest(path=path):
                changed = deepcopy(self.data)
                target = changed
                for key in path[:-1]:
                    target = target[key]
                target[path[-1]] = value
                with self.assertRaises(ValueError):
                    verify(changed, SOURCE)

    def test_source_pin_and_duplicate_json_keys(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'input.json'
            path.write_bytes(SOURCE.read_bytes()+b'\n')
            with self.assertRaisesRegex(ValueError, 'pin'):
                verify(self.data, path)
            path.write_text('{"a":1,"a":2}')
            with self.assertRaisesRegex(ValueError, 'duplicate'):
                read_json(path)

    def test_optimized_cli_positive_and_negative(self):
        good = subprocess.run([sys.executable, '-O', str(HERE/'checker.py')],
                              capture_output=True, text=True)
        self.assertEqual(good.returncode, 0, good.stderr)
        self.assertEqual(json.loads(good.stdout)['status'], 'verified')
        with tempfile.TemporaryDirectory() as directory:
            changed = deepcopy(self.data)
            changed['records'].pop()
            path = Path(directory)/'incomplete.json'
            path.write_text(json.dumps(changed))
            bad = subprocess.run([sys.executable, '-O', str(HERE/'checker.py'),
                                  '--certificate', str(path)], capture_output=True, text=True)
            self.assertNotEqual(bad.returncode, 0)
            self.assertEqual(json.loads(bad.stdout)['status'], 'not_verified')


if __name__ == '__main__':
    unittest.main()
