from pathlib import Path
import pandas as pd

# check if the file is exists or not
def read_transactions(file):
    file = Path(file)

    if not file.exists():
        raise ValueError(f"File not found: {file}")

    file_df = pd.read_excel(file)

    return file_df

#remove_duplicates
def remove_duplicates(items):
    unique_items = []

    for item in items:
        if item not in unique_items:
            unique_items.append(item)

    return unique_items

#convert df to list
def clean_transactions(file_df):
    if "items" not in file_df.columns:
        raise ValueError("Excel file must contain an 'items' column")

    transactions = []

    for value in file_df["items"]:
        #if value is null dont insert in set
        if pd.isna(value):
            continue

        items = []

        for item in str(value).split(","):#convert df to string and add char in item
            item = item.strip()

            if item:
                items.append(item)

        if items:
            transactions.append(remove_duplicates(items))

    if not transactions:
        raise ValueError("No valid transactions found")

    return transactions


def main():
    df = read_transactions("Horizontal_Format.xlsx")

    transactions = clean_transactions(df)
    print(transactions)
if __name__ == "__main__":
    main()







