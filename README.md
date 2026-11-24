# Apriori Algorithm – Data Mining Project

A Python implementation of the Apriori algorithm for mining frequent itemsets and association rules from transactional data stored in Excel. The team implements the Apriori logic directly rather than relying on a ready-made Apriori library.

## Project Status

**Phase 3 completed:** Excel data preparation, support counting, the Apriori engine, and candidate generation and pruning are implemented and integrated. The program currently generates all frequent itemset levels and displays their support values.

| Member | Responsibility | Status |
| --- | --- | --- |
| Student 1 | Excel input, data preparation, and integration | Data preparation implemented |
| Student 2 | Support counting and Apriori engine | Implemented and tested |
| Student 3 | Candidate generation and pruning | Implemented, tested, and integrated |
| Student 4 | Association rules, confidence, and lift | Pending integration |
| Student 5 | Visualization, threshold experiments, and testing | Pending integration |

The association rule and visualization modules are not yet present in the repository. Their test files are currently empty. The full project is not yet ready for final delivery.

## Project Requirements

Based on `Apriori_Description.pdf`, the project must:

- [x] Read transactions from an Excel file (horizontal transaction format).
- [x] Generate frequent itemsets and display their support values.
- [ ] Visualize frequent itemset support using bar charts.
- [ ] Generate association rules from frequent itemsets.
- [ ] Extract strong association rules.
- [ ] Calculate Lift to measure item dependencies.
- [ ] Run experiments with different minimum support and confidence values (support tested; confidence pending).
- [x] Generate all frequent itemset levels (`L1`, `L2`, ..., `Lk`).
- [ ] Provide the complete Python (`.py`) source files for final delivery (current modules are available).

## Tools and Dependencies

- Python 3 — implementation and built-in `unittest` testing
- `pandas` and `openpyxl` — reading Excel files
- `matplotlib` — planned support bar charts

Install dependencies from the project root:

```bash
python -m pip install -r requirements.txt
```

## Current Project Structure

```text
DataMining_project/
├── Horizontal_Format.xlsx
├── excel_reader.py
├── apriori.py
├── candidates.py
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── tests/
    ├── test_excel_reader.py
    ├── test_support.py
    ├── test_apriori.py
    ├── test_candidate_generation.py
    ├── test_integration.py
    ├── test_association_rules.py   # Placeholder (empty)
    └── test_visualization.py      # Placeholder (empty)
```

Planned modules: `association_rules.py` and `visualization.py`.

## Algorithm Workflow

1. Read the Excel file and clean the transaction data.
2. Calculate support for individual items and generate `L1`.
3. Sort and deduplicate the previous frequent itemsets, then join those with a matching prefix to generate candidates.
4. Apply candidate pruning using the Apriori property: every subset of size `k - 1` must be frequent. This step is unnecessary for `C2`.
5. Calculate the support of the remaining candidates and retain those meeting minimum support to produce `Lk`.
6. Repeat until no candidates or no frequent itemsets remain.
7. **Planned:** Generate association rules, calculate confidence and lift, and identify strong rules.
8. **Planned:** Visualize support values and compare different support and confidence thresholds.

## Module Responsibilities and Interfaces

| Module | Main functions | Responsibility |
| --- | --- | --- |
| `excel_reader.py` | `read_transactions`, `clean_transactions`, `remove_duplicates` | Read and normalize Excel transactions |
| `apriori.py` | `compute_initial_l1`, `contains_all_items`, `filter_candidates_by_support`, `run_level_filtering`, `validate_min_support` | Support counting, frequent itemset filtering, and level-wise iteration |
| `candidates.py` | `join_itemsets`, `prune_candidates`, `generate_candidates` | Joining, candidate pruning, lexicographic ordering, and duplicate prevention |
| `main.py` | `main` | Connect the implemented modules and print frequent itemsets |

### Integration Contract

- Transactions are represented as a list of lists of strings, e.g. `[["A", "B"], ["A", "C"]]`.
- The Excel file must contain an `items` column with comma-separated items. Cleaning strips whitespace, converts items to uppercase, removes duplicates within each transaction, and skips empty transactions.
- Itemsets are represented as tuples of distinct items in lexicographic order, e.g. `("A", "B")`.
- `generate_candidates(prev_itemsets, level_k)` receives a list of frequent `(k - 1)`-itemset tuples and returns a list of candidate `k`-itemset tuples after joining and pruning. It assumes valid levels (`k >= 2`) and sorted input tuples.
- `run_level_filtering(transactions, initial_L1, generate_candidates_fn, min_support)` receives the candidate generation function and returns a dictionary of levels, with each level containing itemset tuples mapped to their support values.
- Minimum support is a fraction in the range `(0, 1]`; support is calculated as the number of transactions containing the itemset divided by the total number of transactions.

