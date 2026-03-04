import streamlit as st

from app.components.charts import visualize_spending
from app.services.transaction_service import calculate_net_savings, get_transactions



def show():
    st.subheader("Analytics")
    if "user_id" not in st.session_state:
        st.warning("Please log in first.")
        return

    transactions_df = get_transactions(st.session_state["user_id"])
    income, expense, net_savings = calculate_net_savings(st.session_state["user_id"])

    st.metric("Total Income", f"${income:.2f}")
    st.metric("Total Expense", f"${expense:.2f}")
    st.metric("Net Savings", f"${net_savings:.2f}")

    visualize_spending(transactions_df)