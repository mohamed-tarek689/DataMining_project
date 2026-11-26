# Apriori Algorithm – Data Mining Project

This Python project reads market-basket transactions from Excel and implements Apriori directly. It prints the frequent itemsets at each level, generates association rules, and shows support, confidence, lift, and the dependency indicated by lift for each strong rule.

## Run the project

Open a terminal in the project folder, alongside `main.py` and the two Excel workbooks. Use Python 3 to install the dependencies and start the program.

```bash
python -m pip install -r requirements.txt
python main.py
```

The default input is `Lecture_Example.xlsx`. In `main.py`, `min_support = 0.3` means 30% and `min_confidence = 0.75` means 75%. To run the other example, change the active filename in `read_transactions(...)` to `Horizontal_Format.xlsx` and rerun the same command. Support accepts values in `(0, 1]` and confidence accepts values in `[0, 1]`. An itemset or rule exactly on a threshold qualifies.

The first chart shows one bar per frequent itemset, with support on the vertical axis. With an interactive plotting backend, close the first chart to continue to the experiments. The next figure shows how the strong-rule count changes as each threshold varies.

## Excel input

Use the first worksheet and include a column named `items`. Each row represents one transaction. Put the item names in one cell and separate them with commas.

| items |
| --- |
| A, B, C |
| A, C |
| B |

The reader trims whitespace, converts names to uppercase, skips empty rows, and counts each item once per transaction. Identical baskets on separate rows count as separate transactions. A missing `items` column or a sheet with no valid transactions raises `ValueError`. The reader uses pandas' default handling of missing values. For example, a cell containing only the literal item code `NA` is treated as empty.

## Verify the example results

Both rows use the same thresholds of 30% support and 75% confidence. The counts by level run from `L1` to the last nonempty level.

| Workbook | Transactions | Counts by level | Frequent itemsets | All rules | Strong rules |
| --- | ---: | --- | ---: | ---: | ---: |
| `Lecture_Example.xlsx` | 10 | 5, 9, 6, 1 | 21 | 68 | 26 |
| `Horizontal_Format.xlsx` | 5 | 7, 14, 12, 5, 1 | 39 | 200 | 104 |

In the lecture example, 5 of 10 baskets contain both A and B, 6 contain B, and 8 contain A. For the rule **B → A**, support is **5/10 = 50%**, confidence is **5/6 ≈ 83.33%**, and lift is **(5/6) ÷ (8/10) ≈ 1.0417**. It passes both thresholds. In the reverse direction, **A → B** has confidence **5/8 = 62.5%**, below the 75% threshold.

### Threshold experiments

The program varies minimum support over 20%, 30%, 40%, and 60% with confidence fixed at the configured value. It then varies minimum confidence over 50%, 75%, 80%, and 90% with support fixed. Each row reports the counts of frequent itemsets, all rules, and strong rules. On the lecture workbook at 30% support, raising confidence from 50% to 90% reduces the strong-rule count from 59 to 8. The 21 frequent itemsets and 68 candidate rules stay the same.

## How the implementation fits together

| Module | Role |
| --- | --- |
| `excel_reader.py` | Read the workbook and clean the transactions. |
| `apriori.py` | Count support, build the frequent singletons in L1, and keep the candidates that meet minimum support at each level. |
| `candidates.py` | Join sorted itemsets with a matching prefix. Prune a candidate if any subset of size one less is absent from the previous frequent level. |
| `association_rules.py` | Split each frequent itemset of size two or more into every nonempty antecedent and complementary consequent. Filter by support and confidence and report lift. |
| `experiments.py` | Run the two threshold experiments and collect counts. |
| `visualization.py` | Draw the support bar chart and the two threshold comparisons. |
| `main.py` | Connect the modules, set the input file and thresholds, and display results. |

The mining loop stops when there are no more candidates or no candidate meets minimum support. Lift compares a rule's confidence to the consequent's support. A lift above 1 indicates a positive association, 1 indicates independence, and below 1 indicates a negative association.

## Run the tests

From the project folder, run the full suite with Python's built-in test runner.

```bash
python -m unittest discover -s tests -v
```

To run the integration tests for the sample workbooks and the mining pipeline:

```bash
python -m unittest discover -s tests -p "test_integration.py" -v
```

The reviewed Phase 6 version passed **119 tests across 8 test files**, including the two additional tests for minimum-confidence validation and endpoint behavior. The suite covers Excel cleaning, support counting, candidate generation and pruning, Apriori levels, association rules, visualization, threshold experiments, and integration with both workbooks.

## Team responsibilities

| Member | Responsibility |
| --- | --- |
| Student 1 | Excel input, data preparation, and integration |
| Student 2 | Support counting and the Apriori engine |
| Student 3 | Candidate generation and pruning |
| Student 4 | Association rules, confidence, and lift |
| Student 5 | Visualization, threshold experiments, and testing |
