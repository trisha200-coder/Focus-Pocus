import streamlit as st
from styles import apply_styles
from services.state import initialize_state

initialize_state()

st.set_page_config(
    page_title="Focus Pocus",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_styles()

if not st.session_state.logged_in and not st.session_state.authenticated:
    st.session_state.current_page = "Login"

st.sidebar.title("🎯 Focus Pocus")
st.sidebar.caption("Focus better. Achieve more.")

if st.session_state.logged_in or st.session_state.authenticated:
    pages = ["Dashboard", "Study Routine", "Focus Timer"]
    selected_page = st.sidebar.radio(
        "Navigate",
        pages,
        index=pages.index(st.session_state.current_page) if st.session_state.current_page in pages else 0
    )
    st.session_state.current_page = selected_page

    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.authenticated = False
        st.session_state.current_page = "Login"
        st.rerun()

# Run the selected page script
page_mapping = {
    "Login": "pages/login.py",
    "Dashboard": "pages/dashboard.py",
    "Study Routine": "pages/study_routine.py",
    "Focus Timer": "pages/focus_timer.py"
}

target_file = page_mapping.get(st.session_state.current_page, "pages/login.py")
with open(target_file, "r", encoding="utf-8") as f:
    exec(f.read(), globals())