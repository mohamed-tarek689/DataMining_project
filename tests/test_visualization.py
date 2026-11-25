import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from visualization import (
    plot_frequent_itemsets_support,
    plot_threshold_experiments,
)


class TestVisualization(unittest.TestCase):
    def setUp(self):
        # Deliberately unsorted to test level and itemset ordering.
        self.levels = {
            2: {("A", "B"): 0.5},
            1: {("B",): 0.6, ("A",): 0.8},
        }
        self.support_results = [
            {"min_support": 0.3, "strong_rules_count": 26},
            {"min_support": 0.4, "strong_rules_count": 14},
        ]
        self.confidence_results = [
            {"min_confidence": 0.5, "strong_rules_count": 59},
            {"min_confidence": 0.75, "strong_rules_count": 26},
        ]

    def tearDown(self):
        plt.close("all")

    def test_bar_count(self):
        _, ax = plot_frequent_itemsets_support(self.levels, show=False)
        self.assertEqual(len(ax.patches), 3)

    def test_support_values(self):
        _, ax = plot_frequent_itemsets_support(self.levels, show=False)
        heights = [bar.get_height() for bar in ax.patches]
        for actual, expected in zip(heights, [0.8, 0.6, 0.5]):
            self.assertAlmostEqual(actual, expected)
        self.assertEqual(len(heights), 3)

    def test_itemset_labels(self):
        _, ax = plot_frequent_itemsets_support(self.levels, show=False)
        labels = [label.get_text() for label in ax.get_xticklabels()]
        self.assertEqual(labels, ["L1: A", "L1: B", "L2: A, B"])

    def test_empty_levels(self):
        for levels in ({}, {1: {}}):
            with self.subTest(levels=levels):
                with self.assertRaises(ValueError):
                    plot_frequent_itemsets_support(levels, show=False)

    def test_save_support_chart(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "support.png"
            plot_frequent_itemsets_support(self.levels, save_path=path, show=False)
            self.assertTrue(path.is_file())
            self.assertGreater(path.stat().st_size, 0)

    def test_support_experiment_plot(self):
        _, axes = plot_threshold_experiments(
            self.support_results, self.confidence_results, show=False
        )
        line = axes[0].lines[0]
        self.assertEqual(list(line.get_xdata()), [0.3, 0.4])
        self.assertEqual(list(line.get_ydata()), [26, 14])

    def test_confidence_experiment_plot(self):
        _, axes = plot_threshold_experiments(
            self.support_results, self.confidence_results, show=False
        )
        line = axes[1].lines[0]
        self.assertEqual(list(line.get_xdata()), [0.5, 0.75])
        self.assertEqual(list(line.get_ydata()), [59, 26])

    def test_support_only(self):
        _, axes = plot_threshold_experiments(self.support_results, [], show=False)
        self.assertTrue(axes[0].get_visible())
        self.assertFalse(axes[1].get_visible())

    def test_confidence_only(self):
        _, axes = plot_threshold_experiments([], self.confidence_results, show=False)
        self.assertFalse(axes[0].get_visible())
        self.assertTrue(axes[1].get_visible())

    def test_empty_experiments(self):
        with self.assertRaises(ValueError):
            plot_threshold_experiments([], [], show=False)

    def test_save_experiment_chart(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "experiments.png"
            plot_threshold_experiments(
                self.support_results, self.confidence_results,
                save_path=path, show=False
            )
            self.assertTrue(path.is_file())
            self.assertGreater(path.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
