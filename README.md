# Penny Pilot

Penny Pilot is a personal finance management application designed to help you track your income, expenses, and budget. It provides a user-friendly GUI built with `customtkinter` and integrates OpenAI's GPT to analyze your budget and generate financial advice or a detailed budget plan. Additionally, Penny Pilot includes a Flask-based API to expose its features for programmatic access.

## Features
- **Track Income and Expenses**: Add, view, and manage your income and expenses.
- **Budget Analysis**: Get financial advice based on your income and expenses using OpenAI's GPT.
- **Budget Generation**: Generate a detailed budget plan with savings, essential expenses, and discretionary spending recommendations.
- **Forecasting**: Predict your next month's balance based on historical data.
- **Data Management**: Save and load your financial data to/from a file.
- **Clear Data**: Clear income, expenses, or all data with a single click.
- **API Integration**: Expose features via a RESTful API using Flask (Optional).

## Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API Key (for GPT integration)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/PennyPilot.git
   cd PennyPilot
2. python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. pip install -r requirements.txt
4. OPENAI_API_KEY=your_openai_api_key
5. Gui mode - python [gui.py](http://_vscodecontentref_/1)
Api mode - python [api.py](http://_vscodecontentref_/2)
Flask API Server - python [api.py](http://_vscodecontentref_/3)
6. example of add income
    curl -X POST http://127.0.0.1:5000/add_income \
    -H "Content-Type: application/json" \
    -d '{"amount": 5000, "source": "Salary", "date": "2025-04-18"}'

File Structure

PennyPilot/
├── assets/               # Contains images and other assets
├── [gui.py](http://_vscodecontentref_/4)                # Main GUI application
├── [tracker.py](http://_vscodecontentref_/5)            # Budget tracking logic
├── [gpt_advisor.py](http://_vscodecontentref_/6)        # GPT integration for advice and budget generation
├── [api.py](http://_vscodecontentref_/7)                # Flask API for exposing features
├── [cli_mode.py](http://_vscodecontentref_/8)           # CLI mode (optional)
├── [requirements.txt](http://_vscodecontentref_/9)      # Python dependencies
├── .env                  # Environment variables (e.g., OpenAI API key)
├── .gitignore            # Git ignore file
└── [README.md](http://_vscodecontentref_/10)             # Project documentation
