import pandas as pd
import csv 
from datetime import datetime
from data_entry import get_amount, get_catagory, get_date, get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date","amount","catagory","description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def intialize_csv(cls):
        try: 
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns= cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index= False)

    @classmethod
    def add_entry(cls, date, amount, catagory, description):
        new_entry = {
            "date" : date,
            "amount" : amount,
            "catagory" : catagory,
            "description" : description
        }
        with open(cls.CSV_FILE, "a",newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames= cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")


    @classmethod 
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format = CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"]<= end_date)
        filterd_df = df.loc[mask]

        if filterd_df.empty:
            print("No transactions found on the given date range")
        else: 
            print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            print(
                filterd_df.to_string(
                    index= False, 
                    formatters={"date": lambda x: x.strftime(CSV.FORMAT)}))
            
            total_income = filterd_df[filterd_df["catagory"] == "Income"]["amount"].sum()
            total_expense = filterd_df[filterd_df["catagory"] == "Expense"]["amount"].sum()
            print("\n Summary: ")
            print(f"Total Income : ${total_income: .2f}")
            print(f"Total Expenses : ${total_expense: .2f}")
            print(f"Net savings: ${(total_income - total_expense) : .2f}")

        return filterd_df


def add():
    CSV.intialize_csv()
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or Enter for today's date: ",
                    allow_default=True )
    amount = get_amount()
    catagory = get_catagory()
    description = get_description()
    CSV.add_entry(date, amount, catagory, description)

def plot_transactions(df):
    df.set_index("date", inplace = True)

    income_df = (
        df[df["catagory"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value = 0))
    
    expense_df = (
        df[df["catagory"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value = 0))
    
    plt.figure(figsize=(10,5))
    plt.plot(income_df.index , income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index , expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title('Income and expense over time')
    plt.legend()
    plt.grid(True)
    plt.show()



def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to see a plot? (y/n)").lower() == "y":
                plot_transactions(df)

        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1,2 or 3")

if __name__ == "__main__":
    main()