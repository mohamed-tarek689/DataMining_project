from excel_reader import read_transactions, clean_transactions
from apriori import compute_initial_l1, run_level_filtering
from candidates import generate_candidates
from association_rules import generate_association_rules, get_strong_association_rules
from visualization import plot_frequent_itemsets_support
from experiments import run_threshold_experiments
from visualization import plot_threshold_experiments

def main():
    min_support = 0.3
    min_confidence = 0.75

    df = read_transactions("Lecture_Example.xlsx")
    #df = read_transactions("Horizontal_Format.xlsx")
    transactions = clean_transactions(df)

    initial_l1 = compute_initial_l1(transactions, min_support)
    levels = run_level_filtering(
        transactions=transactions,
        initial_L1=initial_l1,
        generate_candidates_fn=generate_candidates,
        min_support=min_support,
    )

    for level, itemsets in levels.items():
        print(f"L{level}: {itemsets}")

    rules = generate_association_rules(levels)
    strong_rules = get_strong_association_rules(
        transactions,
        rules,
        min_support,
        min_confidence
    )

    print("\nAssociation Rules:")
    for antecedent, consequent in rules:
        print(f"{antecedent} -> {consequent}")

    print("\nStrong Association Rules:")
    for rule in strong_rules:
        print(f"{rule['antecedent']} -> {rule['consequent']}")
        print(f"Support: {rule['support']:.2%}")
        print(f"Confidence: {rule['confidence']:.2%}")
        print(f"Lift: {rule['lift']:.4f}")
        print(f"Correlation: {rule['correlation']}")

    print("Total Association Rules:", len(rules))
    print("Total Strong Rules:", len(strong_rules))

    if any(levels.values()):
        plot_frequent_itemsets_support(levels)
    else:
        print("No frequent itemsets to visualize")

    results = run_threshold_experiments(
        transactions,
        support_thresholds=[0.2, 0.3, 0.4, 0.6],
        confidence_thresholds=[0.5, 0.75, 0.8, 0.9],
        fixed_confidence=min_confidence,
        fixed_support=min_support
    )

    print("\nSupport Experiments:")
    for row in results["support_results"]:
        print(row)

    print("\nConfidence Experiments:")
    for row in results["confidence_results"]:
        print(row)

    plot_threshold_experiments(
        results["support_results"],
        results["confidence_results"]
    )

if __name__ == "__main__":
    main()