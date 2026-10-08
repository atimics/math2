"""Independent checker regressions. Run: python -m unittest discover -s experiments/cdc."""

import copy
import json
import unittest
from pathlib import Path

try:
    from .verify import verify_cover, verify_palette_clique
except ImportError:
    from verify import verify_cover, verify_palette_clique


def k4_cover():
    graph = {"vertex_count": 4, "edges": [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]}
    # Three four-cycles, each complementary to one perfect matching.
    witness = {**copy.deepcopy(graph), "labels": 3,
               "pairs": [[1, 2], [0, 2], [0, 1], [0, 1], [0, 2], [1, 2]]}
    return graph, witness


class CheckerTests(unittest.TestCase):
    def test_checked_artifacts_without_solver(self):
        artifact = Path(__file__).with_name("results.json")
        with artifact.open(encoding="utf-8") as stream:
            results = json.load(stream)
        self.assertEqual(results["schema_version"], 1)
        self.assertTrue(results["records"])
        checked = 0
        for record in results["records"]:
            graph = record["graph"]
            outputs = [record["construction"], record.get("compression_to_five", {})]
            outputs.extend(record.get("unrestricted", {}).values())
            for output in outputs:
                witness = output.get("witness")
                if witness is not None:
                    with self.subTest(graph=graph["name"], labels=witness["labels"]):
                        summary = verify_cover(graph, witness)
                        self.assertEqual(summary, output["verification"])
                        checked += 1
            certificate = record.get("compression_to_five", {}).get("metadata", {}).get("clique_certificate")
            if certificate is not None:
                replayed = verify_palette_clique(
                    record["construction"]["witness"],
                    certificate["clique_labels"], certificate["target_labels"])
                self.assertEqual(replayed, certificate)
        self.assertGreater(checked, 0)

    def test_hand_valid_k4(self):
        graph, witness = k4_cover()
        summary = verify_cover(graph, witness)
        self.assertEqual(summary["edges"], 6)
        self.assertEqual(summary["used_labels"], 3)
        self.assertEqual(summary["label_edge_counts"], {"0": 4, "1": 4, "2": 4})

    def test_edge_order_and_orientation(self):
        graph, witness = k4_cover()
        witness["edges"] = [edge[::-1] for edge in reversed(witness["edges"])]
        witness["pairs"].reverse()
        verify_cover(graph, witness)

    def test_empty_labels_allowed(self):
        graph, witness = k4_cover()
        witness["labels"] = 8
        self.assertEqual(verify_cover(graph, witness)["used_labels"], 3)

    def test_pair_corruptions(self):
        for pair in ([0], [0, 0], [0, 3], [-1, 1], [True, 2], [0.0, 2], "12", None):
            with self.subTest(pair=pair):
                graph, witness = k4_cover()
                witness["pairs"][0] = pair
                with self.assertRaises(ValueError):
                    verify_cover(graph, witness)

    def test_odd_degrees(self):
        graph, witness = k4_cover()
        witness["pairs"][0] = [0, 2]
        with self.assertRaisesRegex(ValueError, "odd degree"):
            verify_cover(graph, witness)

    def test_missing_or_extra_pair(self):
        for pairs in ([], [[0, 1]] * 7, None):
            graph, witness = k4_cover()
            witness["pairs"] = pairs
            with self.assertRaises(ValueError):
                verify_cover(graph, witness)

    def test_integer_fields_reject_bool_and_float(self):
        for field, values in (("vertex_count", (True, 4.0, 0)), ("labels", (True, 3.0, 1))):
            for value in values:
                with self.subTest(field=field, value=value):
                    graph, witness = k4_cover()
                    witness[field] = value
                    with self.assertRaises(ValueError):
                        verify_cover(graph, witness)

    def test_bad_graph_edges(self):
        for edge in ([0, 0], [0, 4], [True, 1], [0.0, 1], [0], None, [2, 0]):
            with self.subTest(edge=edge):
                graph, witness = k4_cover()
                graph["edges"][0] = edge
                with self.assertRaises(ValueError):
                    verify_cover(graph, witness)

    def test_witness_graph_must_match(self):
        graph, witness = k4_cover()
        witness["vertex_count"] = 6
        witness["edges"] = [[0, 1], [1, 2], [2, 0], [3, 4], [4, 5], [5, 3], [0, 3], [1, 4], [2, 5]]
        witness["pairs"] = [[0, 1]] * 9
        with self.assertRaisesRegex(ValueError, "does not match"):
            verify_cover(graph, witness)

    def test_disconnected_cubic_graph(self):
        graph, witness = k4_cover()
        graph["vertex_count"] = 8
        graph["edges"] += [[u + 4, v + 4] for u, v in graph["edges"][:]]
        with self.assertRaisesRegex(ValueError, "connected"):
            verify_cover(graph, witness)

    def test_cubic_graph_with_bridge(self):
        # Two K4s with one edge subdivided, joined at the subdivision vertices.
        graph = {"vertex_count": 10, "edges": [[0, 4], [4, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3],
                 [5, 9], [9, 6], [5, 7], [5, 8], [6, 7], [6, 8], [7, 8], [4, 9]]}
        _, witness = k4_cover()
        with self.assertRaisesRegex(ValueError, "bridge"):
            verify_cover(graph, witness)


