💰 Personal Expense Tracker - Web Application

A modern, interactive web application built with Streamlit to track personal expenses, manage budgets, and visualize financial habits.

This application allows users to log daily expenses, set monthly budgets for different categories, and view insightful dashboards and reports on their spending patterns. It's a simple yet powerful tool for personal finance management.

✨ Key Features

Interactive Dashboard: Quick overview of total spending, number of expenses, and average expense amount.

Expense Logging: Add new expenses with categories, amounts, and optional notes.

Budget Management: Set monthly spending limits per category and track your progress.

Proactive Alerts: Get warnings when close to a budget limit and alerts when exceeded.

Data Visualization:

Bar chart: Spending distribution by category.

Line chart: Cumulative spending trend over time.

Full History: Searchable and sortable table of all past expenses.

Persistent Storage: All data stored in a local SQLite database (expenses.db).

🛠️ Tech Stack

Language: Python

Framework: Streamlit

Data Manipulation: Pandas

Database: SQLite

🚀 Getting Started

Follow these instructions to set up and run the project locally.

✅ Prerequisites

Python 3.8 or higher

pip (Python package installer)

📥 Installation & Setup

Clone the repository:

git clone https://github.com/RakeshGanesh/expense-tracker-streamlit.git
cd expense-tracker-streamlit


Create and activate a virtual environment (recommended):

For Windows

python -m venv .venv
.\.venv\Scripts\activate


For macOS/Linux

python3 -m venv .venv
source .venv/bin/activate


Install the required dependencies:

pip install -r requirements.txt

▶️ Running the Application

Run the Streamlit app:

streamlit run app.py


Then open your browser. It should auto-open a new tab, or you can navigate to:
👉 http://localhost:8501

📂 Project Structure
expense-tracker-streamlit/
├── app.py              # Main Streamlit app
├── expenses.db         # SQLite database (auto-created)
├── requirements.txt    # Dependencies
└── README.md           # Documentation

📸 Screenshots <img width="1916" height="988" alt="image" src="https://github.com/user-attachments/assets/e8989d68-45e1-447f-ae70-4fb24dab7d46" />



🤝 Contributing

Contributions are welcome! Please fork this repo and submit a pull request.

📜 License

This project is licensed under the MIT License.
