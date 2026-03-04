import streamlit as st

from app.services.auth_service import register_user


def show_register_page():
    st.subheader("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if username and password:
            success, message = register_user(username, password)
            if success:
                st.success(message)
                st.session_state["page"] = "Login"
            else:
                st.error(message)
        else:
            st.error("Please fill out all fields.")
