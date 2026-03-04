from datetime import datetime

import streamlit as st

from app.services.transaction_service import add_transaction, delete_transaction, get_transactions, update_transaction


def show_add():
    st.subheader("Add Transaction")
    if "user_id" not in st.session_state:
        st.warning("Please log in first.")
        return

    category = st.selectbox("Category", ["Food", "Entertainment", "Bills", "Shopping", "Salary", "Others"])
    type_ = st.radio("Type", ["Income", "Expense"])
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    date = st.date_input("Date")
    description = st.text_input("Description")

    if st.button("Add Transaction"):
        if amount > 0:
            add_transaction(st.session_state["user_id"], category, amount, type_, date, description)
            st.success("Transaction added!")
        else:
            st.error("Amount must be greater than 0.")


def show_history():
    st.subheader("Transaction History")
    if "user_id" not in st.session_state:
        st.warning("Please log in first.")
        return

    # Filters for transaction history
    start_date = st.date_input("Start Date", value=datetime(2021, 1, 1))
    end_date = st.date_input("End Date", value=datetime.now())
    category = st.selectbox("Category", ["All", "Food", "Entertainment", "Bills", "Shopping", "Salary", "Others"])

    transactions_df = get_transactions(st.session_state["user_id"], start_date, end_date, category)
    if not transactions_df.empty:
        st.dataframe(transactions_df)

        # Option to export as CSV
        csv = transactions_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"transaction_history_{datetime.now().strftime('%Y-%m-%d')}.csv",
            mime="text/csv",
        )

        # Editing and Deleting Transactions
        transaction_id = st.selectbox("Select Transaction to Edit or Delete", transactions_df["id"])
        transaction = transactions_df[transactions_df["id"] == transaction_id].iloc[0]

        st.subheader("Edit Transaction")
        category = st.selectbox("Category", ["Food", "Entertainment", "Bills", "Shopping", "Salary", "Others"],
                                index=["Food", "Entertainment", "Bills", "Shopping", "Salary", "Others"].index(
                                    transaction["category"]))
        type_ = st.radio("Type", ["Income", "Expense"], index=["Income", "Expense"].index(transaction["type"]))
        amount = st.number_input("Amount", min_value=0.0, value=transaction["amount"], format="%.2f")
        date = st.date_input("Date", value=datetime.strptime(transaction["date"], "%Y-%m-%d"))
        description = st.text_input("Description", value=transaction["description"])

        if st.button("Update Transaction"):
            if amount > 0:
                update_transaction(transaction_id, category, amount, type_, date, description)
                st.success("Transaction updated!")
            else:
                st.error("Amount must be greater than 0.")

        if st.button("Delete Transaction"):
            delete_transaction(transaction_id)
            st.success("Transaction deleted!")