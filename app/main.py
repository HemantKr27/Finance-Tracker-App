import streamlit as st

from app.pages import login, register, dashboard, transactions, analytics
from app.database.models import create_tables
from app.services.jwt_handler import verify_token
from app.utils.cookie_manager import cookies


def init_session():
    """Initialize session variables"""

    if "user_id" not in st.session_state:
        st.session_state.user_id = None

    if "token" not in st.session_state:
        st.session_state.token = None

    if "page" not in st.session_state:
        st.session_state.page = "Login"


def restore_login():
    """Restore login using JWT cookie"""

    if not st.session_state.token:

        token = cookies.get("jwt_token")

        if token:
            user_id = verify_token(token)

            if user_id:
                st.session_state.token = token
                st.session_state.user_id = user_id
                st.session_state.page = "Dashboard"


def show_auth_pages():
    """Login / Register navigation"""

    page = st.sidebar.radio(
        "Navigation",
        ["Login", "Register"]
    )

    if page == "Login":
        login.show()
    else:
        register.show_register_page()


def show_app_pages():
    """Main application navigation"""

    pages = {
        "Dashboard": dashboard.show,
        "Add Transaction": transactions.show_add,
        "History": transactions.show_history,
        "Analytics": analytics.show
    }

    menu = list(pages.keys()) + ["Logout"]

    page = st.sidebar.radio("Navigation", menu)

    if page == "Logout":

        cookies["jwt_token"] = ""
        cookies.save()

        st.session_state.clear()
        st.rerun()

    # show selected page
    pages[page]()


def main():

    st.set_page_config(
        page_title="Finance Tracker",
        layout="wide"
    )

    create_tables()

    init_session()
    restore_login()

    st.sidebar.title("💰 Finance Tracker")
    st.sidebar.markdown("---")

    if st.session_state.user_id:
        show_app_pages()
    else:
        show_auth_pages()


if __name__ == "__main__":
    main()