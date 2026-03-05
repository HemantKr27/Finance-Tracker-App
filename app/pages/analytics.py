import streamlit as st

from app.components.charts import visualize_spending
from app.services.transaction_service import (
    calculate_net_savings,
    get_transactions
)


def show():

    st.subheader("Analytics")

    if "user_id" not in st.session_state:
        st.warning("Please log in first.")
        return

    user_id = st.session_state["user_id"]

    transactions_df = get_transactions(user_id)

    income, expense, net_savings = calculate_net_savings(user_id)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Income", f"${income:.2f}")
    col2.metric("Total Expense", f"${expense:.2f}")
    col3.metric("Net Savings", f"${net_savings:.2f}")

    st.markdown("---")

    visualize_spending(transactions_df)