"""Public-layout integration plus the independent enumerator's regressions."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

try:
    from .affine_lifts import FIXTURE, IndependentTests, load_fixture
except ImportError:
    from affine_lifts import FIXTURE, IndependentTests, load_fixture


class SourceRecordTests(unittest.TestCase):
    def test_reuses_exact_named_predecessor_record(self):
        graph, flow, lift = load_fixture(FIXTURE)
        self.assertEqual(graph.vertex_count, 10)
        self.assertEqual(flow, (6, 5, 3, 7, 1, 5, 2, 1, 4, 4, 4, 7, 3, 2, 6))
        self.assertEqual(lift.translations, (0, 4, 0, 3, 2, 2, 0, 3, 5, 5))

    def test_missing_or_duplicate_record_rejected(self):
        source = json.loads(FIXTURE.read_text())
        record = next(r for r in source["records"]
                      if r["graph"]["name"] == "petersen-k6-palette")
        with TemporaryDirectory() as directory:
            path = Path(directory) / "results.json"
            for records in ([], [record, record]):
                with self.subTest(count=len(records)):
                    path.write_text(json.dumps({**source, "records": records}))
                    with self.assertRaisesRegex(ValueError, "exactly one"):
                        load_fixture(path)
