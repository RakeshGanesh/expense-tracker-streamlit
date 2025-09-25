import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import calendar

# --- Database Setup (Copied from your original script) ---
DB_FILE = "expenses.db"

def _get_db_connection():
    """Helper function to get a database connection."""
    return sqlite3.connect(DB_FILE)

def setup_database():
    """Initializes the SQLite database and creates tables if they don't exist."""
    conn = _get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            note TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT UNIQUE NOT NULL,
            limit_amount REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def check_budget_alert(category):
    """Checks budget status for a category and returns an alert message if needed."""
    conn = _get_db_connection()
    cursor = conn.cursor()

    # Get the budget limit for the given category
    cursor.execute("SELECT limit_amount FROM budgets WHERE category = ?", (category,))
    result = cursor.fetchone()

    # If no budget is set for this category, do nothing
    if not result:
        conn.close()
        return None

    limit = result[0]

    # Calculate total spending for this category in the current month
    current_month = datetime.now().strftime("%Y-%m")
    cursor.execute(
        "SELECT SUM(amount) FROM expenses WHERE category = ? AND strftime('%Y-%m', date) = ?",
        (category, current_month)
    )
    total_spent_result = cursor.fetchone()
    total_spent = total_spent_result[0] if total_spent_result[0] is not None else 0
    
    conn.close()

    # Check for alert conditions
    if total_spent > limit:
        overage = total_spent - limit
        return ("error", f"🚨 BUDGET ALERT: You have exceeded your budget for '{category}' by ₹{overage:,.2f} this month. (Spent: ₹{total_spent:,.2f} of ₹{limit:,.2f})")
    elif total_spent >= limit * 0.9:
        remaining = limit - total_spent
        return ("warning", f"⚠️ BUDGET WARNING: You are close to your budget for '{category}'. Only ₹{remaining:,.2f} remaining. (Spent: ₹{total_spent:,.2f} of ₹{limit:,.2f})")
    
    return None

# --- Page Configuration ---
st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# --- Main App ---
st.title("💰 Personal Expense Tracker")
st.markdown("Track your spending, manage budgets, and visualize your financial habits.")

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Add Expense", "View All Expenses", "Manage Budgets"])

# Initialize database on first run
setup_database()

# --- Page: Dashboard ---
if page == "Dashboard":
    st.header("Financial Dashboard")

    conn = _get_db_connection()
    df = pd.read_sql_query("SELECT date, category, amount FROM expenses", conn)
    conn.close()

    if df.empty:
        st.info("No expenses recorded yet. Add an expense to see your dashboard.")
    else:
        df['date'] = pd.to_datetime(df['date'])
        
        # --- Metrics ---
        total_spent = df['amount'].sum()
        expense_count = len(df)
        avg_expense = df['amount'].mean()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Spent", f"₹{total_spent:,.2f}")
        col2.metric("Number of Expenses", f"{expense_count}")
        col3.metric("Average Expense", f"₹{avg_expense:,.2f}")

        st.markdown("---")
        
        # --- Charts ---
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Expenses by Category")
            category_summary = df.groupby('category')['amount'].sum().sort_values(ascending=False)
            st.bar_chart(category_summary)

        with col2:
            st.subheader("Spending Over Time")
            df = df.sort_values('date')
            df['cumulative_amount'] = df['amount'].cumsum()
            time_summary = df.set_index('date')['amount']
            st.line_chart(time_summary)

# --- Page: Add Expense ---
elif page == "Add Expense":
    st.header("Add a New Expense")
    
    with st.form("expense_form", clear_on_submit=True):
        category = st.text_input("Category", placeholder="e.g., Food, Travel, Shopping")
        amount = st.number_input("Amount", min_value=0.01, format="%.2f")
        note = st.text_area("Note (Optional)")
        
        submitted = st.form_submit_button("Add Expense")
        if submitted:
            if not category or amount <= 0:
                st.error("Please fill in both Category and a valid Amount.")
            else:
                clean_category = category.strip().capitalize()
                date = datetime.now().strftime("%Y-%m-%d")
                conn = _get_db_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO expenses (date, category, amount, note) VALUES (?, ?, ?, ?)",
                               (date, clean_category, amount, note))
                conn.commit()
                conn.close()
                st.success(f"✅ Added Expense: {clean_category} - ₹{amount:.2f}")

                # Check and display budget alert
                alert = check_budget_alert(clean_category)
                if alert:
                    alert_type, alert_message = alert
                    if alert_type == "error":
                        st.error(alert_message)
                    else:
                        st.warning(alert_message)

# --- Page: View All Expenses ---
elif page == "View All Expenses":
    st.header("All Recorded Expenses")
    
    conn = _get_db_connection()
    df = pd.read_sql_query("SELECT date, category, amount, note FROM expenses ORDER BY date DESC", conn)
    conn.close()
    
    if df.empty:
        st.info("No expenses recorded yet.")
    else:
        df.index = range(1, len(df) + 1)
        st.dataframe(df, use_container_width=True)

# --- Page: Manage Budgets ---
elif page == "Manage Budgets":
    st.header("Manage Your Budgets")

    # --- Set a new budget ---
    with st.form("budget_form", clear_on_submit=True):
        st.subheader("Set or Update a Budget")
        category = st.text_input("Category")
        limit = st.number_input("Budget Limit", min_value=0.01, format="%.2f")
        submitted = st.form_submit_button("Set Budget")

        if submitted:
            if not category or limit <= 0:
                st.error("Please provide a category and a valid limit.")
            else:
                conn = _get_db_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT OR REPLACE INTO budgets (category, limit_amount) VALUES (?, ?)", 
                               (category.strip().capitalize(), limit))
                conn.commit()
                conn.close()
                st.success(f"Budget for '{category}' set to ₹{limit:.2f}.")
    
    st.markdown("---")

    # --- View current budgets ---
    st.subheader("Current Budget Status")
    conn = _get_db_connection()
    query = """
        SELECT
            b.category,
            b.limit_amount,
            COALESCE(SUM(e.amount), 0) as spent_this_month
        FROM budgets b
        LEFT JOIN expenses e ON b.category = e.category AND strftime('%Y-%m', e.date) = strftime('%Y-%m', 'now', 'localtime')
        GROUP BY b.category
        ORDER BY b.category
    """
    df_budgets = pd.read_sql_query(query, conn)
    conn.close()

    if df_budgets.empty:
        st.info("No budgets set yet.")
    else:
        df_budgets['remaining'] = df_budgets['limit_amount'] - df_budgets['spent_this_month']
        df_budgets['progress'] = (df_budgets['spent_this_month'] / df_budgets['limit_amount'])
        
        for index, row in df_budgets.iterrows():
            st.write(f"**{row['category']}**")
            # Ensure progress is capped at 1.0 for the progress bar
            progress_val = min(row['progress'], 1.0)
            st.progress(progress_val)
            
            status_color = "green" if row['remaining'] >= 0 else "red"
            st.markdown(f"Spent ₹{row['spent_this_month']:,.2f} of ₹{row['limit_amount']:,.2f}. <span style='color:{status_color};'>Remaining: ₹{row['remaining']:,.2f}</span>", unsafe_allow_html=True)

