import csv
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from data_entry import (
  get_amount, get_category, get_date, get_description
)

class CSV:
  CSV_FILE = "finance_data.csv"
  COLUMNS = ['Date', 'Amount', 'Category', 'Description']
  DATE_FORMAT="%d-%m-%Y"

  @classmethod
  def initalize_csv(cls):
    try:
      pd.read_csv(cls.CSV_FILE) 
    except FileNotFoundError:
      df = pd.DataFrame(columns=cls.COLUMNS)
      df.to_csv(cls.CSV_FILE, index=False)

  @classmethod
  def add_entry(cls, date, amount, category, description):
    new_entry = {
      "Date" : date,
      "Amount" : amount,
      "Category" : category,
      "Description" : description
    }
    with open(cls.CSV_FILE, 'a', newline='') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS) 
      writer.writerow(new_entry)
    print("Entry added successfully")
  
  @classmethod
  def get_transactions(cls, start_date, end_date):
    df = pd.read_csv(cls.CSV_FILE)
    df["Date"] = pd.to_datetime(df["Date"], format=CSV.DATE_FORMAT)
    start_date = datetime.strptime(start_date, CSV.DATE_FORMAT)
    end_date = datetime.strptime(end_date, CSV.DATE_FORMAT)

    mask = (df["Date"] >= start_date) & (df["Date"] <= end_date)
    filtered_df = df.loc[mask]

    if filtered_df.empty:
      print("No transactions found in the given date range")
    else:
      print(
        f"Transactions from {start_date.strftime(CSV.DATE_FORMAT)} to {end_date.strftime(CSV.DATE_FORMAT)}"
        )
      print(
        filtered_df.to_string(
          index=False, formatters={'Date' : lambda x: x.strftime(CSV.DATE_FORMAT)}
          )
        )
      
      total_income = filtered_df[filtered_df['Category'] == 'Income']['Amount'].sum()
      total_expense = filtered_df[filtered_df['Category'] == 'Expense']['Amount'].sum()
      print("\nSummary:")
      print(f"Total Income: {total_income:.2f}")
      print(f"Total Expense: {total_expense:.2f}")
      print(f"Net Savings: {total_income - total_expense:.2f}")
    return filtered_df 

def add_transaction():
  CSV.initalize_csv()
  date = get_date(
    """
    Enter the date of the transaction as following:
    'dd-mm-yyyy' (dd=date, mm=month, yyyy=year): """, allow_default=True)
  amount = get_amount()
  category = get_category()
  description = get_description()
  CSV.add_entry(date, amount, category, description)

def plot_transaction(df, save=False):
  df.set_index('Date', inplace=True)

  income_df = (
    df[df['Category'] == 'Income']
    .resample("D")
    .sum()
    .reindex(df.index, fill_value=0)
  )
  expense_df = (
    df[df['Category'] == 'Expense']
    .resample("D")
    .sum()
    .reindex(df.index, fill_value=0)
  )
  plt.figure(figsize=(10, 5))
  plt.plot(income_df.index, income_df['Amount'], label='Income', color='g')
  plt.plot(expense_df.index, expense_df['Amount'], label='Expense', color='r')
  plt.xlabel('Date')
  plt.ylabel('Amount')
  plt.title('Income and Expenses Over Time')
  plt.legend()
  plt.grid(True)
  plt.show()
  if save:
    plt.savefig("plot.png")


def main():
  while True:
    print("\n1. Add a new transaction")
    print("2. View transactions and a summary within a date range")
    print("3. Exit")
    choice = input("Enter your choice {1-3}: ")
    
    if choice == '1':
      add_transaction()
    elif choice == '2':
      start_date = get_date("Enter the start date (dd-mm-yy): ")
      end_date = get_date("Enter the end date (dd-mm-yy): ")
      df = CSV.get_transactions(start_date, end_date)
      if input("Do you want to see plot? (y/n)").lower() == 'y':
        if input("Do you want to save it? (y/n)").lower() == 'y':
          plot_transaction(df, save=True)
        else:
          plot_transaction(df)
    elif choice == '3':
      print("Exiting...")
      break
    else:
      print("Invalid choice. Enter {1-3}")

if __name__ == '__main__':
  main()
