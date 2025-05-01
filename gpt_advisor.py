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
    You are a certified financial advisor evaluating a user's monthly budget.

    User's Financial Data:
    - Total Monthly Income: ${total_income:.2f}
    - Total Monthly Expenses: ${total_expenses:.2f}

    Instructions:
    1. Analyze whether the user has a surplus or deficit, and state how much.
    2. Suggest three clear, actionable strategies to reduce expenses or manage spending more effectively.
    3. Optionally provide high-level tips for building long-term financial health (e.g., emergency funds, debt payoff strategies).

    Format the response using section titles and bullet points where helpful. Use an informative yet friendly tone.
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
    You are a financial advisor helping a user structure a smart, sustainable monthly budget.

    User's Current Situation:
    - Total Monthly Income: ${total_income:.2f}
    - Total Monthly Expenses: ${abs(total_expenses):.2f}

    Please generate a recommended monthly budget with the following format:

    [📥 Recommended Savings Target]
    - Suggest a savings amount based on income, ideally 15–20%, and explain why.

    [🏠 Essentials]
    - Break down essential expenses (e.g., rent, utilities, transportation, groceries).
    - Provide realistic percentage allocations or dollar estimates.

    [🍿 Discretionary Spending]
    - Suggest discretionary categories (e.g., entertainment, dining out, subscriptions).
    - Offer strategies to limit or manage this area responsibly.

    [📘 Financial Recommendations]
    - Give two or three tailored tips to strengthen the user's overall financial habits.
    - Include suggestions like using budgeting apps, emergency funds, or automating savings.

    Respond clearly and concisely with bullet points under each section.
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
    You are a machine-learning-based financial transaction categorizer.

    Instructions:
    - Match the transaction description to the most relevant category.
    - Choose only one from this list (lowercase): 
    ["food", "groceries", "gas", "utilities", "entertainment", "salary", "shopping", "travel", "fees", "health", "gifts", "transfer", "education", "family", "other"]
    - Output ONLY the matching category with no punctuation, quotes, or explanation.

    Transaction description:
    "{description}"

    Respond with a single word from the list.
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
    You are a machine-learning-based financial transaction categorizer.

        Instructions:
        - Match the transaction description to the most relevant category.
        - Choose only one from this list (lowercase): 
        ["food", "groceries", "gas", "utilities", "entertainment", "salary", "shopping", "travel", "fees", "health", "gifts", "transfer", "education", "family", "other"]
        - Output ONLY the matching category with no punctuation, quotes, or explanation.

        Transaction description:
        "{description}"

        Respond with a single word from the list.
        """
    try:
        result = get_gpt_advice(prompt).strip().lower()
        # If GPT returns weird stuff, fallback
        return result        
    except Exception as e:
        print(f"Async categorize error: {e}")
        return "other"




