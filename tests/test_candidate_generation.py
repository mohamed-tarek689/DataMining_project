import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from level_filtering import run_level_filtering


def dummy_generate_candidates(prev_itemsets, level_k):
    if level_k == 2:
        return [
            ("milk", "bread"),
            ("milk", "butter"),
            ("bread", "butter"),
        ]
    return []


def main():
    sample_transactions = [
        ["milk", "bread", "butter"],
        ["bread", "butter"],
        ["milk", "bread"],
        ["milk", "butter"],
    ]
    sample_L1 = {
        ("milk",): 0.75,
        ("bread",): 0.75,
        ("butter",): 0.75,
    }

    result_levels = run_level_filtering(
        transactions=sample_transactions,
        initial_L1=sample_L1,
        generate_candidates_fn=dummy_generate_candidates,
        min_support=0.5,
    )

    for lvl, items in result_levels.items():
        print(f"L{lvl}: {items}")


if __name__ == "__main__":
    main()
