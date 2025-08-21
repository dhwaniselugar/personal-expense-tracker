import csv
import datetime

FILENAME = "expenses.csv"

def load_expenses(filename):
    """
    Loads expenses from a CSV file.
    Args:
        filename (str): The name of the CSV file to load from.
    Returns:
        list: A list of expense dictionaries.
    """
    expenses = []
    try:
        with open(filename, mode='r', newline='') as f:
            reader = csv.reader(f)
            next(reader) # Skip header row
            for row in reader:
                # Create a dictionary for each expense and handle data types
                expense = {
                    'date': row[0],
                    'category': row[1],
                    'amount': float(row[2]),
                    'description': row[3]
                }
                expenses.append(expense)
    except FileNotFoundError:
        # If the file doesn't exist, return an empty list.
        return []
    return expenses

def save_expenses(filename, expenses_list):
    """
    Saves the list of expenses to a CSV file.
    Args:
        filename (str): The name of the CSV file to save to.
        expenses_list (list): The list of expense dictionaries to save.
    """
    with open(filename, mode='w', newline='') as f:
        fieldnames = ['date', 'category', 'amount', 'description']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(expenses_list)
    print("Expenses saved successfully!")

def add_expense(expenses_list):
    """
    Prompts the user for expense details, validates them,
    and adds the new expense to the list.
    Args:
        expenses_list (list): The list to which the new expense will be added.
    """
    # Get and validate the date
    while True:
        date_str = input("Enter the date of the expense (YYYY-MM-DD): ")
        try:
            datetime.datetime.strptime(date_str, '%Y-%m-%d')
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    # Get and validate the amount
    while True:
        try:
            amount = float(input("Enter the amount spent: "))
            break
        except ValueError:
            print("Invalid amount. Please enter a number.")

    category = input("Enter the category (e.g., Food, Travel): ")
    description = input("Enter a brief description: ")

    new_expense = {
        'date': date_str,
        'category': category,
        'amount': amount,
        'description': description
    }
    expenses_list.append(new_expense)
    print("\nExpense added successfully!")

def view_expenses(expenses_list):
    """
    Displays all expenses in a formatted table.
    Args:
        expenses_list (list): The list of expenses to display.
    """
    if not expenses_list:
        print("\nNo expenses recorded yet.")
        return

    print("\n--- All Expenses ---")
    print(f"{'Date':<12} | {'Category':<15} | {'Amount':<10} | {'Description'}")
    print("-" * 60)
    for expense in expenses_list:
        print(f"{expense['date']:<12} | {expense['category']:<15} | ${expense['amount']:<9.2f} | {expense['description']}")
    print("-" * 60)

def track_budget(expenses_list):
    """
    Calculates total expenses and compares them against a user-set budget.
    Args:
        expenses_list (list): The list of expenses to calculate the total from.
    """
    # Get and validate the budget
    while True:
        try:
            budget = float(input("Enter your monthly budget: "))
            if budget < 0:
                print("Budget must be a positive number.")
                continue
            break
        except ValueError:
            print("Invalid amount. Please enter a number.")

    # Calculate total expenses using a sum of a generator expression
    total_expenses = sum(expense['amount'] for expense in expenses_list)
    remaining_balance = budget - total_expenses

    print("\n--- Budget Summary ---")
    print(f"Total Budget:    ${budget:.2f}")
    print(f"Total Expenses:  ${total_expenses:.2f}")
    print("-" * 25)

    if remaining_balance >= 0:
        print(f"✅ You have ${remaining_balance:.2f} left for the month.")
    else:
        print(f"⚠️ You have exceeded your budget by ${abs(remaining_balance):.2f}!")

def main():
    """
    The main function to run the expense tracker application.
    """
    expenses = load_expenses(FILENAME)

    while True:
        print("\n--- Personal Expense Tracker ---")
        print("1. Add an expense")
        print("2. View expenses")
        print("3. Track budget")
        print("4. Save expenses")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            add_expense(expenses)
        elif choice == '2':
            view_expenses(expenses)
        elif choice == '3':
            track_budget(expenses)
        elif choice == '4':
            save_expenses(FILENAME, expenses)
        elif choice == '5':
            save_expenses(FILENAME, expenses)
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

# Entry point of the script
if __name__ == "__main__":
    main()