from excel_reader import read_transactions, clean_transactions
from apriori import compute_initial_l1, run_level_filtering
from candidates import generate_candidates



def main():
    min_support = 0.6
    df = read_transactions("Horizontal_Format.xlsx")
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


if __name__ == "__main__":
    main()