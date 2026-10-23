
import streamlit as st


def initialize_state():
    defaults = {
        "logged_in": False,
        "authenticated": False,
        "user_name": "",
        "login_email": "",
        "current_page": "Login",
        "subjects": [],
        "study_sessions": [],
        "streak": 0,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
