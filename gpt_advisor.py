# Handles all gpt calls and responses
import os
import openai
from dotenv import load_dotenv
from openai import AuthenticationError, RateLimitError, APIConnectionError, OpenAIError
import asyncio

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to call OpenAI API and get a response
def get_gpt_advice(prompt):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful financial advisor."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=min(512, 4096 - len(prompt.split())) * 2,  # Rough estimate of token count
            temperature=0.7,
        )
        return (response.choices[0].message.content.strip())
    except AuthenticationError:
        print("Error: Invalid API key. Please check your OpenAI API key in the .env file.")
        return "Authentication error: Invalid API key."
    except RateLimitError:
        print("Error: Rate limit exceeded. Please wait and try again later.")
        return "Rate limit error: Too many requests. Please try again later."
    except APIConnectionError:
        print("Error: Failed to connect to the OpenAI API. Please check your internet connection.")
        return "Connection error: Unable to connect to OpenAI servers."
    except OpenAIError as e:
        print(f"An OpenAI-specific error occurred: {e}")
        return f"OpenAI error: {e}"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred. Please try again later."

def analyze_budget(income, expenses):
    total_income = sum(item["amount"] for item in income)
    total_expenses = sum(item["amount"] for item in expenses)

    # Prepare the prompt for GPT
    prompt = f"""
    You are a professional financial advisor reviewing a user's budget.

    Here is the data:
    - Total Monthly Income: ${total_income:.2f}
    - Total Monthly Expenses: ${total_expenses:.2f}

    Please provide a structured analysis with the following format:
    1. 📊 Summary of the current financial state (e.g., surplus or deficit)
    2. 💡 Three actionable suggestions to improve budgeting or reduce expenses
    3. 📈 Optional tips on building long-term financial health

    Keep it concise and practical.
    """
    
    # Get advice from GPT
    advice = get_gpt_advice(prompt)
    
    if advice:
        return advice
    else:
        return "Could not retrieve advice from GPT."
    
def create_budget(income, expenses):
    total_income = sum(item["amount"] for item in income)
    total_expenses = sum(item["amount"] for item in expenses)

    # Prepare the prompt for GPT
    prompt = f"""
    You are a financial advisor. Based on the following financial snapshot, generate a detailed monthly budget.

    User Profile:
    - Total Monthly Income: ${total_income:.2f}
    - Total Monthly Expenses: ${abs(total_expenses):.2f}

    Required Output:
    - 📥 Recommended Savings Target (in $)
    - 🏠 Essentials (e.g., rent, utilities, groceries) — include breakdowns
    - 🍿 Discretionary Spending (e.g., entertainment, dining out) — include breakdowns
    - 📘 Recommendations for better financial health or habit changes

    Respond in clear, structured sections with labels like:
    [🏠 Essentials], [🍿 Discretionary], etc.
    """

    # Get the budget from GPT
    try:
        budget = get_gpt_advice(prompt)
        return budget
    except Exception as e:
        print(f"Error creating budget: {e}")
        return "Could not generate a budget at this time."
    
def categorize_transaction(description):
    prompt = f"""
    You are a financial transaction categorizer.

    Rules:
    - Pick the one best-matching category for the transaction below.
    - Respond with only one lowercase category from this list:
    ["food", "groceries", "gas", "utilities", "entertainment", "salary", "shopping", "travel", "fees", "health", "gifts", "transfer", "education", "family", "other"]

    Transaction Description:
    "{description}"

    Respond with only the category. No explanation. No punctuation. No full sentences.
    """
    result = get_gpt_advice(prompt).strip().lower()
    valid_categories = [
        "food", "groceries", "gas", "utilities", "entertainment", "salary",
        "shopping", "travel", "fees", "health", "gifts", "transfer", "education",
        "family", "other"
    ]
    return result if result in valid_categories else "other"

async def async_categorize_transaction(description):
    prompt = f"""
You are a financial transaction categorizer.

Rules:
- Pick one best matching category for the following transaction.
- Only respond with a one-word category like "food", "groceries", "gas", "utilities", "entertainment", "salary", "shopping", "travel", "fees", "health", or "other".
- No full sentences.

Transaction description:
"{description}"

Respond with only the one category word.
"""
    try:
        result = get_gpt_advice(prompt).strip().lower()
        # If GPT returns weird stuff, fallback
        return result        
    except Exception as e:
        print(f"Async categorize error: {e}")
        return "other"




