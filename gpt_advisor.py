# Handles all gpt calls and responses
import os
import openai
from dotenv import load_dotenv
from openai import AuthenticationError, RateLimitError, APIConnectionError, OpenAIError

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
            max_tokens=150,
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
    You are a financial advisor. Based on the following budget data, provide advice on how to manage finances better.
    
    Income: ${total_income:.2f}
    Expenses: ${total_expenses:.2f}
    
    Please provide:
    1. A brief summary of the current financial state
    2. Three suggestions to improve budgeting or reduce expenses
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
    You are a financial advisor. Based on the following budget data, create a detailed monthly budget.
    
    Total Income: ${total_income:.2f}
    Total Expenses: ${total_expenses:.2f}
    
    Please include:
    1. Suggested savings amount.
    2. Allocations for essential expenses (e.g., rent, utilities, groceries).
    3. Allocations for discretionary spending (e.g., entertainment, dining out).
    4. Any recommendations for improving financial health.
    """

    # Get the budget from GPT
    try:
        budget = get_gpt_advice(prompt)
        return budget
    except Exception as e:
        print(f"Error creating budget: {e}")
        return "Could not generate a budget at this time."
    
def classify_transaction(description, amount):
    prompt = (
        f"Classify the following transactions as either 'income' or 'expense'. "
        f"Respond with only one word: income or expense.\n\n"
        f"Description: \"{description}\"\nAmount: {amount}"
    )
    return get_gpt_advice(prompt).lower()



