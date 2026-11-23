from excel_reader import read_transactions, clean_transactions
def main():
    df = read_transactions("Horizontal_Format.xlsx")

    transactions = clean_transactions(df)
    print(transactions)
if __name__ == "__main__":
    main()







