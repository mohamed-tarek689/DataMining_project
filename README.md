# Apriori Algorithm – Data Mining Project

A Python project for mining frequent itemsets and association rules from transaction data stored in Excel. The Apriori algorithm will be implemented by the team rather than using a ready-made Apriori library.

## Project Requirements

Based on `Apriori_Description.pdf`, the project must:

1. Read transactions from an Excel file (horizontal transaction format).
2. Generate **all frequent itemsets** (`L1`, `L2`, ..., `Lk`) and display their support values.
3. Visualize frequent itemset support with bar charts.
4. Generate association rules from frequent itemsets.
5. Identify strong rules using minimum support and confidence.
6. Calculate **Lift** to measure item dependencies.
7. Run experiments with different minimum support and confidence values.
8. Provide Python (`.py`) source files.

## Tools

- **Python** — implementation
- **pandas** and **openpyxl** — reading Excel files
- **matplotlib** — support bar charts

Install dependencies:

```bash
pip install -r requirements.txt
```

## Planned Project Structure

```text
apriori-project/
├── data/                  # Excel transaction datasets
├── excel_reader.py        # Load and clean transactions
├── apriori.py             # Support counting and frequent itemsets
├── candidates.py          # Candidate generation and pruning
├── association_rules.py   # Rules, confidence, and lift
├── visualization.py       # Support bar charts
├── main.py                # Run the workflow and experiments
├── tests/                 # Test datasets and checks
├── requirements.txt
└── README.md
```

*Module names and responsibilities are an initial plan and may be refined during integration.*

## Workflow

1. Read and prepare transactions from Excel.
2. Find frequent 1-itemsets (`L1`) using **minimum support**.
3. Generate candidates, prune impossible candidates using the **Apriori property**, and calculate support.
4. Repeat for `L2` through `Lk` until no more frequent itemsets are found.
5. Generate association rules, calculate confidence and lift, and select strong rules.
6. Display results, plot support charts, and compare different thresholds.

## Running Tests (Terminal)

Tests use Python's built-in `unittest` module, so no additional testing package is required.

1. Open a terminal (PowerShell, Command Prompt, or the PyCharm terminal).
2. Navigate to the **project root** (the folder containing `main.py`, `excel_reader.py`, and `tests/`).
3. Install project dependencies if you have not already done so:

   ```bash
   python -m pip install -r requirements.txt
   ```

### Run all tests

To discover and run **every test file** inside `tests/`:

```bash
python -m unittest discover -s tests -v
```

### Run tests from one specific file

For example, to run only the Excel reader tests in `tests/test_excel_reader.py`:

```bash
python -m unittest discover -s tests -p "test_excel_reader.py" -v
```

Replace `test_excel_reader.py` with another test filename (such as `test_apriori.py`) when that file exists.

### Run one specific test (optional)

To run only `test_remove_duplicates` from the `TestExcelReader` class:

```bash
python -m unittest discover -s tests -p "test_excel_reader.py" -k test_remove_duplicates -v
```

### Reading the results

- `ok` means the test passed.
- `FAIL` means an assertion did not match the expected result.
- `ERROR` means an exception occurred while running a test.
- `Ran N tests` shows **how many tests actually ran**, not how many are written in the project.
- `OK` at the end means all tests that were executed passed; if you expected more tests, check the count.

**Test discovery:** Name test files `test_*.py` and test methods `test_*` so `unittest` can find them. Run the commands from the project root to make project imports work correctly. Tests are an internal quality check, not an explicit additional deliverable in `Apriori_Description.pdf`.

## Proposed Team Responsibilities

| Member | Responsibility |
|---|---|
| Student 1 | Excel input, data preparation, and integration |
| Student 2 | Support counting and Apriori engine |
| Student 3 | Candidate generation and pruning |
| Student 4 | Association rules, confidence, and lift |
| Student 5 | Visualization, threshold experiments, and testing |

**Integration agreement (planned):** The Excel reader supplies transactions as a list of lists. The Apriori modules return frequent itemsets grouped by level with their support values. The rules module uses these itemsets and a confidence threshold; the visualization module uses itemsets and support values.

## Status

**Planning stage.** Requirements and dependencies are identified; implementation, testing, and integration are not yet marked complete. Run instructions will be updated when `main.py` is implemented.

> Academic note: All submitted code should be understood and developed by the team in accordance with the instructor's rules on plagiarism and AI assistance.