Example output structure (illustrative):

```python
{
    1: {("A",): 0.75, ("B",): 0.75, ("C",): 0.5},
    2: {("A", "B"): 0.5, ("A", "C"): 0.5, ("B", "C"): 0.5},
    3: {("A", "B", "C"): 0.5}
}
```

The planned association rule module will consume frequent itemsets and a minimum confidence threshold; the visualization module will consume itemsets and their support values.

## Running the Project

Clone or download the repository, then navigate to the project root:

```bash
git clone https://github.com/mohamed-tarek689/DataMining_project.git
cd DataMining_project
python -m pip install -r requirements.txt
python main.py
```

The current program reads `Horizontal_Format.xlsx` from the project root. The default minimum support in `main.py` is `0.6` (60%). To try a different threshold, change the `min_support` value in `main.py` and run the program again.

With the supplied dataset and 60% minimum support, the expected frequent itemsets are:

| Level | Itemset | Support |
| --- | --- | ---: |
| L1 | E | 0.8 |
| L1 | K | 1.0 |
| L1 | M | 0.6 |
| L1 | O | 0.6 |
| L1 | Y | 0.6 |
| L2 | E, K | 0.8 |
| L2 | E, O | 0.6 |
| L2 | K, M | 0.6 |
| L2 | K, O | 0.6 |
| L2 | K, Y | 0.6 |
| L3 | E, K, O | 0.6 |

The order of entries printed within `L1` may vary without changing the result.

### Validation at Different Minimum Support Thresholds

| Minimum support | L1 | L2 | L3 | L4 | L5 | L6 | Total frequent itemsets |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 20% | 11 | 36 | 51 | 36 | 13 | 2 | 149 |
| 60% | 5 | 5 | 1 | 0 | 0 | 0 | 11 |

These results were observed in local runs and are consistent with the sample transactions used in Section 2. Confidence-based experiments will be added after association rule generation is implemented.

## Running Tests (Terminal)

Tests use Python's built-in `unittest` module, so no additional testing package is required. Open a terminal (PowerShell, Command Prompt, or the PyCharm terminal) in the project root and install the dependencies first.

### Run all tests

```bash
python -m unittest discover -s tests -v
```

### Run a specific test file

```bash
python -m unittest discover -s tests -p "test_excel_reader.py" -v
python -m unittest discover -s tests -p "test_candidate_generation.py" -v
python -m unittest discover -s tests -p "test_integration.py" -v
```

### Run one specific test (optional)

```bash
python -m unittest discover -s tests -p "test_excel_reader.py" -k test_remove_duplicates -v
```

### Current Test Results

Latest team-reported local results at the Phase 3 milestone:

| Test suite | Passed |
| --- | ---: |
| Candidate generation unit tests | 17 / 17 |
| Integration tests | 4 / 4 |
| Full regression suite | 51 / 51 |

The full regression suite includes the candidate generation and integration tests; the counts are not additive. The current tests cover Excel preparation, support counting, the Apriori engine, candidate generation, and integration of the two Apriori modules. Association rule and visualization tests are still pending.

### Reading the results

- `ok` means the test passed.
- `FAIL` means an assertion did not match the expected result.
- `ERROR` means an exception occurred while running a test.
- `Ran N tests` shows how many tests actually ran.
- `OK` means all executed tests passed; check the test count as well.

**Test discovery:** Name test files `test_*.py` and test methods `test_*`. Run commands from the project root so imports resolve correctly. Tests are an internal quality check, not an explicit additional deliverable in `Apriori_Description.pdf`.

## Remaining Work

1. Implement association rule generation, confidence, strong rule filtering, and lift.
2. Implement bar charts of frequent itemset support.
3. Integrate the remaining modules into `main.py` and run experiments with different support and confidence thresholds.
4. Add the remaining unit and integration tests and rerun the complete regression suite.
5. Verify every official requirement before final delivery and prepare for the project discussion.

> Academic note: All submitted code should be understood and developed by the team in accordance with the instructor's rules on plagiarism and AI assistance.
