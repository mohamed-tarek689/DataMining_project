import unittest

from apriori import compute_initial_l1, run_level_filtering
from candidates import generate_candidates


class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.transactions = [
            list("MONKEY"),
            list("DONKEY"),
            list("MAKE"),
            list("MUCKY"),
            list("COOKIE")
        ]

    def test_multiple_levels(self):

        transactions = [
            ["A", "B", "C"],
            ["A", "B", "C"],
            ["A", "D"],
            ["B", "D"]
        ]

        min_support = 0.5

        l1 = compute_initial_l1(transactions, min_support)

        result = run_level_filtering(
            transactions,
            l1,
            generate_candidates,
            min_support
        )

        expected = {
            1: {
                ("A",): 0.75,
                ("B",): 0.75,
                ("C",): 0.5,
                ("D",): 0.5
            },
            2: {
                ("A", "B"): 0.5,
                ("A", "C"): 0.5,
                ("B", "C"): 0.5
            },
            3: {
                ("A", "B", "C"): 0.5
            }
        }

        self.assertEqual(result, expected)

    def test_section_example_60_percent(self):

        min_support = 0.6

        l1 = compute_initial_l1(
            self.transactions, min_support
        )

        result = run_level_filtering(
            self.transactions,
            l1,
            generate_candidates,
            min_support
        )

        expected = {
            1: {
                ("E",): 0.8,
                ("K",): 1.0,
                ("M",): 0.6,
                ("O",): 0.6,
                ("Y",): 0.6
            },
            2: {
                ("E", "K"): 0.8,
                ("E", "O"): 0.6,
                ("K", "M"): 0.6,
                ("K", "O"): 0.6,
                ("K", "Y"): 0.6
            },
            3: {
                ("E", "K", "O"): 0.6
            }
        }

        self.assertEqual(result, expected)

    def test_section_example_20_percent(self):

        min_support = 0.2

        l1 = compute_initial_l1(
            self.transactions, min_support
        )

        result = run_level_filtering(
            self.transactions,
            l1,
            generate_candidates,
            min_support
        )

        expected_counts = {
            1: 11,
            2: 36,
            3: 51,
            4: 36,
            5: 13,
            6: 2
        }

        actual_counts = {}

        for level, itemsets in result.items():
            actual_counts[level] = len(itemsets)

        self.assertEqual(actual_counts, expected_counts)

        self.assertEqual(result[6], {
            ("D", "E", "K", "N", "O", "Y"): 0.2,
            ("E", "K", "M", "N", "O", "Y"): 0.2
        })

    def test_no_frequent_candidates(self):

        transactions = [["A"], ["B"]]
        min_support = 0.5

        l1 = compute_initial_l1(transactions, min_support)

        result = run_level_filtering(
            transactions,
            l1,
            generate_candidates,
            min_support
        )

        self.assertEqual(result, {
            1: {
                ("A",): 0.5,
                ("B",): 0.5
            }
        })


if __name__ == "__main__":
    unittest.main()