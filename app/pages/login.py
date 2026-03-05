import streamlit as st

from app.services.auth_service import authenticate_user
from app.services.jwt_handler import create_token
from app.utils.cookie_manager import cookies


def show():

    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if not username or not password:
            st.warning("Please enter username and password")
            return

        user_id = authenticate_user(username, password)

        if user_id:

            # create JWT token
            token = create_token(user_id)

            #store JWT token
            cookies["jwt_token"] = token
            cookies.save()

            # save session
            st.session_state["token"] = token
            st.session_state["user_id"] = user_id
            st.session_state["page"] = "Dashboard"

            st.success("Login successful!")

            st.rerun()

        else:
            st.error("Invalid username or password.")