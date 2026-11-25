from excel_reader import read_transactions, clean_transactions
from apriori import compute_initial_l1, run_level_filtering
from candidates import generate_candidates
from association_rules import generate_association_rules, get_strong_association_rules


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

    print("Total Association Rules:", len(rules))
    print("Total Strong Rules:", len(strong_rules))


if __name__ == "__main__":
    main()