class ExperimentIntegrationTests(unittest.TestCase):
    def test_petersen_palette_clique_obstruction(self):
        from experiments.cdc.construction import affine_witness
        from experiments.cdc.graphs import fixtures
        graph = next(g for g in fixtures() if g["name"] == "petersen")
        flow = [6, 5, 3, 7, 1, 5, 2, 1, 4, 4, 4, 7, 3, 2, 6]
        witness = affine_witness(graph, flow)
        clique = [1, 2, 3, 5, 6, 7]
        certificate = verify_palette_clique(witness, clique, 5)
        self.assertEqual(certificate["checked_pairs"], 15)
        self.assertFalse(certificate["unrestricted_impossibility_claim"])
        for invalid in ([1, 2, 3, 5, 6, 6], [1, 2, 3, 5, 6, 8],
                        [True, 2, 3, 5, 6, 7], [1, 2, 3, 4, 6, 7], clique[:5]):
            with self.subTest(clique=invalid):
                with self.assertRaises(ValueError):
                    verify_palette_clique(witness, invalid, 5)
        for invalid_k in (True, 5.0, 0):
            with self.assertRaises(ValueError):
                verify_palette_clique(witness, clique, invalid_k)

    def test_constructed_fixture_covers(self):
        from experiments.cdc.construction import construct_cover
        from experiments.cdc.graphs import fixtures
        from experiments.cdc.search import compress_cover
        for graph in fixtures():
            with self.subTest(graph=graph["name"]):
                result = construct_cover(graph, node_limit=100_000)
                self.assertEqual(result["status"], "found")
                verify_cover(graph, result["witness"])
                compressed = compress_cover(result["witness"], 5)
                self.assertEqual(compressed["status"], "compressed")
                verify_cover(graph, compressed["witness"])

    def test_construction_limit_is_unknown(self):
        from experiments.cdc.construction import construct_cover
        from experiments.cdc.graphs import fixtures
        result = construct_cover(fixtures()[3], node_limit=1)
        self.assertEqual(result["status"], "limit")
        self.assertNotIn("witness", result)

    def test_petersen_four_vs_five_solver_regression(self):
        try:
            import scipy.optimize  # optional: checker itself remains stdlib-only
        except ImportError:
            self.skipTest("SciPy required for MILP integration")
        from experiments.cdc.graphs import fixtures
        from experiments.cdc.search import solve_cover
        graph = next(g for g in fixtures() if g["name"] == "petersen")
        four = solve_cover(graph, 4, time_limit=30)
        self.assertEqual(four["status"], "infeasible")
        self.assertFalse(four["metadata"]["proof_certified_unsat"])
        self.assertIsNone(four["witness"])
        five = solve_cover(graph, 5, time_limit=30)
        self.assertEqual(five["status"], "found")
        verify_cover(graph, five["witness"])


if __name__ == "__main__":
    unittest.main()
