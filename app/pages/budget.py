import streamlit as st
from datetime import datetime

from app.services.budget_service import (
    set_budget,
    get_budget_status
)

from app.services.category_service import get_categories


def show():

    st.subheader("Budget Manager")

    if "user_id" not in st.session_state:
        st.warning("Please log in first.")
        return

    user_id = st.session_state["user_id"]

    categories = get_categories()

    if not categories:
        st.warning("No categories found.")
        return

    category_names = [c["name"] for c in categories]

    # --- Budget Setup Form ---

    st.markdown("### Set Monthly Budget")

    col1, col2 = st.columns(2)

    with col1:
        selected_category = st.selectbox("Category", category_names)

    with col2:
        amount = st.number_input("Budget Amount", min_value=0.0, format="%.2f")

    today = datetime.today()

    col3, col4 = st.columns(2)

    with col3:
        month = st.selectbox("Month", list(range(1, 13)), index=today.month - 1)

    with col4:
        year = st.number_input("Year", value=today.year)

    if st.button("Save Budget"):

        category_id = next(
            c["id"] for c in categories if c["name"] == selected_category
        )

        set_budget(user_id, category_id, amount, month, year)

        st.success("Budget saved successfully!")

    st.divider()

    # --- Budget Status Display ---

    st.markdown("### Budget Status")

    for category in categories:

        category_id = category["id"]
        category_name = category["name"]

        status = get_budget_status(user_id, category_id, month, year)

        if status["budget"] == 0:
            continue

        spent = status["spent"]
        budget = status["budget"]
        remaining = status["remaining"]
        percentage = status["percentage"]

        st.markdown(f"#### {category_name}")

        st.progress(min(int(percentage), 100))

        col1, col2, col3 = st.columns(3)

        col1.metric("Budget", f"${budget:.2f}")
        col2.metric("Spent", f"${spent:.2f}")
        col3.metric("Remaining", f"${remaining:.2f}")

        if status["status"] == "Exceeded":
            st.error("⚠ Budget exceeded!")

        elif status["status"] == "Warning":
            st.warning("⚠ Approaching budget limit")

        st.markdown("---")