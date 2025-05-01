import json
from datetime import datetime
import os


class BudgetTracker:
    def __init__(self, app=None):
        self.app = app
        self.income = []
        self.expenses = []

    # ─── INCOME & EXPENSE HANDLERS ─────────────────────────────────────────────

    def add_income(self, amount, source, date=None, category=None):
        amount = self._validate_amount(amount, must_be_positive=True)
        if amount is None: return

        date = self._validate_date(date)
        if not date: return

        self.income.append({
            "amount": amount,
            "date": date,
            "source": source,
            "category": category or "general"
        })

    def add_expense(self, amount, category, date=None, expense_category=None):
        amount = self._validate_amount(amount, must_be_negative=True)
        if amount is None: return

        date = self._validate_date(date)
        if not date: return

        self.expenses.append({
            "amount": amount,
            "date": date,
            "category": category or "misc"
        })

    def add_transaction(self, description, amount, classification=None, date=None, category=None):
        classification = classification or ("income" if float(amount) > 0 else "expense")

        if classification.lower() == "income":
            self.add_income(amount, description, date, category)
        elif classification.lower() == "expense":
            self.add_expense(amount, description, date, category)
        else:
            self._notify(f"Unknown classification: {classification}")

    # ─── VALIDATION UTILITIES ──────────────────────────────────────────────────

    def _validate_amount(self, amount, must_be_positive=False, must_be_negative=False):
        try:
            amt = float(amount)
            if must_be_positive and amt <= 0:
                self._notify("Income must be a positive number.")
                return None
            if must_be_negative and amt >= 0:
                self._notify("Expense must be a negative number.")
                return None
            return amt
        except ValueError:
            self._notify("Invalid amount. Please enter a valid number.")
            return None

    def _validate_date(self, date_str):
        if not date_str:
            return datetime.now().strftime("%Y-%m-%d")
        for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"):
            try:
                return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
        self._notify("Invalid date format. Use YYYY-MM-DD or MM/DD/YYYY.")
        return None

    def _notify(self, message):
        if self.app and hasattr(self.app, "show_notification"):
            self.app.show_notification(message)
        else:
            print(message)

    # ─── FILE OPERATIONS ───────────────────────────────────────────────────────

    def save_data(self, filename="budget_data.json"):
        def do_save(create_backup):
            if create_backup:
                self.create_backup()
            self._write_json(filename, {
                "income": self.income,
                "expenses": self.expenses
            })
            self._notify("Data saved successfully.")

        if self.app and hasattr(self.app, "ask_backup_confirmation"):
            self.app.ask_backup_confirmation(do_save)
        else:
            do_save(create_backup=False)

    def save_data_quietly(self, filename="budget_data.json"):
        self._write_json(filename, {
            "income": self.income,
            "expenses": self.expenses
        })

    def _write_json(self, path, data):
        try:
            with open(path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self._notify(f"Error saving data: {e}")

    def load_data(self, filename="budget_data.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            self.income = data.get("income", [])
            self.expenses = data.get("expenses", [])
            self._notify(f"Loaded {len(self.income)} income and {len(self.expenses)} expenses.")
        except FileNotFoundError:
            self._notify(f"File not found: {filename}")
        except json.JSONDecodeError:
            self._notify(f"Error decoding JSON in {filename}")
        except Exception as e:
            self._notify(f"Error loading data: {e}")

    def create_backup(self, current="budget_data.json", backup="budget_data_backup.json"):
        if os.path.exists(backup):
            try:
                os.remove(backup)
            except Exception as e:
                self._notify(f"Could not remove old backup: {e}")
        if os.path.exists(current):
            try:
                os.rename(current, backup)
            except Exception as e:
                self._notify(f"Error creating backup: {e}")

    def load_transactions(self, filename="budget_data.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            transactions = []

            for i in data.get("income", []):
                transactions.append({
                    "date": i["date"],
                    "description": i.get("source", "income"),
                    "amount": i["amount"],
                    "category": i.get("category", "income"),
                    "classification": "income"
                })

            for e in data.get("expenses", []):
                transactions.append({
                    "date": e["date"],
                    "description": e.get("category", "expense"),
                    "amount": e["amount"],
                    "category": e.get("category", "expense"),
                    "classification": "expense"
                })
            print(f"Loaded {len(transactions)} transactions.")
            return transactions
        except Exception as e:
            self._notify(f"Error loading transactions: {e}")
            return []

    # ─── METRICS ───────────────────────────────────────────────────────────────

    def view_income(self):
        return sum(item["amount"] for item in self.income)

    def view_expense(self):
        return sum(item["amount"] for item in self.expenses)

    def view_balance(self):
        return self.view_income() - self.view_expense()

    def get_monthly_averages(self):
        def aggregate_by_month(entries):
            result = {}
            for entry in entries:
                month = entry["date"][:7]  # YYYY-MM
                result.setdefault(month, []).append(entry["amount"])
            return {month: sum(v) / len(v) for month, v in result.items()}

        return {
            "income_avg": aggregate_by_month(self.income),
            "expense_avg": aggregate_by_month(self.expenses)
        }
