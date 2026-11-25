from itertools import combinations
from apriori import contains_all_items


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
    antecedent_frequency = get_frequency(transactions, antecedent)
    if antecedent_frequency == 0:
        return 0
    return get_frequency(transactions, union) / antecedent_frequency


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


def generate_association_rules(levels):
    rules = []

    for level, itemsets in levels.items():
        if level < 2:
            continue

        for itemset in itemsets:
            for size in range(1, len(itemset)):
                for antecedent in combinations(itemset, size):
                    consequent = tuple(
                        item for item in itemset
                        if item not in antecedent
                    )
                    rules.append((antecedent, consequent))

    return rules


def get_strong_association_rules(transactions, rules, min_support, min_confidence):
    strong_rules = []
    for antecedent, consequent in rules:
        support = get_support(transactions, set(antecedent) | set(consequent))
        confidence = get_confidence(transactions, antecedent, consequent)
        lift = get_lift(transactions, antecedent, consequent)

        if support >= min_support and confidence >= min_confidence:
            strong_rules.append({
                "antecedent": antecedent,
                "consequent": consequent,
                "support": support,
                "confidence": confidence,
                "lift": lift,
                "correlation": determine_correlation(transactions, antecedent, consequent)
            })

    return strong_rules
