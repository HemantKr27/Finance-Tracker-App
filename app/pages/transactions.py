from datetime import datetime
import streamlit as st

from app.services.transaction_service import (
    add_transaction,
    delete_transaction,
    get_transactions,
    update_transaction
)

from app.services.category_service import get_categories


def show_add():
    st.subheader("Add Transaction")

    if "user_id" not in st.session_state:
        st.warning("Please log in first.")
        return

    user_id = st.session_state["user_id"]

    categories = get_categories()
    category_names = [c["name"] for c in categories]

    selected_category = st.selectbox("Category", category_names)
    category_id = next(c["id"] for c in categories if c["name"] == selected_category)

    type_ = st.radio("Type", ["Income", "Expense"])
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    date = st.date_input("Date")
    description = st.text_input("Description")

    if st.button("Add Transaction"):
        if amount > 0:
            add_transaction(user_id, category_id, amount, type_, date, description)
            st.success("Transaction added!")
        else:
            st.error("Amount must be greater than 0.")


def show_history():

    st.subheader("Transaction History")

    if "user_id" not in st.session_state:
        st.warning("Please log in first.")
        return

    user_id = st.session_state["user_id"]

    categories = get_categories()
    category_names = ["All"] + [c["name"] for c in categories]

    start_date = st.date_input("Start Date", value=datetime(2021, 1, 1))
    end_date = st.date_input("End Date", value=datetime.now())
    category = st.selectbox("Category", category_names)

    transactions_df = get_transactions(user_id, start_date, end_date, category)

    if transactions_df.empty:
        st.info("No transactions found.")
        return

    st.dataframe(transactions_df)

    csv = transactions_df.to_csv(index=False)

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"transaction_history_{datetime.now().strftime('%Y-%m-%d')}.csv",
        mime="text/csv",
    )

    transaction_id = st.selectbox(
        "Select Transaction to Edit or Delete",
        transactions_df["id"]
    )

    transaction = transactions_df[transactions_df["id"] == transaction_id].iloc[0]

    st.subheader("Edit Transaction")

    selected_category = st.selectbox(
        "Category",
        category_names[1:],
        index=category_names[1:].index(transaction["category"])
    )

    category_id = next(c["id"] for c in categories if c["name"] == selected_category)

    type_ = st.radio(
        "Type",
        ["Income", "Expense"],
        index=["Income", "Expense"].index(transaction["type"])
    )

    amount = st.number_input(
        "Amount",
        min_value=0.0,
        value=transaction["amount"],
        format="%.2f"
    )

    date = st.date_input(
        "Date",
        value=datetime.strptime(transaction["date"], "%Y-%m-%d")
    )

    description = st.text_input(
        "Description",
        value=transaction["description"]
    )

    if st.button("Update Transaction"):

        if amount > 0:
            update_transaction(
                transaction_id,
                category_id,
                amount,
                type_,
                date,
                description
            )
            st.success("Transaction updated!")

        else:
            st.error("Amount must be greater than 0.")

    if st.button("Delete Transaction"):
        delete_transaction(transaction_id)
        st.success("Transaction deleted!")