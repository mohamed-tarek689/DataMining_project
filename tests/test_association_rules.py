import unittest

from association_rules import (
    get_frequency,
    get_total_transactions,
    get_support,
    get_confidence,
    get_lift,
    determine_correlation,
    generate_association_rules,
    get_strong_association_rules,
)


class TestAssociationRules(unittest.TestCase):
    def setUp(self):
        self.transactions = [
            ["A", "B", "C"],
            ["A", "B"],
            ["A", "C"],
            ["B"]
        ]
        # A=3, B=3, C=2, AB=2, AC=2, BC=1, ABC=1

    def test_frequency_single_item(self):
        self.assertEqual(get_frequency(self.transactions, ("A",)), 3)

    def test_frequency_multiple_items(self):
        self.assertEqual(get_frequency(self.transactions, ("A", "B")), 2)
        self.assertEqual(get_frequency(self.transactions, ("A", "B", "C")), 1)

    def test_frequency_missing_item(self):
        self.assertEqual(get_frequency(self.transactions, ("Z",)), 0)

    def test_frequency_duplicate_items_in_transaction(self):
        transactions = [["A", "A", "B"], ["B"]]
        self.assertEqual(get_frequency(transactions, ("A",)), 1)

    def test_frequency_empty_transactions(self):
        self.assertEqual(get_frequency([], ("A",)), 0)

    def test_total_transactions(self):
        self.assertEqual(get_total_transactions(self.transactions), 4)
        self.assertEqual(get_total_transactions([]), 0)

    def test_support(self):
        self.assertAlmostEqual(get_support(self.transactions, ("A",)), 0.75)
        self.assertAlmostEqual(get_support(self.transactions, ("A", "B")), 0.5)

    def test_support_missing_item(self):
        self.assertEqual(get_support(self.transactions, ("Z",)), 0)

    def test_support_empty_transactions(self):
        self.assertEqual(get_support([], ("A",)), 0)

    def test_confidence(self):
        self.assertAlmostEqual(
            get_confidence(self.transactions, ("A",), ("B",)), 2 / 3
        )

    def test_confidence_rule_direction(self):
        self.assertAlmostEqual(
            get_confidence(self.transactions, ("A",), ("C",)), 2 / 3
        )
        self.assertEqual(
            get_confidence(self.transactions, ("C",), ("A",)), 1.0
        )

    def test_confidence_multiple_items(self):
        self.assertAlmostEqual(
            get_confidence(self.transactions, ("A", "B"), ("C",)), 0.5
        )

    def test_confidence_missing_antecedent(self):
        self.assertEqual(get_confidence(self.transactions, ("Z",), ("A",)), 0)

    def test_confidence_missing_consequent(self):
        self.assertEqual(get_confidence(self.transactions, ("A",), ("Z",)), 0)

    def test_confidence_empty_transactions(self):
        self.assertEqual(get_confidence([], ("A",), ("B",)), 0)

    def test_confidence_floating_point_boundary(self):
        # A appears 8 times and AB appears 6 times out of 10.
        transactions = [["A", "B"]] * 6 + [["A"]] * 2 + [["C"]] * 2
        # Exact equality is intentional: a threshold of 0.75 must be accepted.
        self.assertEqual(get_confidence(transactions, ("A",), ("B",)), 0.75)

    def test_lift_positive(self):
        self.assertAlmostEqual(get_lift(self.transactions, ("A",), ("C",)), 4 / 3)

    def test_lift_negative(self):
        self.assertAlmostEqual(get_lift(self.transactions, ("B",), ("C",)), 2 / 3)

    def test_lift_independent(self):
        transactions = [["A", "B"], ["A"], ["B"], ["C"]]
        self.assertAlmostEqual(get_lift(transactions, ("A",), ("B",)), 1.0)

    def test_lift_missing_consequent(self):
        self.assertEqual(get_lift(self.transactions, ("A",), ("Z",)), 0)

    def test_lift_empty_transactions(self):
        self.assertEqual(get_lift([], ("A",), ("B",)), 0)

    def test_correlation_positive(self):
        self.assertEqual(
            determine_correlation(self.transactions, ("A",), ("C",)),
            "positive correlation"
        )

    def test_correlation_negative(self):
        self.assertEqual(
            determine_correlation(self.transactions, ("B",), ("C",)),
            "negative correlation"
        )

    def test_correlation_independent(self):
        transactions = [["A", "B"], ["A"], ["B"], ["C"]]
        self.assertEqual(
            determine_correlation(transactions, ("A",), ("B",)), "independent"
        )

    def test_correlation_missing_consequent(self):
        self.assertEqual(
            determine_correlation(self.transactions, ("A",), ("Z",)),
            "undefined (consequent never occurs)"
        )

    def test_generate_empty_levels(self):
        self.assertEqual(generate_association_rules({}), [])
        self.assertEqual(generate_association_rules({1: {}}), [])

    def test_generate_l1_only(self):
        self.assertEqual(generate_association_rules({1: {("A",): 0.75}}), [])

    def test_generate_l2(self):
        levels = {2: {("A", "B"): 0.5}}
        expected = {(("A",), ("B",)), (("B",), ("A",))}
        rules = generate_association_rules(levels)
        self.assertEqual(len(rules), 2)
        self.assertEqual(set(rules), expected)

    def test_generate_l3(self):
        levels = {3: {("A", "B", "C"): 0.25}}
        expected = {
            (("A",), ("B", "C")), (("B",), ("A", "C")),
            (("C",), ("A", "B")), (("A", "B"), ("C",)),
            (("A", "C"), ("B",)), (("B", "C"), ("A",))
        }
        rules = generate_association_rules(levels)
        self.assertEqual(len(rules), 6)
        self.assertEqual(set(rules), expected)

    def test_generate_l4_and_l5(self):
        for itemset, expected_count in [(tuple("ABCD"), 14), (tuple("ABCDE"), 30)]:
            with self.subTest(itemset=itemset):
                rules = generate_association_rules({len(itemset): {itemset: 0.4}})
                self.assertEqual(len(rules), expected_count)
                self.assertEqual(len(set(rules)), expected_count)
                for antecedent, consequent in rules:
                    self.assertIsInstance(antecedent, tuple)
                    self.assertIsInstance(consequent, tuple)
                    self.assertTrue(antecedent)
                    self.assertTrue(consequent)
                    self.assertFalse(set(antecedent) & set(consequent))
                    self.assertEqual(set(antecedent) | set(consequent), set(itemset))

    def test_generate_multiple_levels(self):
        levels = {
            1: {("A",): 0.75, ("B",): 0.75, ("C",): 0.5},
            2: {("A", "B"): 0.5, ("A", "C"): 0.5, ("B", "C"): 0.25},
            3: {("A", "B", "C"): 0.25}
        }
        rules = generate_association_rules(levels)
        self.assertEqual(len(rules), 12)
        self.assertEqual(len(set(rules)), 12)
        self.assertIn((("B",), ("A",)), rules)
        self.assertIn((("A", "C"), ("B",)), rules)

    def test_strong_rules_metrics(self):
        rules = [(("C",), ("A",)), (("A",), ("C",))]
        result = get_strong_association_rules(self.transactions, rules, 0.5, 0.8)
        self.assertEqual(len(result), 1)
        rule = result[0]
        self.assertEqual(rule["antecedent"], ("C",))
        self.assertEqual(rule["consequent"], ("A",))
        self.assertAlmostEqual(rule["support"], 0.5)
        self.assertAlmostEqual(rule["confidence"], 1.0)
        self.assertAlmostEqual(rule["lift"], 4 / 3)
        self.assertEqual(rule["correlation"], "positive correlation")

    def test_strong_rules_support_filter(self):
        rules = [(("C",), ("A",))]
        self.assertEqual(get_strong_association_rules(self.transactions, rules, 0.6, 0.8), [])

    def test_strong_rules_confidence_filter(self):
        rules = [(("A",), ("C",))]
        self.assertEqual(get_strong_association_rules(self.transactions, rules, 0.5, 0.8), [])

    def test_strong_rules_exact_thresholds(self):
        transactions = [["A", "B"]] * 6 + [["A"]] * 2 + [["C"]] * 2
        rules = [(("A",), ("B",))]
        result = get_strong_association_rules(transactions, rules, 0.6, 0.75)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["confidence"], 0.75)

    def test_strong_rules_just_above_threshold(self):
        transactions = [["A", "B"]] * 6 + [["A"]] * 2 + [["C"]] * 2
        rules = [(("A",), ("B",))]
        self.assertEqual(get_strong_association_rules(transactions, rules, 0.6, 0.7501), [])

    def test_strong_rules_empty(self):
        self.assertEqual(get_strong_association_rules(self.transactions, [], 0.3, 0.7), [])
        self.assertEqual(get_strong_association_rules([], [(("A",), ("B",))], 0.3, 0.7), [])


if __name__ == "__main__":
    unittest.main()
