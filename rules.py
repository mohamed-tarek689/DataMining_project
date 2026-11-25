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
    support = 0
    if get_total_transactions(transactions) != 0:
        support = get_frequency(transactions, candidate) / get_total_transactions(transactions)

    return support



def get_confidence(transactions, antecedent, consequent):
    confidence = 0
    union = set(antecedent) | set(consequent)
    antecedent_support = get_support(transactions, antecedent)
    if antecedent_support != 0:
        confidence = get_support(transactions, union) / antecedent_support

    return confidence


def get_lift(transactions, antecedent, consequent):
    lift = 0
    intersection = set(antecedent) & set(consequent)
    consequent_support = get_support(transactions, consequent)
    if consequent_support != 0:
        lift = get_confidence(transactions, antecedent, consequent) / consequent_support

    return lift


def determine_correlation(transactions, antecedent, consequent):
    if get_lift(transactions, antecedent, consequent) == 1:
        return "independant"
    elif get_lift(transactions, antecedent, consequent) > 1:
        return "positive correlation"
    else:
        return "negative correlation"

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
