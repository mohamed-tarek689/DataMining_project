
def join_itemsets(prev_itemsets, level_k):
    prev_itemsets = sorted(set(prev_itemsets))
    candidates = []

    for i in range(len(prev_itemsets)):
        for j in range(i + 1, len(prev_itemsets)):

            first = prev_itemsets[i]
            second = prev_itemsets[j]

            if first[:-1] == second[:-1]:
                candidate = first + second[-1:]
                candidates.append(candidate)

    return candidates


def prune_candidates(candidates, prev_itemsets, level_k):
    prev_set = set(prev_itemsets)
    pruned_candidates = []

    for candidate in candidates:
        is_valid = True

        for i in range(level_k):
            subset = candidate[:i] + candidate[i + 1:]

            if subset not in prev_set:
                is_valid = False
                break

        if is_valid:
            pruned_candidates.append(candidate)

    return pruned_candidates


def generate_candidates(prev_itemsets, level_k):

    if len(prev_itemsets) < 2:
        return []

    candidates = join_itemsets(prev_itemsets, level_k)

    if level_k == 2:
        return candidates

    return prune_candidates(candidates, prev_itemsets, level_k)