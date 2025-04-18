# from tracker import BudgetTracker
# from gpt_advisor import analyze_budget
# import datetime
# import os

# # Create a new instance of the BudgetTracker class
# tracker = BudgetTracker()
# # Call load_data() on startup to load any existing data
# tracker.load_data()
# # Run a main() in a while loop that shows menu options and accepts user input
# def main():
#     while True:
#         print("""\tWelcome to the Budget Tracker!
#         1. Add Income   2. Add Expense
#         3. View Income  4. View Expenses
#         5. View Balance 6. Save Data
#         7. Load Data    8. Forecast Next Month's Balance
#         9. Exit         10. Get GPT Budgeting Advice""")

#         choice = input("Enter your choice: ").strip()

#         if choice == "1":
#             clear_screen()
#             try:
#                 amount = float(input("Enter income amount: "))
#             except ValueError:
#                 print("Invalid amount. Please enter a number.")
#                 continue
#             try:
#                 source = input("Enter income source: ").strip()
#                 if not source:
#                     print("Income source cannot be empty.")
#                     continue
#             except ValueError:
#                 print("Invalid source. Please enter a valid source.")
#                 continue
#             try:
#                 date_input = input("Enter date (YYYY-MM-DD) or leave blank for today: ").strip()
#                 date = datetime.datetime.strptime(date_input, "%Y-%m-%d").date() if date_input else datetime.date.today()
#             except ValueError:
#                 print("Invalid date. Please enter a valid date.")
#                 continue
#             tracker.add_income(amount, date, source)
#         elif choice == "2":
#             clear_screen()
#             try:
#                 amount = float(input("Enter expense amount: "))
#             except ValueError:
#                 print("Invalid amount. Please enter a number.")
#                 continue
#             try:
#                 category = input("Enter expense category: ").strip()
#                 if not category:
#                     print("Expense category cannot be empty.")
#                     continue
#             except ValueError:
#                 print("Invalid category. Please enter a valid category.")
#                 continue
#             try:
#                 date_input = input("Enter date (YYYY-MM-DD) or leave blank for today: ").strip()
#                 date = datetime.datetime.strptime(date_input, "%Y-%m-%d").date() if date_input else datetime.date.today()
#             except ValueError:
#                 print("Invalid date. Please enter a valid date.")
#                 continue
#             tracker.add_expense(amount, date, category)
#         elif choice == "3":
#             clear_screen()
#             tracker.view_income()
#         elif choice == "4":
#             clear_screen()
#             tracker.view_expense()
#         elif choice == "5":
#             clear_screen()
#             tracker.view_balance()
#         elif choice == "6":
#             clear_screen()
#             tracker.save_data()
#         elif choice == "7":
#             clear_screen()
#             tracker.load_data()
#         elif choice == "8":
#             clear_screen()
#             tracker.forecast_next_month_balance()
#         elif choice == "9":
#             clear_screen()
#             print("Goodbye!")
#             break
#         elif choice == "10":
#             analyze_budget(tracker.income, tracker.expenses)
#         else:
#             print("Invalid choice, please try again.")

# def clear_screen():
#     os.system('cls' if os.name == 'nt' else 'clear')

# if __name__ == "__main__":
#     main()
