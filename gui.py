import customtkinter as ctk
from tracker import BudgetTracker
from gpt_advisor import analyze_budget, create_budget
from PIL import Image
import os
import _tkinter

# Start with a simple GUI using tkinter
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Penny Pilot")
        self.geometry("500x600")
        self.resizable(False, False)
        
        self.tracker = BudgetTracker(self)
        self.tracker.load_data()

        # Create a label
        self.label = ctk.CTkLabel(self, text="Piloting to a better budget...", font=ctk.CTkFont(size=18, weight="bold"))
        self.label.pack(pady=20)

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=20)

        # Frame to hold both income and expense views
        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.pack(pady=10, fill="both", expand=True)

        # Income column
        self.income_label = ctk.CTkLabel(self.log_frame, text="Income:")
        self.income_label.grid(row=0, column=0, padx=10, sticky="w")

        self.income_textbox = ctk.CTkTextbox(self.log_frame, height=120, width=220)
        self.income_textbox.grid(row=1, column=0, padx=10, pady=5)

        # Expense column
        self.expense_label = ctk.CTkLabel(self.log_frame, text="Expenses:")
        self.expense_label.grid(row=0, column=1, padx=10, sticky="w")

        self.expense_textbox = ctk.CTkTextbox(self.log_frame, height=120, width=220)
        self.expense_textbox.grid(row=1, column=1, padx=10, pady=5)


        # Add Income button
        self.income_button = ctk.CTkButton(self.button_frame, text="Add Income", command=lambda: self.open_income_window())
        self.income_button.grid(row=0, column=0, padx=10, pady=10)
        # Add Expense button
        self.expense_button = ctk.CTkButton(self.button_frame, text="Add Expense", command=lambda: self.open_expense_window())
        self.expense_button.grid(row=0, column=1, padx=10, pady=10)
        # View summary button
        self.summary_button = ctk.CTkButton(self.button_frame, text="View Summary", command=lambda: self.open_summary_window())
        self.summary_button.grid(row=1, column=0, padx=10, pady=10)
        # Save Data button
        self.save_button = ctk.CTkButton(self.button_frame, text="Save Data", command=lambda: self.save_data())
        self.save_button.grid(row=1, column=1, padx=10, pady=10)
        # Load Data button
        self.load_button = ctk.CTkButton(self.button_frame, text="Load Data", command=lambda: self.open_load_data_window())
        self.load_button.grid(row=2, column=0, padx=10, pady=10)
        # Get Forecast button
        self.forecast_button = ctk.CTkButton(self.button_frame, text="Forecast", command=lambda: self.open_forecast_window())
        self.forecast_button.grid(row=2, column=1, padx=10, pady=10)
        # Get GPT Advice button
        self.gpt_button = ctk.CTkButton(self.button_frame, text="Get GPT Advice", command=lambda: self.open_gpt_window())
        self.gpt_button.grid(row=3, column=0, padx=10, pady=10)
        # Clear data button that lets the user choose, clear income, expenses or both
        self.clear_button = ctk.CTkButton(self.button_frame, text="Clear Data", command=lambda: self.open_clear_data_window())
        self.clear_button.grid(row=3, column=1, padx=10, pady=10)
        # Add Generate Budget button
        self.budget_button = ctk.CTkButton(self.button_frame, text="Generate Budget", command=lambda: self.open_budget_window())
        self.budget_button.grid(row=4, column=0, padx=10, pady=10)
        # Exit button
        self.exit_button = ctk.CTkButton(self.button_frame, text="Exit", command=self.destroy)
        self.exit_button.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

        # Call update_logs to display initial data
        self.update_logs()


    # Create income window
    def open_income_window(self):
        income_window = ctk.CTkToplevel(self)
        income_window.title("Add Income")
        income_window.geometry("300x250")
        income_window.attributes("-topmost", True)
        income_window.lift()
        income_window.focus_force()

        # Income entry fields
        amount_entry = ctk.CTkEntry(income_window, placeholder_text="Income Amount")
        amount_entry.pack(pady=5)

        source_entry = ctk.CTkEntry(income_window, placeholder_text="Source (e.g., Paycheck)")
        source_entry.pack(pady=5)

        date_entry = ctk.CTkEntry(income_window, placeholder_text="Date (YYYY-MM-DD, leave blank for today)")
        date_entry.pack(pady=5)

        def submit_income():
            amount = amount_entry.get()
            source = source_entry.get()
            date = date_entry.get()
            try:
                self.tracker.add_income(amount, source, date)  # Pass the date parameter
                self.label.configure(text="Income added!")
                self.update_logs()
                income_window.destroy()
            except Exception as e:
                self.label.configure(text=f"Error: {e}")

        submit_btn = ctk.CTkButton(income_window, text="Submit", command=submit_income)
        submit_btn.pack(pady=10)

    # Create expense window
    def open_expense_window(self):
        expense_window = ctk.CTkToplevel(self)
        expense_window.title("Add Expense")
        expense_window.geometry("300x250")
        expense_window.attributes("-topmost", True)
        expense_window.lift()
        expense_window.focus_force()

        # Expense entry fields
        amount_entry = ctk.CTkEntry(expense_window, placeholder_text="Expense Amount")
        amount_entry.pack(pady=5)

        category_entry = ctk.CTkEntry(expense_window, placeholder_text="Category (e.g., Food)")
        category_entry.pack(pady=5)

        date_entry = ctk.CTkEntry(expense_window, placeholder_text="Date (YYYY-MM-DD, leave blank for today)")
        date_entry.pack(pady=5)

        def submit_expense():
            amount = amount_entry.get()
            category = category_entry.get()
            date = date_entry.get()
            try:
                self.tracker.add_expense(amount, category, date)  # Pass the date parameter
                self.label.configure(text="Expense added!")
                self.update_logs()
                expense_window.destroy()
            except Exception as e:
                self.label.configure(text=f"Error: {e}")

        submit_btn = ctk.CTkButton(expense_window, text="Submit", command=submit_expense)
        submit_btn.pack(pady=10)

    # Create summary window
    def open_summary_window(self):
        summary_window = ctk.CTkToplevel(self)
        summary_window.title("Budget Summary")
        summary_window.geometry("300x250")
        summary_window.attributes("-topmost", True)
        summary_window.lift()
        summary_window.focus_force()

        #Summary display
        balance = self.tracker.view_balance() or 0.0
        income = self.tracker.view_income() or 0.0
        expenses = self.tracker.view_expense() or 0.0

        summary_text = f"Balance: ${balance:.2f}\nIncome: ${income:.2f}\nExpenses: ${expenses:.2f}"
        summary_label = ctk.CTkLabel(summary_window, text=summary_text)
        summary_label.pack(pady=20)

    def open_load_data_window(self):
        load_window = ctk.CTkToplevel(self)
        load_window.title("Load Data")
        load_window.geometry("400x150")
        load_window.attributes("-topmost", True)
        load_window.lift()

        # Disable the close button
        load_window.protocol("WM_DELETE_WINDOW", lambda: None)

        def load_main_file():
            try:
                print("Loading main file...")
                self.tracker.load_data("budget_data.json")
                self.update_logs()
                try:
                    if load_window.winfo_exists():  # Check if the window still exists
                        self.after(100, load_window.destroy)  # Use after to ensure the window is destroyed after the current event loop
                except Exception as e:
                    print(f"Error destroying load_window: {e}")
            except _tkinter.TclError as e:
                print(f"TclError occurred: {e}")

        def load_backup_file():
            try:
                print("Loading backup file...")
                self.tracker.load_data("budget_data_backup.json")
                self.update_logs()
                try:
                    if load_window.winfo_exists():  # Check if the window still exists
                        self.after(100, load_window.destroy)  # Use after to ensure the window is destroyed after the current event loop
                except Exception as e:
                    print(f"Error destroying load_window: {e}")
            except _tkinter.TclError as e:
                print(f"TclError occurred: {e}")

        main_file_button = ctk.CTkButton(load_window, text="Load Main File", command=load_main_file)
        main_file_button.pack(side="left", padx=20, pady=10)

        backup_file_button = ctk.CTkButton(load_window, text="Load Backup File", command=load_backup_file)
        backup_file_button.pack(side="right", padx=20, pady=10)

    def open_forecast_window(self):
        forecast_window = ctk.CTkToplevel(self)
        forecast_window.title("Forecast")
        forecast_window.geometry("350x250")
        forecast_window.attributes("-topmost", True)
        forecast_window.lift()
        forecast_window.focus_force()

        #Forecast display
        forecast = self.tracker.forecast_next_month_balance() or 0.0
        balance = self.tracker.view_balance() or 0.0

        averages = self.tracker.get_monthly_averages()
        if averages:
            monthly_income_averages, monthly_expenses_averages = averages
            average_income = sum(monthly_income_averages.values()) / len(monthly_income_averages) if monthly_income_averages else 0.0
            average_expenses = sum(monthly_expenses_averages.values()) / len(monthly_expenses_averages) if monthly_expenses_averages else 0.0
        else:
            average_income = 0.0
            average_expenses = 0.0
        forecast_text = (
            f"Forecast Summary:\n\n"
            f"Current balance: ${balance:.2f}\n"
            f"Average monthly income: ${average_income:.2f}\n"
            f"Average monthly expenses: ${average_expenses:.2f}\n"
            f"Forecasted balance next month: ${forecast:.2f}"
        )

        # Display the forecast text in a label
        forecast_label = ctk.CTkLabel(forecast_window, text=forecast_text)
        forecast_label.pack(pady=20)

    def open_gpt_window(self):
        try:
            advice = analyze_budget(self.tracker.income, self.tracker.expenses)

            advice_window = ctk.CTkToplevel(self)
            advice_window.title("GPT Financial Advice")
            advice_window.geometry("400x300")
            advice_window.attributes("-topmost", True)
            advice_window.lift()
            advice_window.focus_force()

            advice_label = ctk.CTkLabel(advice_window, text=advice, wraplength=360, justify="left")
            advice_label.pack(pady=20)
        except Exception as e:
            self.label.configure(text=f"GPT Error: {e}")

    # Clear data window that lets the user choose, clear income, expenses or both
    def open_clear_data_window(self):
        clear_window = ctk.CTkToplevel(self)
        clear_window.title("Clear Data")
        clear_window.geometry("250x180")
        clear_window.attributes("-topmost", True)
        clear_window.lift()
        clear_window.focus_force()

        # disable the close button 
        clear_window.protocol("WM_DELETE_WINDOW", lambda: None)

        def clear_income():
            self.tracker.income.clear()
            self.label.configure(text="Income cleared!")
            self.update_logs()
            clear_window.destroy()

        def clear_expenses():
            self.tracker.expenses.clear()
            self.label.configure(text="Expenses cleared!")
            self.update_logs()
            clear_window.destroy()

        def clear_all():
            self.tracker.income.clear()
            self.tracker.expenses.clear()
            self.label.configure(text="All data cleared!")
            self.update_logs()
            clear_window.destroy()

        ctk.CTkButton(clear_window, text="Clear Income", command=clear_income).pack(pady=5)
        ctk.CTkButton(clear_window, text="Clear Expenses", command=clear_expenses).pack(pady=5)
        ctk.CTkButton(clear_window, text="Clear All", command=clear_all).pack(pady=5)
    
    def open_budget_window(self):
        try:
                # Generate the budget using OpenAI
            budget = create_budget(self.tracker.income, self.tracker.expenses)

            # Create a new window to display the budget
            budget_window = ctk.CTkToplevel(self)
            budget_window.title("Generated Budget")
            budget_window.geometry("400x400")
            budget_window.attributes("-topmost", True)
            budget_window.lift()
            budget_window.focus_force()

            # disable the close button 
            budget_window.protocol("WM_DELETE_WINDOW", lambda: None)   

            # Display the budget in a label
            budget_label = ctk.CTkLabel(budget_window, text=budget, wraplength=360, justify="left")
            budget_label.pack(pady=20)
        except Exception as e:
            self.label.configure(text=f"Error generating budget: {e}")

    def update_logs(self):
        # Clear both textboxes before updating
        self.income_textbox.delete("0.0", "end")
        self.expense_textbox.delete("0.0", "end")

        # Update income logs
        if not self.tracker.income:
            self.income_textbox.insert("end", "No Income loaded.\n")
        else:
            for entry in self.tracker.income:
                line = f"{entry['date']}: ${entry['amount']} ({entry['source']})\n"
                self.income_textbox.insert("end", line)

        # Update expense logs
        if not self.tracker.expenses:
            self.expense_textbox.insert("end", "No Expenses loaded.\n")
        else:
            for entry in self.tracker.expenses:
                line = f"{entry['date']}: ${entry['amount']} ({entry['category']})\n"
                self.expense_textbox.insert("end", line)

    def show_notification(self, message):
        notification = ctk.CTkToplevel(self)
        notification.title("Notification")
        notification.geometry("250x100")
        notification.attributes("-topmost", True)
        notification.lift()
        notification.focus_force()

        # Disable the close button
        notification.protocol("WM_DELETE_WINDOW", lambda: None)

        label = ctk.CTkLabel(notification, text=message, wraplength=200, justify="center")
        label.pack(pady=10)

        def close_window():
            try:
                if notification.winfo_exists():
                    notification.destroy()
            except _tkinter.TclError:
                pass  # Ignore if the window is already destroyed

        ok_button = ctk.CTkButton(notification, text="OK", command=close_window)
        ok_button.pack(pady=10)

    def ask_backup_confirmation(self, callback):
        # Create a pop-up window
        confirmation_window = ctk.CTkToplevel(self)
        confirmation_window.title("Create Backup?")
        confirmation_window.geometry("400x150")
        confirmation_window.attributes("-topmost", True)
        confirmation_window.lift()
        confirmation_window.focus_force()

        # Disable the close button
        confirmation_window.protocol("WM_DELETE_WINDOW", lambda: None)

        # Add a label to ask the question
        label = ctk.CTkLabel(confirmation_window, text="Do you want to create a backup of the current data?")
        label.pack(pady=20)

        # Define button actions
        def on_yes():
            try:
                callback(True)  # Proceed with backup
                confirmation_window.destroy()
            except _tkinter.TclError:
                pass  # Ignore if the window is already destroyed

        def on_no():
            try:
                callback(False)  # Skip backup
                confirmation_window.destroy()
            except _tkinter.TclError:
                pass  # Ignore if the window is already destroyed

        # Add Yes and No buttons
        yes_button = ctk.CTkButton(confirmation_window, text="Yes", command=on_yes)
        yes_button.pack(side="left", padx=20, pady=10)

        no_button = ctk.CTkButton(confirmation_window, text="No", command=on_no)
        no_button.pack(side="right", padx=20, pady=10)

class Splashscreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Penny Pilot")
        self.geometry("300x300")
        self.resizable(False, False)

        # Load logo image
        logo_path = os.path.join("assets", "PenPil.png")
        self.logo_img = ctk.CTkImage(Image.open(logo_path), size=(100, 100))
        # Display image
        logo_label = ctk.CTkLabel(self, image=self.logo_img, text="")
        logo_label.pack(pady=20)

        # Create a label
        self.label = ctk.CTkLabel(self, text="Welcome to Penny Pilot!\n Loading...", font=ctk.CTkFont(size=18, weight="bold"))
        self.label.pack(pady=20)

if __name__ == "__main__":
    splash = Splashscreen()

    def launch_main_app():
        splash.destroy()
        app = App()
        app.mainloop()
    
    splash.after(2000, launch_main_app)  # Show splash screen for 2 seconds
    splash.mainloop()