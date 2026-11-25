import csv
import json
import os
from datetime import datetime
from collections import defaultdict

import matplotlib.pyplot as plt

DATA_FILE = "expenses.csv"
BUDGET_FILE = "budget.json"
DATE_FORMAT = "%Y-%m-%d"
CATEGORIES = [
    "Food", "Transport", "Shopping", "Education",
    "Bills", "Health", "Entertainment", "Other"
]
FIELDS = ["id", "date", "category", "description", "amount"]


def ensure_files():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
    if not os.path.exists(BUDGET_FILE):
        save_budget(0)


def load_expenses():
    ensure_files()
    with open(DATA_FILE, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_expenses(expenses):
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(expenses)


def load_budget():
    ensure_files()
    try:
        with open(BUDGET_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return float(data.get("monthly_budget", 0))
    except (json.JSONDecodeError, ValueError, OSError):
        return 0.0


def save_budget(amount):
    with open(BUDGET_FILE, "w", encoding="utf-8") as f:
        json.dump({"monthly_budget": amount}, f, indent=4)


def read_amount(prompt):
    while True:
        try:
            amount = float(input(prompt))
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            return round(amount, 2)
        except ValueError:
            print("Please enter a valid number.")


def read_date(prompt="Enter date (YYYY-MM-DD) or press Enter for today: "):
    while True:
        value = input(prompt).strip()
        if not value:
            return datetime.today().strftime(DATE_FORMAT)
        try:
            datetime.strptime(value, DATE_FORMAT)
            return value
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD, for example 2026-11-25.")


def choose_category():
    print("\nCategories:")
    for i, category in enumerate(CATEGORIES, start=1):
        print(f"{i}. {category}")
    while True:
        try:
            choice = int(input("Choose category number: "))
            if 1 <= choice <= len(CATEGORIES):
                return CATEGORIES[choice - 1]
            print("Choose a number from the list.")
        except ValueError:
            print("Please enter a number.")


def next_id(expenses):
    ids = []
    for item in expenses:
        try:
            ids.append(int(item["id"]))
        except (ValueError, KeyError):
            pass
    return str(max(ids, default=0) + 1)


def add_expense():
    expenses = load_expenses()
    expense = {
        "id": next_id(expenses),
        "date": read_date(),
        "category": choose_category(),
        "description": input("Enter description: ").strip() or "No description",
        "amount": f"{read_amount('Enter amount: '):.2f}"
    }
    expenses.append(expense)
    save_expenses(expenses)
    print("Expense added successfully.")


def print_expenses(expenses):
    if not expenses:
        print("No expenses found.")
        return
    print("\nID | Date       | Category       | Description                 | Amount")
    print("-" * 78)
    for e in expenses:
        print(f"{e['id']:>2} | {e['date']} | {e['category']:<14} | "
              f"{e['description'][:25]:<25} | ₹{float(e['amount']):.2f}")


def view_expenses():
    print_expenses(load_expenses())


def find_expense(expenses, expense_id):
    return next((e for e in expenses if e["id"] == expense_id), None)


def edit_expense():
    expenses = load_expenses()
    print_expenses(expenses)
    expense_id = input("\nEnter expense ID to edit: ").strip()
    expense = find_expense(expenses, expense_id)
    if not expense:
        print("Expense ID not found.")
        return

    print("Press Enter to keep the current value.")
    new_date = input(f"Date [{expense['date']}]: ").strip()
    if new_date:
        try:
            datetime.strptime(new_date, DATE_FORMAT)
            expense["date"] = new_date
        except ValueError:
            print("Invalid date. Date was not changed.")

    new_description = input(f"Description [{expense['description']}]: ").strip()
    if new_description:
        expense["description"] = new_description

    change_category = input("Change category? (y/n): ").strip().lower()
    if change_category == "y":
        expense["category"] = choose_category()

    change_amount = input("Change amount? (y/n): ").strip().lower()
    if change_amount == "y":
        expense["amount"] = f"{read_amount('New amount: '):.2f}"

    save_expenses(expenses)
    print("Expense updated.")


def delete_expense():
    expenses = load_expenses()
    print_expenses(expenses)
    expense_id = input("\nEnter expense ID to delete: ").strip()
    expense = find_expense(expenses, expense_id)
    if not expense:
        print("Expense ID not found.")
        return
    confirm = input(f"Delete '{expense['description']}'? (y/n): ").strip().lower()
    if confirm == "y":
        expenses.remove(expense)
        save_expenses(expenses)
        print("Expense deleted.")
    else:
        print("Deletion cancelled.")


def category_summary():
    expenses = load_expenses()
    totals = defaultdict(float)
    for e in expenses:
        totals[e["category"]] += float(e["amount"])
    if not totals:
        print("No expenses to summarize.")
        return
    print("\nCategory-wise spending:")
    for category, total in sorted(totals.items(), key=lambda item: item[1], reverse=True):
        print(f"{category:<15} ₹{total:.2f}")
    print(f"Total: ₹{sum(totals.values()):.2f}")


def monthly_report():
    month = input("Enter month (YYYY-MM): ").strip()
    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month format.")
        return
    expenses = [e for e in load_expenses() if e["date"].startswith(month)]
    print(f"\nReport for {month}")
    print_expenses(expenses)
    total = sum(float(e["amount"]) for e in expenses)
    print(f"Monthly total: ₹{total:.2f}")


def set_budget():
    amount = read_amount("Enter monthly budget: ")
    save_budget(amount)
    print(f"Monthly budget set to ₹{amount:.2f}.")


def budget_status():
    budget = load_budget()
    month = input("Enter month (YYYY-MM) or press Enter for current month: ").strip()
    if not month:
        month = datetime.today().strftime("%Y-%m")
    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month format.")
        return
    spent = sum(float(e["amount"]) for e in load_expenses() if e["date"].startswith(month))
    remaining = budget - spent
    print(f"\nBudget for {month}: ₹{budget:.2f}")
    print(f"Spent: ₹{spent:.2f}")
    print(f"Remaining: ₹{remaining:.2f}")
    if budget > 0 and spent > budget:
        print("Warning: You have exceeded your budget.")
    elif budget > 0:
        print(f"Budget used: {spent / budget * 100:.1f}%")


def expense_chart():
    expenses = load_expenses()
    totals = defaultdict(float)
    for e in expenses:
        totals[e["category"]] += float(e["amount"])
    if not totals:
        print("Add expenses before creating a chart.")
        return
    categories = list(totals.keys())
    amounts = list(totals.values())
    plt.figure(figsize=(9, 5))
    plt.bar(categories, amounts)
    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount (₹)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig("expense_chart.png")
    plt.show()
    print("Chart saved as expense_chart.png")


def export_report():
    expenses = load_expenses()
    if not expenses:
        print("No expenses to export.")
        return
    filename = input("Report filename (Enter for expense_report.csv): ").strip()
    if not filename:
        filename = "expense_report.csv"
    if not filename.lower().endswith(".csv"):
        filename += ".csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(expenses)
    print(f"Report exported to {filename}")


def show_menu():
    print("\n" + "=" * 34)
    print("       SMART EXPENSE TRACKER")
    print("=" * 34)
    options = [
        "Add Expense", "View All Expenses", "Edit Expense",
        "Delete Expense", "Category-wise Summary", "Monthly Expense Report",
        "Set Monthly Budget", "View Budget Status", "Show Expense Chart",
        "Export Expense Report", "Exit"
    ]
    for number, option in enumerate(options, start=1):
        print(f"{number}. {option}")


def main():
    ensure_files()
    actions = {
        "1": add_expense,
        "2": view_expenses,
        "3": edit_expense,
        "4": delete_expense,
        "5": category_summary,
        "6": monthly_report,
        "7": set_budget,
        "8": budget_status,
        "9": expense_chart,
        "10": export_report
    }
    while True:
        show_menu()
        choice = input("Enter your choice (1-11): ").strip()
        if choice == "0":
            print("Thank you for using Smart Expense Tracker.")
            break
        if choice in actions:
            actions[choice]()
        else:
            print("Invalid choice. Please choose from 1 to 11, or 0 to exit.")


if __name__ == "__main__":
    main()
