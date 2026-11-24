import unittest

from apriori import contains_all_items, filter_candidates_by_support


class TestSupport(unittest.TestCase):
    def setUp(self):
        self.transactions = [
            ["A", "B"],
            ["A", "B", "C"],
            ["A", "C"],
            ["B"],
        ]

    def test_contains_all_items(self):
        self.assertTrue(contains_all_items(("B", "A"), ["A", "B", "C"]))

    def test_missing_item(self):
        self.assertFalse(contains_all_items(("A", "C"), ["A", "B"]))

    def test_support_filtering(self):
        candidates = [("A", "B"), ("A", "C"), ("B", "C")]
        result = filter_candidates_by_support(self.transactions, candidates, 0.5)
        self.assertEqual(result, {("A", "B"): 0.5, ("A", "C"): 0.5})

    def test_support_above_threshold(self):
        result = filter_candidates_by_support(self.transactions, [("A",)], 0.5)
        self.assertEqual(result, {("A",): 0.75})

    def test_duplicate_items_in_transaction(self):
        transactions = [["A", "A", "B"], ["B"]]
        result = filter_candidates_by_support(transactions, [("A", "B")], 0.5)
        self.assertEqual(result, {("A", "B"): 0.5})

    def test_candidate_order_and_duplicates(self):
        candidates = [("B", "A"), ("A", "B")]
        result = filter_candidates_by_support(self.transactions, candidates, 0.5)
        self.assertEqual(result, {("A", "B"): 0.5})

    def test_support_precision(self):
        transactions = [["A", "B"], ["A"], ["B"]]
        result = filter_candidates_by_support(transactions, [("A", "B")], 0.3)
        self.assertAlmostEqual(result[("A", "B")], 1 / 3, places=12)

    def test_empty_transactions(self):
        self.assertEqual(filter_candidates_by_support([], [("A",)], 0.5), {})

    def test_empty_candidates(self):
        self.assertEqual(filter_candidates_by_support(self.transactions, [], 0.5), {})

    def test_no_frequent_candidates(self):
        self.assertEqual(
            filter_candidates_by_support(self.transactions, [("B", "C")], 0.5), {}
        )

    def test_invalid_min_support(self):
        for value in (-0.1, 0, 1.1):
            with self.subTest(min_support=value):
                with self.assertRaises(ValueError):
                    filter_candidates_by_support(self.transactions, [("A",)], value)


if __name__ == "__main__":
    unittest.main()
