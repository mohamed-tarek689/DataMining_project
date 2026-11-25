import unittest
from copy import deepcopy

from experiments import run_threshold_experiments


class TestThresholdExperiments(unittest.TestCase):
    def setUp(self):
        # A=3/4, B=2/4, C=1/4, AB=2/4.
        # A -> B: confidence 2/3; B -> A: confidence 1.
        self.transactions = [["A", "B"], ["A", "B"], ["A"], ["C"]]

    def counts(self, rows):
        return [
            (row["frequent_itemsets_count"],
             row["association_rules_count"],
             row["strong_rules_count"])
            for row in rows
        ]

    def test_vary_support(self):
        results = run_threshold_experiments(
            self.transactions, [0.25, 0.5, 0.75, 1.0], [],
            fixed_confidence=0.75
        )
        rows = results["support_results"]
        self.assertEqual([r["min_support"] for r in rows], [0.25, 0.5, 0.75, 1.0])
        self.assertEqual([r["fixed_confidence"] for r in rows], [0.75] * 4)
        self.assertEqual(self.counts(rows), [(4, 2, 1), (3, 2, 1), (1, 0, 0), (0, 0, 0)])
        self.assertEqual(results["confidence_results"], [])

    def test_vary_confidence(self):
        results = run_threshold_experiments(
            self.transactions, [], [0, 0.5, 0.75, 1.0], fixed_support=0.5
        )
        rows = results["confidence_results"]
        self.assertEqual([r["min_confidence"] for r in rows], [0, 0.5, 0.75, 1.0])
        self.assertEqual([r["fixed_support"] for r in rows], [0.5] * 4)
        self.assertEqual(self.counts(rows), [(3, 2, 2), (3, 2, 2), (3, 2, 1), (3, 2, 1)])
        self.assertEqual(results["support_results"], [])

    def test_exact_thresholds(self):
        results = run_threshold_experiments(
            self.transactions, [0.5], [2 / 3, 0.67],
            fixed_support=0.5, fixed_confidence=2 / 3
        )
        self.assertEqual(self.counts(results["support_results"]), [(3, 2, 2)])
        self.assertEqual(self.counts(results["confidence_results"]), [(3, 2, 2), (3, 2, 1)])

    def test_empty_transactions(self):
        results = run_threshold_experiments([], [0.3], [0.75])
        self.assertEqual(self.counts(results["support_results"]), [(0, 0, 0)])
        self.assertEqual(self.counts(results["confidence_results"]), [(0, 0, 0)])

    def test_empty_threshold_lists(self):
        results = run_threshold_experiments(self.transactions, [], [])
        self.assertEqual(results, {"support_results": [], "confidence_results": []})

    def test_invalid_support_thresholds(self):
        for value in (-0.1, 0, 1.1):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    run_threshold_experiments(self.transactions, [value], [0.75])

    def test_invalid_confidence_thresholds(self):
        for value in (-0.1, 1.1):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    run_threshold_experiments(self.transactions, [0.3], [value])

    def test_invalid_fixed_support(self):
        for value in (-0.1, 0, 1.1):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    run_threshold_experiments(
                        self.transactions, [0.3], [0.75], fixed_support=value
                    )

    def test_invalid_fixed_confidence(self):
        for value in (-0.1, 1.1):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    run_threshold_experiments(
                        self.transactions, [0.3], [0.75], fixed_confidence=value
                    )

    def test_no_input_modification(self):
        original = deepcopy(self.transactions)
        run_threshold_experiments(self.transactions, [0.3, 0.5], [0.5, 0.75])
        self.assertEqual(self.transactions, original)

    def test_lecture_example(self):
        # Lecture 2 dataset, with repeated transactions preserved.
        transactions = [list(items) for items in (
            "ABCDEF", "ACDE", "CDE", "BF", "ABCD",
            "ABE", "ABC", "ABE", "AC", "ACDE"
        )]
        results = run_threshold_experiments(
            transactions, [0.2, 0.3, 0.4, 0.6], [0.5, 0.75, 0.8, 0.9],
            fixed_support=0.3, fixed_confidence=0.75
        )
        self.assertEqual(self.counts(results["support_results"]), [
            (27, 98, 32), (21, 68, 26), (14, 26, 14), (5, 2, 2)
        ])
        self.assertEqual(self.counts(results["confidence_results"]), [
            (21, 68, 59), (21, 68, 26), (21, 68, 17), (21, 68, 8)
        ])


if __name__ == "__main__":
    unittest.main()
