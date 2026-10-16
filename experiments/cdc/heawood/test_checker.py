from copy import deepcopy
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest

from experiments.cdc.heawood import checker


class CertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = json.loads(Path(checker.__file__).with_name('certificate.json').read_text())

    def test_exact_obstruction_and_different_flow_cover(self):
        result = checker.verify(self.certificate)
        self.assertEqual(result['palette_chromatic_numbers'], [7, 7])
        self.assertEqual(result['all_lifts_including_global_translates'], 16)
        self.assertEqual(result['different_flow_cover_labels'], 3)

    def test_independent_review_inputs_agree_with_certificate(self):
        folder = Path(checker.__file__).parent
        benchmark = json.loads((folder / 'benchmark.json').read_text())
        comparator = json.loads((folder / 'comparator.json').read_text())
        self.assertEqual(self.certificate['graph'], benchmark['graph'])
        self.assertEqual(self.certificate['flow'], benchmark['records'][0]['flow'])
        self.assertEqual(self.certificate['lifts'], benchmark['records'][0]['lifts'])
        self.assertEqual(self.certificate['comparator'], comparator)

    def test_omitted_duplicate_and_corrupted_lift(self):
        for mutation in ('omit', 'duplicate', 'translation', 'pair'):
            data = deepcopy(self.certificate)
            if mutation == 'omit': data['lifts'].pop()
            if mutation == 'duplicate': data['lifts'][1] = deepcopy(data['lifts'][0])
            if mutation == 'translation': data['lifts'][0]['translations'][1] ^= 1
            if mutation == 'pair': data['lifts'][0]['pairs'][0][0] ^= 1
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                checker.verify(data)

    def test_graph_and_flow_corruption(self):
        for mutation in ('graph', 'flow'):
            data = deepcopy(self.certificate)
            if mutation == 'graph': data['graph']['edges'][0][1] = 7
            else: data['flow'][0] = 4
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                checker.verify(data)

    def test_clique_and_coloring_controls(self):
        for mutation in ('clique', 'coloring', 'number'):
            data = deepcopy(self.certificate)
            if mutation == 'clique': data['lifts'][0]['clique'][-1] = data['lifts'][0]['clique'][0]
            if mutation == 'coloring': data['lifts'][0]['coloring'] = {str(i): 0 for i in range(8)}
            if mutation == 'number': data['lifts'][0]['chromatic_number'] = 6
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                checker.verify(data)

    def test_comparator_corruption(self):
        data = deepcopy(self.certificate)
        data['comparator']['flow'][0] = 4
        with self.assertRaises(ValueError): checker.verify(data)

    def test_invalid_schema(self):
        data = deepcopy(self.certificate)
        data['schema_version'] = 0
        with self.assertRaises(ValueError): checker.verify(data)

    def test_cli_and_negative_control_with_optimization(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'certificate.json'
            data = deepcopy(self.certificate)
            data['lifts'].pop()
            path.write_text(json.dumps(data))
            for options in ([], ['-O']):
                good = subprocess.run([sys.executable, *options, '-m', checker.__name__], capture_output=True, text=True)
                bad = subprocess.run([sys.executable, *options, '-m', checker.__name__, '--certificate', str(path)], capture_output=True, text=True)
                self.assertEqual(good.returncode, 0, good.stdout + good.stderr)
                self.assertEqual(bad.returncode, 1, bad.stdout + bad.stderr)
                self.assertEqual(json.loads(bad.stdout)['status'], 'not_verified')


if __name__ == '__main__':
    unittest.main()
