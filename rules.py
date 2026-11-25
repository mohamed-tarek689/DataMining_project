from itertools import combinations

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

def get_frequency(transactions, candidate):
    frequency = 0
    for transaction in transactions:
        if contains_all_items(candidate, transaction):
            frequency += 1
    return frequency


def get_total_transactions(transactions):
    return len(transactions)


def get_support(transactions, candidate):
    total = get_total_transactions(transactions)
    if total == 0:
        return 0
    return get_frequency(transactions, candidate) / total


def get_confidence(transactions, antecedent, consequent):
    union = set(antecedent) | set(consequent)
    antecedent_support = get_support(transactions, antecedent)
    if antecedent_support == 0:
        return 0
    return get_support(transactions, union) / antecedent_support


def get_lift(transactions, antecedent, consequent):
    consequent_support = get_support(transactions, consequent)
    if consequent_support == 0:
        return 0
    return get_confidence(transactions, antecedent, consequent) / consequent_support


def determine_correlation(transactions, antecedent, consequent):
    if get_support(transactions, consequent) == 0:
        return "undefined (consequent never occurs)"
    lift = get_lift(transactions, antecedent, consequent)
    if lift == 1:
        return "independent"
    elif lift > 1:
        return "positive correlation"
    else:
        return "negative correlation"


def subset_frequency_check(candidate, frequent):
    for subset in combinations(candidate, len(candidate) - 1):
        if frozenset(subset) not in frequent:
            return False
    return True


def make_candidates(previous_level, size, frequent):
    candidates = set()
    for itemset1, itemset2 in combinations(previous_level, 2):
        combined = itemset1 | itemset2
        if len(combined) == size and subset_frequency_check(combined, frequent):
            candidates.add(combined)
    return candidates


def find_frequent_itemsets(transactions, min_support):
    frequent = {}
    items = set()
    for transaction in transactions:
        for item in transaction:
            items.add(item)
    level = []
    for item in sorted(items):
        itemset = frozenset([item])
        support = get_support(transactions, itemset)
        if support >= min_support:
            frequent[itemset] = support
            level.append(itemset)
    size = 2
    while level:
        candidates = make_candidates(level, size, frequent)
        level = []
        for candidate in candidates:
            support = get_support(transactions, candidate)
            if support >= min_support:
                frequent[candidate] = support
                level.append(candidate)
        size += 1
    return frequent


def generate_rules(transactions, frequent, min_confidence):
    rules = []
    for itemset, itemset_support in frequent.items():
        if len(itemset) < 2:
            continue
        for size in range(1, len(itemset)):
            for antecedent in combinations(itemset, size):
                antecedent = frozenset(antecedent)
                consequent = itemset - antecedent
                confidence = get_confidence(transactions, antecedent, consequent)
                if confidence >= min_confidence:
                    lift = get_lift(transactions, antecedent, consequent)
                    correlation = determine_correlation(transactions, antecedent, consequent)
                    rules.append((set(antecedent), set(consequent), itemset_support, confidence, lift, correlation))
    return rules
