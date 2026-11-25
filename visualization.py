import matplotlib.pyplot as plt


def _flatten_levels(levels):
    labels = []
    supports = []
    for level in sorted(levels):
        for itemset, support in sorted(levels[level].items()):
            labels.append(f"L{level}: {', '.join(itemset)}")
            supports.append(support)
    return labels, supports


def plot_frequent_itemsets_support(levels, save_path=None, show=True):
    labels, supports = _flatten_levels(levels)
    if not labels:
        raise ValueError("There are no frequent itemsets to visualize")

    width = max(8, len(labels) * 0.65)
    fig, ax = plt.subplots(figsize=(width, 5))
    positions = range(len(labels))
    ax.bar(positions, supports)
    ax.set_xticks(list(positions))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Support")
    ax.set_xlabel("Frequent itemsets")
    ax.set_title("Support of Frequent Itemsets")
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    if show:
        plt.show()
    return fig, ax


def plot_threshold_experiments(
    support_results,
    confidence_results,
    save_path=None,
    show=True,
):

    if not support_results and not confidence_results:
        raise ValueError("No threshold experiment results were provided")

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))

    if support_results:
        x = [row["min_support"] for row in support_results]
        y = [row["strong_rules_count"] for row in support_results]
        axes[0].plot(x, y, marker="o")
        axes[0].set_xlabel("Minimum support")
        axes[0].set_ylabel("Number of strong rules")
        axes[0].set_title("Effect of Minimum Support")
        axes[0].grid(True, linestyle="--", alpha=0.35)
    else:
        axes[0].set_visible(False)

    if confidence_results:
        x = [row["min_confidence"] for row in confidence_results]
        y = [row["strong_rules_count"] for row in confidence_results]
        axes[1].plot(x, y, marker="o")
        axes[1].set_xlabel("Minimum confidence")
        axes[1].set_ylabel("Number of strong rules")
        axes[1].set_title("Effect of Minimum Confidence")
        axes[1].grid(True, linestyle="--", alpha=0.35)
    else:
        axes[1].set_visible(False)

    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    if show:
        plt.show()
    return fig, axes
