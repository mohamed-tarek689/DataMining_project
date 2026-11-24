
def validate_min_support(min_support):
    if not (0 < min_support <= 1):
        raise ValueError("Minimum support must be between 0 and 1")

def compute_initial_l1(transactions, min_support):
    validate_min_support(min_support)

    total_transactions = len(transactions)
    if total_transactions == 0:
        return {}

    item_counts = {}
    for transaction in transactions:
        for item in set(transaction):
            key = (item,)
            if key in item_counts:
                item_counts[key] += 1
            else:
                item_counts[key] = 1

    l1 = {}
    for key, count in item_counts.items():
        support = count / total_transactions
        if support >= min_support:
            l1[key] = support

    return l1

def contains_all_items(candidate, transaction):
    for item in candidate:
        found = False
        for t_item in transaction:
            if item == t_item:
                found = True
                break
        if not found:
            return False
    return True


def filter_candidates_by_support(transactions, candidates, min_support):
    validate_min_support(min_support)

    frequent_itemsets = {}
    total_transactions = len(transactions)

    if total_transactions == 0:
        return frequent_itemsets

    for candidate in candidates:
        match_count = 0
        for transaction in transactions:
            if contains_all_items(candidate, transaction):
                match_count += 1

        support = match_count / total_transactions
        if support >= min_support:
            frequent_itemsets[tuple(sorted(candidate))] = support

    return frequent_itemsets


def run_level_filtering(transactions, initial_L1, generate_candidates_fn, min_support):
    validate_min_support(min_support)

    levels = {1: initial_L1}
    current_L = initial_L1
    k = 2

    while len(current_L) > 0:
        current_itemsets = []
        for itemset in current_L:
            current_itemsets.append(itemset)

        next_candidates = generate_candidates_fn(current_itemsets, k)

        if len(next_candidates) == 0:
            break

        next_L = filter_candidates_by_support(transactions, next_candidates, min_support)

        if len(next_L) == 0:
            break

        levels[k] = next_L
        current_L = next_L
        k += 1

    return levels
