import unittest

from candidates import join_itemsets, prune_candidates, generate_candidates


class TestCandidateGeneration(unittest.TestCase):

    # Joining tests
    def test_join_l1_to_c2(self):
        prev = [("A",), ("B",), ("C",)]
        expected = [("A", "B"), ("A", "C"), ("B", "C")]
        self.assertEqual(join_itemsets(prev, 2), expected)

    def test_join_l2_to_c3(self):
        prev = [("A", "B"), ("A", "C"), ("A", "D"), ("B", "C")]
        expected = [("A", "B", "C"), ("A", "B", "D"), ("A", "C", "D")]
        self.assertEqual(join_itemsets(prev, 3), expected)

    def test_join_l3_to_c4(self):
        prev = [("A", "B", "C"), ("A", "B", "D")]
        self.assertEqual(join_itemsets(prev, 4), [("A", "B", "C", "D")])

    def test_different_prefixes(self):
        prev = [("A", "B"), ("B", "C")]
        self.assertEqual(join_itemsets(prev, 3), [])

    def test_duplicate_prevention(self):
        prev = [("A",), ("A",), ("B",), ("B",)]
        self.assertEqual(join_itemsets(prev, 2), [("A", "B")])

    def test_lexicographic_order(self):
        prev = [("C",), ("A",), ("B",)]
        expected = [("A", "B"), ("A", "C"), ("B", "C")]
        self.assertEqual(join_itemsets(prev, 2), expected)

    # Candidate pruning tests
    def test_keep_valid_candidate(self):
        prev = [("A", "B"), ("A", "C"), ("B", "C")]
        candidates = [("A", "B", "C")]
        self.assertEqual(prune_candidates(candidates, prev, 3), candidates)

    def test_prune_missing_subset(self):
        prev = [("A", "B"), ("A", "C")]
        candidates = [("A", "B", "C")]
        self.assertEqual(prune_candidates(candidates, prev, 3), [])

    def test_prune_multiple_missing_subsets(self):
        prev = [("A", "B", "C"), ("A", "B", "D")]
        candidates = [("A", "B", "C", "D")]
        self.assertEqual(prune_candidates(candidates, prev, 4), [])

    def test_prune_mixed_candidates(self):
        prev = [("A", "B"), ("A", "C"), ("A", "D"), ("B", "C")]
        candidates = [("A", "B", "D"), ("A", "B", "C"), ("A", "C", "D")]
        self.assertEqual(prune_candidates(candidates, prev, 3), [("A", "B", "C")])

    # Main candidate generation tests
    def test_generate_c2(self):
        prev = [("B",), ("A",), ("C",), ("A",)]
        expected = [("A", "B"), ("A", "C"), ("B", "C")]
        self.assertEqual(generate_candidates(prev, 2), expected)

    def test_generate_c3(self):
        prev = [("B", "C"), ("A", "D"), ("A", "B"), ("A", "C")]
        self.assertEqual(generate_candidates(prev, 3), [("A", "B", "C")])

    def test_generate_c4(self):
        prev = [("A", "B", "C"), ("A", "B", "D"),
                ("A", "C", "D"), ("B", "C", "D")]
        self.assertEqual(generate_candidates(prev, 4), [("A", "B", "C", "D")])

    def test_empty_input(self):
        self.assertEqual(generate_candidates([], 2), [])

    def test_single_itemset(self):
        self.assertEqual(generate_candidates([("A", "B", "C")], 4), [])

    def test_no_input_modification(self):
        prev = [("B", "C"), ("A", "B"), ("A", "C")]
        original = prev.copy()
        generate_candidates(prev, 3)
        self.assertEqual(prev, original)

    def test_lecture_example(self):
        # Lecture 2, slides 32-34: BD is not frequent.
        prev = [("A", "B"), ("A", "C"), ("A", "D"), ("A", "E"),
                ("B", "C"), ("B", "E"), ("C", "D"), ("C", "E"), ("D", "E")]
        expected = [("A", "B", "C"), ("A", "B", "E"), ("A", "C", "D"),
                    ("A", "C", "E"), ("A", "D", "E"), ("B", "C", "E"),
                    ("C", "D", "E")]
        self.assertEqual(generate_candidates(prev, 3), expected)


if __name__ == "__main__":
    unittest.main()
