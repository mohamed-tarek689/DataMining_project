from apriori import compute_initial_l1, run_level_filtering
from candidates import generate_candidates
from association_rules import generate_association_rules, get_strong_association_rules


def run_threshold_experiments(
    transactions,
    support_thresholds,
    confidence_thresholds,
    fixed_confidence=0.5,
    fixed_support=0.2,
):
    if not 0 <= fixed_confidence <= 1:
        raise ValueError("fixed_confidence must be between 0 and 1")
    if not 0 < fixed_support <= 1:
        raise ValueError("fixed_support must be between 0 and 1")

    for threshold in support_thresholds:
        if not 0 < threshold <= 1:
            raise ValueError("Every support threshold must be in (0, 1]")
    for threshold in confidence_thresholds:
        if not 0 <= threshold <= 1:
            raise ValueError("Every confidence threshold must be in [0, 1]")

    support_results = []
    confidence_results = []

    def analyze(min_support, min_confidence):
        l1 = compute_initial_l1(transactions, min_support)
        levels = run_level_filtering(
            transactions, l1, generate_candidates, min_support
        )
        rules = generate_association_rules(levels)
        strong_rules = get_strong_association_rules(
            transactions, rules, min_support, min_confidence
        )
        itemset_count = sum(len(level) for level in levels.values())
        return levels, rules, strong_rules, itemset_count

    for support in support_thresholds:
        levels, rules, strong_rules, itemset_count = analyze(
            support, fixed_confidence
        )
        support_results.append({
            "min_support": support,
            "fixed_confidence": fixed_confidence,
            "frequent_itemsets_count": itemset_count,
            "association_rules_count": len(rules),
            "strong_rules_count": len(strong_rules),
        })

    for confidence in confidence_thresholds:
        levels, rules, strong_rules, itemset_count = analyze(
            fixed_support, confidence
        )
        confidence_results.append({
            "min_confidence": confidence,
            "fixed_support": fixed_support,
            "frequent_itemsets_count": itemset_count,
            "association_rules_count": len(rules),
            "strong_rules_count": len(strong_rules),
        })

    return {
        "support_results": support_results,
        "confidence_results": confidence_results,
    }
