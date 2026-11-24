from excel_reader import read_transactions, clean_transactions
from level_filtering import run_level_filtering


def compute_initial_l1(transactions, min_support):
    total_transactions = len(transactions)
    if total_transactions == 0:
        return {}

    item_counts = {}
    for transaction in transactions:
        for item in transaction:
            key = (item,)
            if key in item_counts:
                item_counts[key] += 1
            else:
                item_counts[key] = 1

    l1 = {}
    for key, count in item_counts.items():
        support = count / total_transactions
        if support >= min_support:
            l1[key] = round(support, 4)

    return l1


def placeholder_generate_candidates(prev_itemsets, level_k):
    return []


def main():
    min_support = 0.2
    df = read_transactions("Horizontal_Format.xlsx")
    transactions = clean_transactions(df)

    initial_l1 = compute_initial_l1(transactions, min_support)
    levels = run_level_filtering(
        transactions=transactions,
        initial_L1=initial_l1,
        generate_candidates_fn=placeholder_generate_candidates,
        min_support=min_support,
    )

    for level, itemsets in levels.items():
        print(f"L{level}: {itemsets}")


if __name__ == "__main__":
    main()









# from excel_reader import read_transactions, clean_transactions
# def main():
#     df = read_transactions("Horizontal_Format.xlsx")

#     transactions = clean_transactions(df)
#     print(transactions)
# if __name__ == "__main__":
#     main()







