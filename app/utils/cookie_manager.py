import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

cookies = EncryptedCookieManager(
    prefix="finance_tracker_",
    password="very_strong_password"
)

# wait until cookies are ready
if not cookies.ready():
    st.stop()