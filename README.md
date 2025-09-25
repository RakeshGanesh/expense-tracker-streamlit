💰 Personal Expense Tracker - Web Application
A modern, interactive web application built with Streamlit to track personal expenses, manage budgets, and visualize financial habits.

This application allows users to log daily expenses, set monthly budgets for different categories, and view insightful dashboards and reports on their spending patterns. It's a simple yet powerful tool for personal finance management.

✨ Key Features
Interactive Dashboard: Get a quick overview of your total spending, number of expenses, and average expense amount.

Expense Logging: Easily add new expenses with categories, amounts, and optional notes.

Budget Management: Set monthly spending limits for any category and track your progress.

Proactive Alerts: Receive automatic warnings when you're close to a budget limit and alerts when you've exceeded one.

Data Visualization:

An interactive bar chart shows spending distribution by category.

A line chart visualizes your cumulative spending trend over time.

Full History: A searchable and sortable table displays all your past expenses.

Persistent Storage: All data is securely stored in a local SQLite database (expenses.db).

🛠️ Tech Stack
Language: Python

Web Framework: Streamlit

Data Manipulation: Pandas

Database: SQLite

🚀 Getting Started
Follow these instructions to set up and run the project on your local machine.

Prerequisites
Python 3.8 or higher

pip (Python package installer)

Installation & Setup
Clone the repository:

git clone [https://github.com/RakeshGanesh/expense-tracker-streamlit.git](https://github.com/RakeshGanesh/expense-tracker-streamlit.git)
cd expense-tracker-streamlit


Create and activate a virtual environment (recommended):

# For Windows
python -m venv .venv
.\.venv\Scripts\activate

# For macOS/Linux
python3 -m venv .venv
source .venv/bin/activate


Install the required dependencies:

pip install -r requirements.txt


Running the Application
Run the Streamlit app from your terminal:

streamlit run app.py


Open your web browser: The application should automatically open in a new tab. If not, navigate to the local URL shown in your terminal (usually http://localhost:8501).