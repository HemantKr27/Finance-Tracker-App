import streamlit as st
from app.pages import login, register, dashboard, transactions, analytics
from app.database.models import create_tables

def main():
    st.set_page_config(page_title="Finance Tracker", layout="wide")

    create_tables()

    # Initialize session state
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = None

    st.sidebar.title("💰 Finance Tracker")

    # --------- NOT LOGGED IN ---------
    if not st.session_state["user_id"]:
        page = st.sidebar.radio("Navigation", ["Login", "Register"])

        if page == "Login":
            login.show()
        else:
            register.show()

    # --------- LOGGED IN ---------
    else:
        page = st.sidebar.radio(
            "Navigation",
            ["Dashboard", "Add Transaction", "History", "Analytics", "Logout"]
        )

        if page == "Dashboard":
            dashboard.show()

        elif page == "Add Transaction":
            transactions.show_add()

        elif page == "History":
            transactions.show_history()

        elif page == "Analytics":
            analytics.show()

        elif page == "Logout":
            st.session_state.clear()
            st.rerun()


if __name__ == "__main__":
    main()