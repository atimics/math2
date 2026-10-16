"""Direct positive witness and meaningful corruption controls."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from .witness import verify

HERE = Path(__file__).parent
SOURCE = HERE.parent/'heawood'/'certificate.json'


class WitnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((HERE/'three-step-experiment.json').read_text())

    def test_three_step_repair(self):
        result = verify(self.data, SOURCE)
        self.assertEqual(result['cycle_lengths'], [6, 10, 6])
        self.assertEqual(result['deltas'], [3, 4, 5])
        self.assertEqual(result['final_labels'], [1, 2, 3])
        self.assertEqual(result['cover_cycle_lengths'], [14, 14, 14])

    def test_corruptions(self):
        mutations = [
            (('steps',), self.data['steps'][:-1]),
            (('steps', 0, 'delta'), 0),
            (('steps', 0, 'delta'), True),
            (('steps', 0, 'delta'), 1),  # zero on edge 6
            (('steps', 0, 'cycle_edges'), [6, 8]),
            (('steps', 0, 'cycle_edges'), [6, 8, 16, 17, 18, 18]),
            (('steps', 0, 'cycle_edges', 0), -1),
            (('steps', 0, 'flow', 0), 0),
            (('steps', 0, 'flow', 0), True),
            (('final_flow', 0), 7),
        ]
        for path, value in mutations:
            with self.subTest(path=path, value=value):
                data = deepcopy(self.data)
                target = data
                for key in path[:-1]:
                    target = target[key]
                target[path[-1]] = value
                with self.assertRaises(ValueError):
                    verify(data, SOURCE)

    def test_source_pin(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'source.json'
            path.write_bytes(SOURCE.read_bytes()+b'\n')
            with self.assertRaisesRegex(ValueError, 'pin'):
                verify(self.data, path)

    def test_optimized_cli_rejects_illegal_path(self):
        with tempfile.TemporaryDirectory() as directory:
            bad = deepcopy(self.data)
            bad['steps'][0]['delta'] = 1
            path = Path(directory)/'bad.json'
            path.write_text(json.dumps(bad))
            proc = subprocess.run([sys.executable, '-O', str(HERE/'witness.py'),
                                   '--source', str(SOURCE), '--witness', str(path)],
                                  capture_output=True, text=True)
            self.assertNotEqual(proc.returncode, 0)
            self.assertEqual(json.loads(proc.stdout)['status'], 'not_verified')


if __name__ == '__main__':
    unittest.main()
