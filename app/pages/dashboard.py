import streamlit as st
import pandas as pd
from datetime import datetime
from app.services.transaction_service import (
    calculate_net_savings,
    get_transactions
)
from app.components.charts import (
    monthly_trend_chart,
    category_bar_chart,
    visualize_spending
)


def show():
    st.title("📊 Dashboard")

    if "user_id" not in st.session_state:
        st.warning("Please login first.")
        st.stop()

    user_id = st.session_state["user_id"]

    # --- KPIs ---
    income, expense, net = calculate_net_savings(user_id)

    savings_rate = (net / income * 100) if income > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Income", f"${income:.2f}")
    col2.metric("Total Expense", f"${expense:.2f}")
    col3.metric("Net Savings", f"${net:.2f}")
    col4.metric("Savings Rate", f"{savings_rate:.1f}%")

    st.divider()

    # --- Fetch Data ---
    transactions_df = get_transactions(user_id)

    if transactions_df.empty:
        st.info("No transactions yet.")
        return

    transactions_df["date"] = pd.to_datetime(transactions_df["date"])

    # --- Monthly Trend ---
    st.subheader("📈 Monthly Trend")
    monthly_trend_chart(transactions_df)

    st.divider()

    #visualize spendings
    visualize_spending()

    # --- Bottom Section ---
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("📊 Category Breakdown")
        category_bar_chart(transactions_df)

    with col_right:
        st.subheader("🧾 Recent Transactions")
        recent = transactions_df.sort_values("date", ascending=False).head(5)
        st.dataframe(recent, use_container_width=True)