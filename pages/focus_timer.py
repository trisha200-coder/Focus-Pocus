
import streamlit as st
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

from services.state import award_session


# ---------- Page header ----------
st.markdown(
    '<div class="fp-eyebrow">ONE THING AT A TIME</div>',
    unsafe_allow_html=True
)

st.title("Focus Timer")
st.write(
    "You don't need a perfect session. "
    "You just need a place to begin."
)


# ---------- Session settings ----------
subjects = st.session_state.subjects or ["General Study"]

if st.session_state.timer_subject not in subjects:
    st.session_state.timer_subject = subjects[0]

timer_active = st.session_state.timer_running

col1, col2 = st.columns([1.4, 1])

with col1:
    st.selectbox(
        "Studying",
        subjects,
        key="timer_subject",
        disabled=timer_active
    )

with col2:
    st.number_input(
        "Session length (minutes)",
        min_value=1,
        max_value=180,
        step=5,
        key="timer_duration",
        disabled=timer_active
    )


# ---------- Live timer refresh ----------
# Refresh the Streamlit page every second while running.
if st.session_state.timer_running:
    st_autorefresh(
        interval=1000,
        limit=None,
        key="focus_timer_refresh"
    )


# ---------- Calculate remaining time ----------
if (
    st.session_state.timer_running
    and st.session_state.timer_end is not None
):
    seconds_left = max(
        0,
        int(
            (
                st.session_state.timer_end - datetime.now()
            ).total_seconds()
        )
    )

elif st.session_state.timer_paused_remaining is not None:
    seconds_left = int(
        st.session_state.timer_paused_remaining
    )

else:
    seconds_left = int(
        st.session_state.timer_duration
    ) * 60


minutes, seconds = divmod(seconds_left, 60)

total_seconds = max(
    1,
    int(st.session_state.timer_duration) * 60
)

progress = max(
    0.0,
    min(1.0, 1 - seconds_left / total_seconds)
)


# ---------- Timer display ----------
left, center, right = st.columns([1, 1.5, 1])

with center:
    st.markdown(
        '<div class="fp-card" '
        'style="text-align:center;padding:34px 22px;">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="fp-eyebrow">YOUR CURRENT SESSION</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div style="font-family:Space Grotesk;'
        f'font-size:5rem;font-weight:700;'
        f'letter-spacing:-.06em;color:#d4c4ff;">'
        f'{minutes:02d}:{seconds:02d}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<p class="fp-muted">📘 '
        f'{st.session_state.timer_subject} · '
        f'{st.session_state.timer_duration} minute session</p>',
        unsafe_allow_html=True
    )

    st.progress(progress)


    # ---------- Session completed ----------
    if (
        st.session_state.timer_running
        and seconds_left <= 0
    ):
        completed_subject = st.session_state.timer_subject
        completed_minutes = int(
            st.session_state.timer_duration
        )

        award_session(
            completed_subject,
            completed_minutes
        )

        st.success(
            f"🎉 Session complete! You earned "
            f"{completed_minutes * 2} XP."
        )

        st.balloons()
        st.rerun()


    # ---------- Running ----------
    elif st.session_state.timer_running:
        st.success(
            "🌙 Focus mode is on. Keep going, one minute at a time."
        )

        if st.button(
            "⏸ Pause session",
            use_container_width=True
        ):
            st.session_state.timer_paused_remaining = seconds_left
            st.session_state.timer_running = False
            st.session_state.timer_end = None
            st.rerun()


    # ---------- Paused ----------
    elif st.session_state.timer_paused_remaining is not None:
        st.warning("Your session is paused.")

        if st.button(
            "▶ Resume session",
            use_container_width=True
        ):
            st.session_state.timer_end = (
                datetime.now()
                + timedelta(
                    seconds=int(
                        st.session_state.timer_paused_remaining
                    )
                )
            )

            st.session_state.timer_running = True
            st.session_state.timer_paused_remaining = None
            st.rerun()

        if st.button(
            "↻ Reset timer",
            use_container_width=True
        ):
            st.session_state.timer_running = False
            st.session_state.timer_end = None
            st.session_state.timer_paused_remaining = None
            st.rerun()


    # ---------- Ready to start ----------
    else:
        if st.button(
            "▶ Start focus session",
            use_container_width=True
        ):
            st.session_state.timer_end = (
                datetime.now()
                + timedelta(
                    minutes=int(st.session_state.timer_duration)
                )
            )

            st.session_state.timer_running = True
            st.session_state.timer_paused_remaining = None
            st.rerun()


    st.markdown("</div>", unsafe_allow_html=True)


# ---------- Helpful note ----------
st.caption(
    "Earn 2 XP per minute after completing a session. "
    "You can change the session duration before starting."
)
