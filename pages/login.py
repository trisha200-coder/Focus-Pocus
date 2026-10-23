
import streamlit as st


# ---------- Page styling ----------
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }

    .login-container {
        max-width: 540px;
        margin: 35px auto 0 auto;
        padding: 36px;
        background: linear-gradient(145deg, #201b2f, #13111d);
        border: 1px solid #3b3050;
        border-radius: 24px;
        box-shadow: 0 20px 80px rgba(124, 77, 255, 0.12);
    }

    .login-eyebrow {
        color: #b9a7f9;
        text-transform: uppercase;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
    }

    .login-subtitle {
        color: #aaa4bc;
        line-height: 1.7;
    }

    .login-footer {
        color: #aaa4bc;
        font-size: 12px;
        text-align: center;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------- Login form ----------
left, center, right = st.columns([1, 2, 1])

with center:
    st.markdown(
        '<div class="login-container">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-eyebrow">YOUR PERSONAL STUDY SPACE</div>',
        unsafe_allow_html=True
    )

    st.markdown("# 🌙 Focus Pocus")

    st.markdown(
        '<p class="login-subtitle">'
        'Less scrolling. More becoming.<br>'
        'Build focus one small session at a time.'
        '</p>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.subheader("Welcome back")

    with st.form("focus_pocus_login"):
        name = st.text_input(
            "Your name",
            placeholder="Enter your name"
        )

        email = st.text_input(
            "Email address",
            placeholder="you@example.com"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter a password"
        )

        remember = st.checkbox("Keep me signed in during this session")

        submitted = st.form_submit_button(
            "Enter your study space →",
            use_container_width=True
        )

        if submitted:
        if not name.strip() or not email.strip() or not password:
            st.error("Please complete all fields.")
        elif "@" not in email or "." not in email.split("@")[-1]:
            st.error("Please enter a valid email address.")
        else:
            # Demo login: save credentials to session state
            st.session_state.user_name = name.strip().split()[0]
            st.session_state.login_email = email.strip()
            
            # 1. Mark the user as logged in
            st.session_state.logged_in = True
            st.session_state.authenticated = True
            
            # 2. Tell app.py to switch to Dashboard
            st.session_state.current_page = "Dashboard"

            st.success("Welcome to Focus Pocus! ✨")
            
            # 3. Trigger an immediate rerun to load the Dashboard
            st.rerun()
    st.markdown(
        '<div class="login-footer">'
        'A gentle space to learn, grow, and try again.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)
