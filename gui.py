import sys, csv, os
import pandas as pd
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QTextEdit, QDialog, QLineEdit, QFileDialog, QMessageBox,
    QTableWidget, QTableWidgetItem
)
from PySide6.QtGui import QFont
from tracker import BudgetTracker
from gpt_advisor import analyze_budget, create_budget, async_categorize_transaction
import asyncio
import re

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Penny Pilot")
        self.setFixedSize(700, 700)

        self.tracker = BudgetTracker(None)
        self.tracker.load_data()

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        title = QLabel("Piloting to a better budget...")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        main_layout.addWidget(title)

        logs = QHBoxLayout()
        self.income_text = QTextEdit(); self.income_text.setReadOnly(True)
        self.expense_text = QTextEdit(); self.expense_text.setReadOnly(True)
        logs.addWidget(self._wrap_group("Income", self.income_text))
        logs.addWidget(self._wrap_group("Expenses", self.expense_text))
        main_layout.addLayout(logs)

        buttons = QGridLayout()
        self._add_button(buttons, "Add Income", self.add_income_dialog, 0, 0)
        self._add_button(buttons, "Add Expense", self.add_expense_dialog, 0, 1)
        self._add_button(buttons, "View Summary", self.view_summary, 0, 2)
        self._add_button(buttons, "Save Data", self.tracker.save_data, 1, 0)
        self._add_button(buttons, "Load Data", lambda: (self.tracker.load_data(), self.update_logs()), 1, 1)
        self._add_button(buttons, "Get GPT Advice", self.get_gpt_advice, 1, 2)
        self._add_button(buttons, "Clear Data", self.clear_data, 2, 0)
        self._add_button(buttons, "Generate Budget", self.generate_budget, 2, 1)
        self._add_button(buttons, "Upload Statement", self.upload_statement, 2, 2)
        self._add_button(buttons, "Manage Transactions", self.manage_transactions, 3, 0)
        self._add_button(buttons, "Exit", self.close, 3, 1, 1, 2)
        main_layout.addLayout(buttons)

        self.update_logs()

    def _wrap_group(self, label, widget):
        wrapper = QWidget(); layout = QVBoxLayout(wrapper)
        layout.addWidget(QLabel(label)); layout.addWidget(widget)
        return wrapper

    def _add_button(self, layout, text, func, row, col, rowspan=1, colspan=1):
        btn = QPushButton(text); btn.clicked.connect(func)
        layout.addWidget(btn, row, col, rowspan, colspan)

    def update_logs(self):
        self.income_text.clear(); self.expense_text.clear()
        for i in self.tracker.income:
            self.income_text.append(f"{i['date']}: ${i['amount']} ({i['source']})")
        for e in self.tracker.expenses:
            self.expense_text.append(f"{e['date']}: ${e['amount']} ({e['category']})")

    def add_income_dialog(self):
        self._data_dialog("Add Income", ["Amount", "Source", "Date"], self.tracker.add_income)

    def add_expense_dialog(self):
        self._data_dialog("Add Expense", ["Amount", "Category", "Date"], self.tracker.add_expense)

    def _data_dialog(self, title, fields, handler):
        dlg = QDialog(self); dlg.setWindowTitle(title); layout = QVBoxLayout(dlg)
        entries = [QLineEdit(placeholderText=f) for f in fields]
        for entry in entries: layout.addWidget(entry)
        submit_btn = QPushButton("Submit"); layout.addWidget(submit_btn)
        def submit():
            try:
                handler(*(e.text() for e in entries))
                self.update_logs(); dlg.accept()
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))
        submit_btn.clicked.connect(submit); dlg.exec()

    def view_summary(self):
        i = self.tracker.view_income(); e = self.tracker.view_expense(); b = self.tracker.view_balance()
        QMessageBox.information(self, "Summary", f"Income: ${i:.2f}\\nExpenses: ${e:.2f}\\nBalance: ${b:.2f}")

    def clear_data(self):
        self.tracker.income.clear(); self.tracker.expenses.clear(); self.update_logs()
        QMessageBox.information(self, "Cleared", "All data cleared.")

    def get_gpt_advice(self):
        dlg = QDialog(self); dlg.setWindowTitle("GPT Advice")
        layout = QVBoxLayout(dlg)
        text = QTextEdit(); text.setReadOnly(True)
        text.setPlainText(analyze_budget(self.tracker.income, self.tracker.expenses))
        layout.addWidget(text); layout.addWidget(QPushButton("Close", clicked=dlg.accept))
        dlg.exec()

    def generate_budget(self):
        dlg = QDialog(self); dlg.setWindowTitle("Generated Budget")
        layout = QVBoxLayout(dlg)
        text = QTextEdit(); text.setReadOnly(True)
        text.setPlainText(create_budget(self.tracker.income, self.tracker.expenses))
        layout.addWidget(text); layout.addWidget(QPushButton("Close", clicked=dlg.accept))
        dlg.exec()

    def upload_statement(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Statement", "", "CSV Files (*.csv);;Excel Files (*.xlsx)")
        if not path: return
        try:
            if path.endswith(".csv"):
                with open(path, newline='') as f:
                    for row in csv.DictReader(f):
                        self._process_row(row.get("Description"), row.get("Amount"))
            elif path.endswith(".xlsx"):
                df = pd.read_excel(path)
                for _, row in df.iterrows():
                    self._process_row(row.get("Description"), row.get("Amount"))
            elif path.endswith(".pdf"):
                import fitz  # PyMuPDF
                doc = fitz.open(path)
                text = ""
                for page in doc:
                    text += page.get_text()

                lines = text.splitlines()
                temp_date = None
                temp_description_lines = []

                AMOUNT_REGEX = re.compile(r"^-?\\$?\\d[\\d,]*\\.\\d{2}$")
                DATE_REGEX = re.compile(r"^\\d{2}/\\d{2}/(\\d{2}|\\d{4})$")

                for line in lines:
                    line = line.strip()
                    if not line:
                        continue

                    if DATE_REGEX.match(line):
                        temp_date = line
                        temp_description_lines = []

                    elif AMOUNT_REGEX.match(line):
                        if temp_date and temp_description_lines:
                            description = " ".join(temp_description_lines)
                            amount = line.replace("$", "").replace(",", "")
                            try:
                                amount = float(amount)
                                classification = "income" if amount > 0 else "expense"
                                category = asyncio.run(async_categorize_transaction(description))
                                self.tracker.add_transaction(description, amount, classification, temp_date, category)
                            except:
                                continue
                        temp_date = None
                        temp_description_lines = []

                    else:
                        temp_description_lines.append(line)

                self.update_logs()
                QMessageBox.information(self, "Uploaded", "PDF transactions imported.")
            self.update_logs()
            QMessageBox.information(self, "Uploaded", "Transactions imported.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _process_row(self, desc, amt):
        if not desc or not amt: return
        try:
            amt = float(amt.replace("$", "").replace(",", ""))
            classification = "income" if amt > 0 else "expense"
            loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop)
            category = loop.run_until_complete(async_categorize_transaction(desc))
            date = "2024-01-01"
            self.tracker.add_transaction(desc, amt, classification, date, category)
        except Exception as e:
            print("Row error:", e)

    def manage_transactions(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Manage Transactions")
        dlg.resize(700, 400)
        layout = QVBoxLayout(dlg)

        table = QTableWidget()
        transactions = self.tracker.load_transactions()
        table.setRowCount(len(transactions))
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Date", "Description", "Amount", "Category"])

        for i, t in enumerate(transactions):
            table.setItem(i, 0, QTableWidgetItem(t["date"]))
            table.setItem(i, 1, QTableWidgetItem(t["description"]))
            table.setItem(i, 2, QTableWidgetItem(str(t["amount"])))
            table.setItem(i, 3, QTableWidgetItem(t["category"]))

        layout.addWidget(table)

        # Delete Button
        def delete_selected():
            selected = table.currentRow()
            if selected < 0:
                QMessageBox.warning(dlg, "No Selection", "Please select a row to delete.")
                return

            txn = transactions[selected]
            # Attempt to remove from income or expenses
            found = False
            for lst in [self.tracker.income, self.tracker.expenses]:
                for entry in lst:
                    if (
                        entry["amount"] == txn["amount"]
                        and entry["date"] == txn["date"]
                        and entry.get("source", entry.get("category")) == txn["description"]
                    ):
                        lst.remove(entry)
                        found = True
                        break
                if found:
                    break

            if found:
                self.tracker.save_data_quietly()
                self.update_logs()
                table.removeRow(selected)
                QMessageBox.information(dlg, "Deleted", "Transaction removed.")
            else:
                QMessageBox.warning(dlg, "Not Found", "Could not find matching transaction.")

        delete_btn = QPushButton("Delete Selected")
        delete_btn.clicked.connect(delete_selected)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dlg.accept)

        btn_row = QHBoxLayout()
        btn_row.addWidget(delete_btn)
        btn_row.addWidget(close_btn)
        layout.addLayout(btn_row)

        dlg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())