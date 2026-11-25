# Smart Expense Tracker

A beginner-friendly Python mini project for tracking personal expenses from the command line.

## Features
- Add, view, edit, and delete expenses
- Expense categories and category-wise totals
- Monthly expense report
- Monthly budget and remaining-budget status
- Bar chart of category spending
- Export expenses to CSV
- Persistent storage using CSV and JSON files

## Requirements
- Python 3.9+
- Matplotlib

## Setup in VS Code
1. Open this folder in VS Code.
2. Open Terminal → New Terminal.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run:

   ```bash
   python main.py
   ```

## Data files
The program automatically creates:
- `expenses.csv` to store expense records
- `budget.json` to store the monthly budget

Keep these files in the same folder as `main.py`.

## Usage
Run the program and choose an option from the menu. Dates use `YYYY-MM-DD` and month reports use `YYYY-MM`.

## Learning concepts
Functions, loops, conditionals, lists, dictionaries, CSV file handling, JSON, date handling, exception handling, and Matplotlib.

## Disclaimer
This is an educational project. It is not a banking or financial application.
