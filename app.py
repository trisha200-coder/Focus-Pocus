import streamlit as st
from styles import apply_styles
from services.state import initialize_state

# Page configuration - must be the first Streamlit command
st.set_page_config(
    page_title="Focus Pocus",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

initialize_state()
apply_styles()

# Define all pages with clean titles and icons
login_page = st.Page("pages/login.py", title="Login", icon="🌙")
dashboard_page = st.Page("pages/dashboard.py", title="Dashboard", icon="📊", default=True)
routine_page = st.Page("pages/study_routine.py", title="Study Routine", icon="📅")
timer_page = st.Page("pages/focus_timer.py", title="Focus Timer", icon="⏱️")

is_authenticated = st.session_state.get("logged_in", False) or st.session_state.get("authenticated", False)

if not is_authenticated:
    # Hide sidebar navigation completely during login
    pg = st.navigation([login_page], position="hidden")
else:
    # Sidebar header
    st.sidebar.title("🎯 Focus Pocus")
    st.sidebar.caption("Focus better. Achieve more.")
    
    # Modern Streamlit navigation - only show main app pages
    pg = st.navigation({
        "Navigate": [dashboard_page, routine_page, timer_page]
    })
    
    # Logout button in sidebar
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.authenticated = False
        st.rerun()

pg.run()
