import unittest
from pathlib import Path
from apriori import compute_initial_l1, run_level_filtering
from candidates import generate_candidates
from excel_reader import read_transactions, clean_transactions
from association_rules import generate_association_rules, get_strong_association_rules


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


class TestAssociationRulesIntegration(unittest.TestCase):

    def read_dataset(self, filename):
        project_root = Path(__file__).resolve().parent.parent
        return clean_transactions(read_transactions(project_root / filename))

    def run_pipeline(self, transactions, min_support, min_confidence):
        l1 = compute_initial_l1(transactions, min_support)
        levels = run_level_filtering(
            transactions, l1, generate_candidates, min_support
        )
        rules = generate_association_rules(levels)
        strong_rules = get_strong_association_rules(
            transactions, rules, min_support, min_confidence
        )
        return levels, rules, strong_rules

    def check_results(self, levels, rules, strong_rules, counts, all_count, strong_count):
        self.assertEqual({k: len(v) for k, v in levels.items()}, counts)
        self.assertEqual(len(rules), all_count)
        self.assertEqual(len(set(rules)), all_count)
        self.assertEqual(len(strong_rules), strong_count)
        pairs = {(r["antecedent"], r["consequent"]) for r in strong_rules}
        self.assertEqual(len(pairs), strong_count)
        self.assertTrue(pairs.issubset(set(rules)))
        for left, right in rules:
            self.assertTrue(left and right)
            self.assertTrue(set(left).isdisjoint(right))
            union = tuple(sorted(left + right))
            self.assertIn(union, levels[len(union)])

    def test_lecture_example(self):
        transactions = self.read_dataset("Lecture_Example.xlsx")
        self.assertEqual(len(transactions), 10)
        result = self.run_pipeline(transactions, 0.3, 0.7)
        self.check_results(*result, {1: 5, 2: 9, 3: 6, 4: 1}, 68, 27)
        _, rules, strong_rules = result
        by_pair = {(r["antecedent"], r["consequent"]): r for r in strong_rules}
        self.assertIn((("A",), ("B",)), rules)
        self.assertNotIn((("A",), ("B",)), by_pair)
        rule = by_pair[(("B",), ("A",))]
        self.assertAlmostEqual(rule["support"], 5 / 10)
        self.assertAlmostEqual(rule["confidence"], 5 / 6)
        self.assertAlmostEqual(rule["lift"], 25 / 24)
        self.assertEqual(rule["correlation"], "positive correlation")
        rule = by_pair[(("B", "C"), ("A",))]
        self.assertAlmostEqual(rule["support"], 0.3)
        self.assertAlmostEqual(rule["confidence"], 1.0)
        self.assertAlmostEqual(rule["lift"], 1.25)

    def test_lecture_confidence_boundary(self):
        transactions = self.read_dataset("Lecture_Example.xlsx")
        result = self.run_pipeline(transactions, 0.3, 0.75)
        self.check_results(*result, {1: 5, 2: 9, 3: 6, 4: 1}, 68, 26)
        _, _, strong_rules = result
        by_pair = {(r["antecedent"], r["consequent"]): r for r in strong_rules}
        rule = by_pair[(("A",), ("C",))]
        self.assertEqual(rule["confidence"], 0.75)
        self.assertAlmostEqual(rule["support"], 0.6)
        self.assertAlmostEqual(rule["lift"], 0.75 / 0.7)

    def test_section_example_60_80(self):
        transactions = self.read_dataset("Horizontal_Format.xlsx")
        self.assertEqual(len(transactions), 5)
        result = self.run_pipeline(transactions, 0.6, 0.8)
        self.check_results(*result, {1: 5, 2: 5, 3: 1}, 16, 9)
        _, _, strong_rules = result
        by_pair = {(r["antecedent"], r["consequent"]): r for r in strong_rules}
        rule = by_pair[(("M",), ("K",))]
        self.assertAlmostEqual(rule["support"], 0.6)
        self.assertAlmostEqual(rule["confidence"], 1.0)
        self.assertAlmostEqual(rule["lift"], 1.0)
        self.assertEqual(rule["correlation"], "independent")
        self.assertNotIn((("K",), ("M",)), by_pair)

    def test_horizontal_example_30_70(self):
        transactions = self.read_dataset("Horizontal_Format.xlsx")
        result = self.run_pipeline(transactions, 0.3, 0.7)
        self.check_results(*result, {1: 7, 2: 14, 3: 12, 4: 5, 5: 1}, 200, 104)
        _, rules, _ = result
        self.assertIn((("E", "K", "N", "O"), ("Y",)), rules)

    def test_no_frequent_pairs(self):
        result = self.run_pipeline([["A"], ["B"]], 0.5, 0.7)
        self.check_results(*result, {1: 2}, 0, 0)

    def test_no_strong_rules(self):
        transactions = [["A", "B"], ["A"], ["B"], ["C"]]
        result = self.run_pipeline(transactions, 0.25, 0.75)
        self.check_results(*result, {1: 3, 2: 1}, 2, 0)

    def test_negative_correlation(self):
        transactions = [["A", "B"], ["A"], ["B"], ["A", "C"]]
        _, _, strong_rules = self.run_pipeline(transactions, 0.25, 0.5)
        by_pair = {(r["antecedent"], r["consequent"]): r for r in strong_rules}
        rule = by_pair[(("B",), ("A",))]
        self.assertAlmostEqual(rule["support"], 0.25)
        self.assertAlmostEqual(rule["confidence"], 0.5)
        self.assertAlmostEqual(rule["lift"], 2 / 3)
        self.assertEqual(rule["correlation"], "negative correlation")


if __name__ == "__main__":
    unittest.main()
