"""All-flow coverage, exact witnesses, and failure controls; stdlib only."""
from copy import deepcopy
from itertools import product
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

try:
    from .affine_lifts import Graph, load_fixture, FIXTURE
    from .all_flows import (enumerate_flows, normalize_flow, count_by_subsets,
                           linear_maps, build_certificate, verify_certificate)
except ImportError:
    from affine_lifts import Graph, load_fixture, FIXTURE
    from all_flows import (enumerate_flows, normalize_flow, count_by_subsets,
                          linear_maps, build_certificate, verify_certificate)


class AllFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph, cls.old_flow, _ = load_fixture(FIXTURE)
        cls.data = build_certificate(cls.graph)

    def test_theta_against_direct_assignments(self):
        graph = Graph.read({"vertex_count": 2, "edges": [[0, 1]] * 3})
        flows = tuple(enumerate_flows(graph))
        expected = {f for f in product(range(1, 8), repeat=3) if f[0] ^ f[1] ^ f[2] == 0}
        self.assertEqual(len(flows), 42)
        self.assertEqual(set(flows), expected)
        self.assertEqual({normalize_flow(f) for f in flows}, {(1, 2, 3)})
        self.assertEqual(count_by_subsets(graph, 8), 42)

    def test_normalization_and_all_linear_maps(self):
        normalized = normalize_flow(self.old_flow)
        relation = {**dict(zip(self.old_flow, normalized)), 0: 0}
        self.assertEqual(len(relation), 8)
        self.assertTrue(all(relation[a ^ b] == relation[a] ^ relation[b]
                            for a, b in product(range(8), repeat=2)))
        self.assertEqual(normalize_flow(normalized), normalized)
        maps = linear_maps()
        self.assertEqual(len(maps), 168)
        self.assertEqual(len(set(maps)), 168)
        for mapping in maps:
            self.assertEqual(set(mapping), set(range(8)))
            self.assertTrue(all(mapping[a ^ b] == mapping[a] ^ mapping[b]
                                for a, b in product(range(8), repeat=2)))
            self.assertEqual(normalize_flow(tuple(mapping[x] for x in self.old_flow)), normalized)
        for invalid in [(8,), (-1,), (True,)]:
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                normalize_flow(invalid)

    def test_complete_certificate_and_saved_artifact(self):
        report = verify_certificate(self.graph, self.data)
        self.assertEqual((report["flows"], report["orbits"],
                          report["root_fixed_lifts_across_representatives"]), (28560, 170, 280))
        self.assertEqual(report["lift_used_label_histogram"], {5: 250, 6: 30})
        self.assertTrue(report["all_flows_have_five_label_lift"])
        self.assertEqual(count_by_subsets(self.graph, 4), 0)
        self.assertEqual(self.data, json.loads(Path(__file__).with_name("all_flows.json").read_text()))

    def test_certificate_failure_controls(self):
        controls = [("omit_orbit", "coverage"), ("repeat_orbit", "overlap"),
                    ("omit_lift", "lifts"), ("bad_flow", "conservation"),
                    ("bad_translation", "translation"), ("bad_coloring", "color"),
                    ("bad_clique", "clique"), ("bad_graph", "graph")]
        for damage, reason in controls:
            with self.subTest(damage=damage):
                data = deepcopy(self.data)
                if damage == "omit_orbit":
                    data["records"].pop()
                elif damage == "repeat_orbit":
                    data["records"].append(deepcopy(data["records"][0]))
                elif damage == "omit_lift":
                    next(r for r in data["records"] if len(r["lifts"]) > 1)["lifts"].pop()
                elif damage == "bad_flow":
                    data["records"][0]["flow"][0] ^= 4
                elif damage == "bad_translation":
                    data["records"][0]["lifts"][0]["translations"][1] ^= 1
                elif damage == "bad_coloring":
                    lift = data["records"][0]["lifts"][0]
                    a, b = lift["pairs"][0]
                    lift["coloring"][str(a)] = lift["coloring"][str(b)]
                elif damage == "bad_clique":
                    data["records"][0]["lifts"][0]["clique"][0] = 8
                elif damage == "bad_graph":
                    data["graph"]["edges"][0] = [0, 2]
                with self.assertRaisesRegex(ValueError, reason):
                    verify_certificate(self.graph, data)

    def test_cli_success_and_failure_with_optimized_python(self):
        root = Path(__file__).resolve().parents[2]
        with TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            data = deepcopy(self.data)
            data["records"].pop()
            path.write_text(json.dumps(data))
            for optimized in (False, True):
                with self.subTest(optimized=optimized):
                    command = [sys.executable] + (["-O"] if optimized else [])
                    command += ["-m", "experiments.cdc.all_flows"]
                    good = subprocess.run(command, cwd=root, capture_output=True, text=True)
                    self.assertEqual(good.returncode, 0, good.stderr)
                    self.assertEqual(json.loads(good.stdout)["status"], "verified")
                    bad = subprocess.run(command + ["--certificate", str(path)], cwd=root,
                                         capture_output=True, text=True)
                    self.assertEqual(bad.returncode, 1)
                    self.assertIn("coverage", json.loads(bad.stdout)["reason"])


if __name__ == "__main__":
    unittest.main()
