import unittest

from apriori import compute_initial_l1, run_level_filtering


class TestApriori(unittest.TestCase):
    def setUp(self):
        self.transactions = [
            ["A", "B", "C"],
            ["A", "B", "C"],
            ["A", "D"],
            ["B", "D"],
        ]

    def test_initial_l1(self):
        result = compute_initial_l1(self.transactions, 0.6)
        self.assertEqual(result, {("A",): 0.75, ("B",): 0.75})

    def test_initial_l1_at_threshold(self):
        result = compute_initial_l1(self.transactions, 0.5)
        self.assertEqual(result, {
            ("A",): 0.75, ("B",): 0.75, ("C",): 0.5, ("D",): 0.5
        })

    def test_initial_l1_duplicate_items(self):
        result = compute_initial_l1([["A", "A"], ["B"]], 0.5)
        self.assertEqual(result, {("A",): 0.5, ("B",): 0.5})

    def test_initial_l1_precision(self):
        result = compute_initial_l1([["A"], ["B"], ["B"]], 0.3)
        self.assertAlmostEqual(result[("A",)], 1 / 3, places=12)

    def test_initial_l1_empty_transactions(self):
        self.assertEqual(compute_initial_l1([], 0.5), {})

    def test_initial_l1_no_frequent_items(self):
        self.assertEqual(compute_initial_l1(self.transactions, 1.0), {})

    def test_multiple_levels(self):
        l1 = {("A",): 0.75, ("B",): 0.75, ("C",): 0.5, ("D",): 0.5}
        l2 = {("A", "B"): 0.5, ("A", "C"): 0.5, ("B", "C"): 0.5}
        l3 = {("A", "B", "C"): 0.5}
        calls = []

        # A stub returns known candidates; it does not implement Student 3's logic.
        def dummy_generate_candidates(prev_itemsets, level_k):
            calls.append((level_k, set(prev_itemsets)))
            if level_k == 2:
                return [("A", "B"), ("A", "C"), ("A", "D"),
                        ("B", "C"), ("B", "D"), ("C", "D")]
            if level_k == 3:
                return [("A", "B", "C")]
            return []

        result = run_level_filtering(self.transactions, l1, dummy_generate_candidates, 0.5)
        self.assertEqual(result, {1: l1, 2: l2, 3: l3})
        self.assertEqual(calls, [(2, set(l1)), (3, set(l2)), (4, set(l3))])

    def test_stop_when_l1_empty(self):
        def dummy_generate_candidates(prev_itemsets, level_k):
            self.fail("Candidate generation must not run when L1 is empty")

        result = run_level_filtering(self.transactions, {}, dummy_generate_candidates, 0.5)
        self.assertEqual(result, {1: {}})

    def test_stop_when_no_candidates(self):
        l1 = {("A",): 1.0}
        result = run_level_filtering([["A"]], l1, lambda prev, k: [], 1.0)
        self.assertEqual(result, {1: l1})

    def test_stop_when_no_frequent_candidates(self):
        transactions = [["A"], ["B"]]
        l1 = {("A",): 0.5, ("B",): 0.5}
        calls = []

        def dummy_generate_candidates(prev_itemsets, level_k):
            calls.append(level_k)
            return [("A", "B")]

        result = run_level_filtering(transactions, l1, dummy_generate_candidates, 0.5)
        self.assertEqual(result, {1: l1})
        self.assertEqual(calls, [2])

    def test_initial_l1_invalid_min_support(self):
        for value in (-0.1, 0, 1.1):
            with self.subTest(min_support=value):
                with self.assertRaises(ValueError):
                    compute_initial_l1(self.transactions, value)

    def test_level_filtering_invalid_min_support(self):
        for value in (-0.1, 0, 1.1):
            with self.subTest(min_support=value):
                with self.assertRaises(ValueError):
                    run_level_filtering([], {}, lambda prev, k: [], value)


if __name__ == "__main__":
    unittest.main()
