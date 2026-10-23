
import streamlit as st
from styles import apply_styles

# Page configuration
st.set_page_config(
    page_title="Focus Pocus",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply shared styling
apply_styles()

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_page" not in st.session_state:
    st.session_state.current_page = "Login"

# App title
st.sidebar.title("🎯 Focus Pocus")
st.sidebar.caption("Focus better. Achieve more.")

# Navigation
if st.session_state.logged_in:
    pages = [
        "Dashboard",
        "Study Routine",
        "Focus Timer"
    ]

    selected_page = st.sidebar.radio(
        "Navigate",
        pages,
        index=(
            pages.index(st.session_state.current_page)
            if st.session_state.current_page in pages
            else 0
        )
    )

    st.session_state.current_page = selected_page

    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_page = "Login"
        st.rerun()

else:
    st.session_state.current_page = "Login"

# Load the selected page
if st.session_state.current_page == "Login":
    from pages.login import login_page
login_page()

elif st.session_state.current_page == "Dashboard":
    from pages.dashboard import dashboard_page
    dashboard_page()

elif st.session_state.current_page == "Study Routine":
    from pages.study_routine import study_routine_page
    study_routine_page()

elif st.session_state.current_page == "Focus Timer":
    from pages.focus_timer import focus_timer_page
    focus_timer_page()



