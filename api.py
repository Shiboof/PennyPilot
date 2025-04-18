from flask import Flask, request, jsonify
from tracker import BudgetTracker
from gpt_advisor import analyze_budget, create_budget

app = Flask(__name__)

# Create a global instance of BudgetTracker
tracker = BudgetTracker(None)  # Pass `None` since this is not connected to the GUI
tracker.load_data()

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Penny Pilot API!"})

# Add income
@app.route("/add_income", methods=["POST"])
def add_income():
    data = request.json
    amount = data.get("amount")
    source = data.get("source")
    date = data.get("date", None)  # Optional date
    if not amount or not source:
        return jsonify({"error": "Amount and source are required"}), 400
    tracker.add_income(amount, source, date)
    return jsonify({"message": "Income added successfully!"})

# Add expense
@app.route("/add_expense", methods=["POST"])
def add_expense():
    data = request.json
    amount = data.get("amount")
    category = data.get("category")
    date = data.get("date", None)  # Optional date
    if not amount or not category:
        return jsonify({"error": "Amount and category are required"}), 400
    tracker.add_expense(amount, category, date)
    return jsonify({"message": "Expense added successfully!"})

# View income
@app.route("/view_income", methods=["GET"])
def view_income():
    return jsonify({"income": tracker.income})

# View expenses
@app.route("/view_expenses", methods=["GET"])
def view_expenses():
    return jsonify({"expenses": tracker.expenses})

# View balance
@app.route("/view_balance", methods=["GET"])
def view_balance():
    balance = tracker.view_balance()
    return jsonify({"balance": balance})

# Generate budget
@app.route("/generate_budget", methods=["GET"])
def generate_budget():
    budget = create_budget(tracker.income, tracker.expenses)
    return jsonify({"budget": budget})

# Analyze budget
@app.route("/analyze_budget", methods=["GET"])
def analyze_budget_api():
    advice = analyze_budget(tracker.income, tracker.expenses)
    return jsonify({"advice": advice})

# Save data
@app.route("/save_data", methods=["POST"])
def save_data():
    tracker.save_data()
    return jsonify({"message": "Data saved successfully!"})

# Load data
@app.route("/load_data", methods=["POST"])
def load_data():
    tracker.load_data()
    return jsonify({"message": "Data loaded successfully!"})

if __name__ == "__main__":
    app.run(debug=True)