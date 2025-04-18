# classes and functions
import json
from datetime import datetime
import os

# main CLI logic

class BudgetTracker:
    def __init__(self, app):
        self.app = app
        self.income = []
        self.expenses = []
    
    # Accepts amount and desc, and stores them in a list with the current date
    def add_income(self, amount, source, date=None):
        try:
            amount = float(amount)
        except ValueError:
            self.app.show_notification("Invalid amount. Please enter a number.")
            return
        if amount < 0:
            self.app.show_notification("Amount cannot be negative.")
            return

        # Validate or default the date
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")  # Default to today's date
        else:
            date = self.parse_date(date)  # Use the new parse_date method
            if not date:
                self.app.show_notification("Invalid date format. Please use YYYY-MM-DD or MM/DD/YYYY.")
                return

        try:
            self.income.append({"amount": amount, "date": date, "source": source})
            self.app.show_notification(f"Income of ${amount:.2f} added on {date}.")
        except Exception as e:
            self.app.show_notification(f"Error: {e}")
    
    def add_expense(self, amount, category, date=None):
        try:
            amount = float(amount)
        except ValueError:
            self.app.show_notification("Invalid amount. Please enter a number.")
            return
        if amount < 0:
            self.app.show_notification("Amount cannot be negative.")
            return

        # Validate or default the date
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")  # Default to today's date
        else:
            date = self.parse_date(date)  # Use the new parse_date method
            if not date:
                self.app.show_notification("Invalid date format. Please use YYYY-MM-DD or MM/DD/YYYY.")
                return

        try:
            self.expenses.append({"amount": amount, "date": date, "category": category})
            self.app.show_notification(f"Expense of ${amount:.2f} added on {date}.")
        except Exception as e:
            self.app.show_notification(f"Error: {e}")

    def parse_date(self, date_str):
        """Attempt to parse the date string with multiple formats and return it in YYYY-MM-DD format."""
        formats = ["%Y-%m-%d", "%m/%d/%Y", "%m-%d-%Y", "%d/%m/%Y", "%d-%m-%Y"]
        for fmt in formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                return parsed_date.strftime("%Y-%m-%d")  # Reformat to YYYY-MM-DD
            except ValueError:
                continue
        return None  # Return None if no format matches

    # view total income
    def view_income(self):
        if not self.income:
            print("No income entries found")
            return 0.0
        else:
            try:
                total_income = sum(item["amount"] for item in self.income)
                print(total_income)
                return total_income
            except Exception as e:
                print(e)
                return 0.0

    # view total expenses
    def view_expense(self):
        if not self.expenses:
            print("No income entries found")
            return 0.0
        else:
            try:
                total_expenses = sum(item["amount"] for item in self.expenses)
                print("Total expenses: ${:.2f}".format(total_expenses))
                return total_expenses
            except Exception as e:
                print(e)
                return 0.0

    # get balance
    def view_balance(self):

        if not self.income and not self.expenses:
            print("No entries found, balances set to 0")
            total_income = 0
            total_expenses = 0
            balance = total_income - total_expenses
            return balance
        
        try:
            total_income = self.view_income()
            total_expenses = self.view_expense()
            balance = total_income - total_expenses
            print(f"Your balance is: ${balance:.2f}")
            return balance
        except Exception as e:
            print(e)
            return 0.0

    # save data to json file
    def save_data(self, filename="budget_data.json"):
        # ask the user if they want to create a backup of the current data
        create_backup = input("Do you want to create a backup of the current data? (y/n): ").strip().lower()
        if create_backup == "y":
            # check if budget_data.json exists, if it doesnt create it
            self.create_backup
            # save current data to budget_data.json
        else:
            print("No backup created")
        # save current data to budget_data.json
        data = {
            "income": self.income,
            "expenses": self.expenses
        }
        try:
            with open(filename, "w") as file:
                json.dump(data, file)
            print(f"Data saved successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(e)

    # load data from json file
    def load_data(self, filename="budget_data.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                self.income = data.get("income", [])
                self.expenses = data.get("expenses", [])
            print(f"Loaded {len(self.income)} income entries and {len(self.expenses)} expense entries")
        except FileNotFoundError:
            print("No previous data found. Starting fresh.")
        except json.JSONDecodeError:
            print("Error decoding JSON data. Starting fresh.")
        except Exception as e:
            print(e)

    def create_backup(self, current_filename="budget_data.json", backup_filename="budget_data_backup.json"):
        if os.path.exists(backup_filename):
            try:
                os.remove(backup_filename)
                print("Previous backup deleted successfully")
            except Exception as e:
                print(f"Error deleting backup: {e}")
        if os.path.exists(current_filename):
            try:
                os.rename(current_filename, backup_filename)
                print("Backup created successfully")
            except Exception as e:
                print(f"Error creating backup: {e}")

    def get_monthly_averages(self):
        if not self.income and not self.expenses:
            print("No entries found")
            return
        try:
            income_by_month = {}
            expenses_by_month = {}
            for item in self.income:
                month = item["date"][:7]  # YYYY-MM format
                income_by_month.setdefault(month, []).append(item["amount"])
            for item in self.expenses:
                month = item["date"][:7]  # YYYY-MM format
                expenses_by_month.setdefault(month, []).append(item["amount"])
            monthly_income_averages = {month: sum(amounts) / len(amounts) for month, amounts in income_by_month.items()}
            monthly_expenses_averages = {month: sum(amounts) / len(amounts) for month, amounts in expenses_by_month.items()}
            print("Monthly Income Averages:", monthly_income_averages)
            print("Monthly Expenses Averages:", monthly_expenses_averages)
            return monthly_income_averages, monthly_expenses_averages
        except Exception as e:
            print(e)
    
    def forecast_next_month_balance(self):
        get_monthly_averages = self.get_monthly_averages()
        if not get_monthly_averages:
            print("No monthly averages found")
            return
        try:
            monthly_income_averages, monthly_expenses_averages = get_monthly_averages
            next_month_income = sum(monthly_income_averages.values()) / len(monthly_income_averages)
            next_month_expenses = sum(monthly_expenses_averages.values()) / len(monthly_expenses_averages)
            current_balance = self.view_balance() or 0
            forecasted_balance = current_balance + (next_month_income - next_month_expenses)
            print(f"Average monthly income: ${next_month_income:.2f}")
            print(f"Average monthly expenses: ${next_month_expenses:.2f}")
            print(f"Current balance: ${current_balance:.2f}")
            print(f"Next month's forecasted balance: ${forecasted_balance:.2f}")
            return forecasted_balance
        except Exception as e:
            print(e)