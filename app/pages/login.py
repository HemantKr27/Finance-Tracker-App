import streamlit as st

from app.services.auth_service import authenticate_user



def show():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user_id = authenticate_user(username, password)
        if user_id:
            st.success(f"Welcome, {username}!")
            st.session_state["user_id"] = user_id
            st.session_state["page"] = "Add Transaction"
        else:
            st.error("Invalid username or password.")
