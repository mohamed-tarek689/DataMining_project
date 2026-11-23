
import unittest
from pathlib import Path
import pandas as pd

from excel_reader import (
    read_transactions,
    clean_transactions,
    remove_duplicates
)


class TestExcelReader(unittest.TestCase):

    # Test 1: Remove repeated items
    def test_remove_duplicates(self):
        items = ["M", "O", "O", "K"]
        result = remove_duplicates(items)

        self.assertEqual(result, ["M", "O", "K"])

    # Test 2: Remove extra spaces and empty items
    def test_clean_spaces(self):
        df = pd.DataFrame({
            "items": [" M, O, , K, "]
        })

        result = clean_transactions(df)

        self.assertEqual(result, [["M", "O", "K"]])

    # Test 3: Skip empty transactions
    def test_empty_rows(self):
        df = pd.DataFrame({
            "items": [None, "M,K", " , "]
        })

        result = clean_transactions(df)

        self.assertEqual(result, [["M", "K"]])

    # Test 4: Missing items column
    def test_missing_column(self):
        df = pd.DataFrame({
            "products": ["M,K"]
        })

        with self.assertRaises(ValueError):
            clean_transactions(df)

    # Test 5: No valid transactions
    def test_no_transactions(self):
        df = pd.DataFrame({
            "items": [None, "", " , "]
        })

        with self.assertRaises(ValueError):
            clean_transactions(df)

    # Test 6: File does not exist
    def test_missing_file(self):
        with self.assertRaises(ValueError):
            read_transactions("not_existing_file.xlsx")

    # Test 7: Read the actual Excel dataset
    def test_real_excel_file(self):
        project_dir = Path(__file__).resolve().parent.parent
        excel_path = project_dir / "Horizontal_Format.xlsx"

        df = read_transactions(excel_path)
        transactions = clean_transactions(df)

        self.assertEqual(len(transactions), 5)
        self.assertEqual(
            transactions[4],
            ["C", "O", "K", "I", "E"]
        )


if __name__ == "__main__":
    unittest.main()
