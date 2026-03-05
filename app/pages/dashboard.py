import streamlit as st
import pandas as pd
import plotly.express as px

from app.services.transaction_service import get_transactions


def show_dashboard():

    st.title("Financial Dashboard")

    # Get user id from session
    user_id = st.session_state.get("user_id")

    if not user_id:
        st.warning("Please login first")
        return

    # Fetch transactions
    df = get_transactions(user_id)

    if df.empty:
        st.warning("No transactions found.")
        return

    df["date"] = pd.to_datetime(df["date"])

    # -------- Financial Calculations --------
    income = df[df["type"] == "Income"]["amount"].sum()
    expense = df[df["type"] == "Expense"]["amount"].sum()

    balance = income - expense

    savings_rate = (balance / income * 100) if income > 0 else 0

    # -------- KPI CARDS --------
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Balance", f"${balance:,.2f}")
    col2.metric("Total Income", f"${income:,.2f}")
    col3.metric("Total Expense", f"${expense:,.2f}")
    col4.metric("Savings Rate", f"{savings_rate:.1f}%")

    st.divider()

    # -------- Expense by Category --------
    expense_df = df[df["type"] == "Expense"]

    if not expense_df.empty:

        category_chart = px.pie(
            expense_df,
            values="amount",
            names="category",
            title="Expenses by Category"
        )

        st.plotly_chart(category_chart, use_container_width=True)

    # -------- Income vs Expense --------
    summary = pd.DataFrame({
        "Type": ["Income", "Expense"],
        "Amount": [income, expense]
    })

    bar_chart = px.bar(
        summary,
        x="Type",
        y="Amount",
        color="Type",
        title="Income vs Expense"
    )

    st.plotly_chart(bar_chart, use_container_width=True)

    # -------- Monthly Trend --------
    df["month"] = df["date"].dt.to_period("M").astype(str)

    monthly = df.groupby(["month", "type"])["amount"].sum().reset_index()

    trend_chart = px.line(
        monthly,
        x="month",
        y="amount",
        color="type",
        markers=True,
        title="Monthly Income vs Expense Trend"
    )

    st.plotly_chart(trend_chart, use_container_width=True)