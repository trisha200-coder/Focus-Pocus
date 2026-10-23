
import streamlit as st
import pandas as pd
from datetime import date, timedelta

from services.state import minutes_today, achievements


# ---------- Header ----------
st.markdown(
    '<div class="fp-eyebrow">YOUR SPACE · YOUR PACE</div>',
    unsafe_allow_html=True
)

st.title(f"Good to see you, {st.session_state.user_name} ✨")
st.write("Small, focused sessions add up. Let's make today count.")


# ---------- Today's statistics ----------
today_minutes = minutes_today()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Focused today",
    f"{today_minutes // 60}h {today_minutes % 60:02d}m"
)

col2.metric(
    "Daily goal",
    f"{st.session_state.daily_goal // 60}h "
    f"{st.session_state.daily_goal % 60:02d}m"
)

col3.metric(
    "Current streak",
    f"🔥 {st.session_state.streak} days"
)

col4.metric(
    "Focus XP",
    f"✨ {st.session_state.xp}"
)

st.divider()


# ---------- Main dashboard layout ----------
main, side = st.columns([1.6, 1], gap="large")


# ---------- Subjects ----------
with main:
    st.subheader("📚 Pick a subject")
    st.caption("Choose a subject to start your focus session.")

    subjects = st.session_state.subjects

    if subjects:
        subject_columns = st.columns(2)

        for i, subject in enumerate(subjects):
            with subject_columns[i % 2]:
                st.markdown(
                    '<div class="fp-card">',
                    unsafe_allow_html=True
                )

                st.markdown(f"### 📘 {subject}")

                subject_sessions = [
                    session
                    for session in st.session_state.sessions
                    if session["subject"] == subject
                ]

                subject_minutes = sum(
                    session["minutes"]
                    for session in subject_sessions
                )

                st.caption(
                    f"{len(subject_sessions)} sessions · "
                    f"{subject_minutes // 60}h "
                    f"{subject_minutes % 60:02d}m studied"
                )

                if st.button(
                    "Start focus →",
                    key=f"start_subject_{i}",
                    use_container_width=True
                ):
                    st.session_state.timer_subject = subject
                    st.session_state.timer_duration = int(
                        st.session_state.focus_minutes
                    )
                    st.session_state.timer_running = False
                    st.session_state.timer_end = None
                    st.session_state.timer_paused_remaining = None

                    st.session_state.current_page = "Focus Timer"
                    st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.info("Add a subject to begin studying.")

    # ---------- Add subject ----------
    with st.expander("＋ Add a subject"):
        with st.form("add_subject_form"):
            new_subject = st.text_input(
                "Subject name",
                placeholder="e.g. Operating Systems"
            )

            add_clicked = st.form_submit_button("Add subject")

        if add_clicked:
            clean_subject = new_subject.strip()

            if not clean_subject:
                st.warning("Please enter a subject name.")

            elif clean_subject in st.session_state.subjects:
                st.warning("This subject already exists.")

            else:
                st.session_state.subjects.append(clean_subject)
                st.success(f"{clean_subject} added!")
                st.rerun()

    # ---------- Weekly study chart ----------
    st.subheader("📊 Your weekly rhythm")

    chart_data = []

    for offset in range(6, -1, -1):
        day = date.today() - timedelta(days=offset)

        minutes = sum(
            session["minutes"]
            for session in st.session_state.sessions
            if session["date"] == day.isoformat()
        )

        chart_data.append({
            "Day": day.strftime("%a"),
            "Hours studied": round(minutes / 60, 2)
        })

    chart_df = pd.DataFrame(chart_data)

    st.bar_chart(
        chart_df.set_index("Day"),
        height=230
    )

    if st.button(
        "View study routine →",
        use_container_width=True
    ):
        st.session_state.current_page = "Study Routine"
        st.rerun()


# ---------- Right column ----------
with side:

    # ---------- Daily goal ----------
    remaining = max(
        0,
        int(st.session_state.daily_goal) - today_minutes
    )

    st.markdown(
        '<div class="fp-card">',
        unsafe_allow_html=True
    )

    st.subheader("🌱 Today's goal")

    st.markdown(
        f'<div class="fp-big">'
        f'{remaining // 60}h {remaining % 60:02d}m'
        f'</div>'
        '<p class="fp-muted">left to reach your goal</p>',
        unsafe_allow_html=True
    )

    st.progress(
        min(
            1.0,
            today_minutes / max(1, st.session_state.daily_goal)
        )
    )

    if today_minutes == 0:
        if st.session_state.subjects:
            suggested_subject = st.session_state.subjects[0]
        else:
            suggested_subject = "your favourite subject"

        goal_message = (
            f"Start small: try one "
            f"{st.session_state.focus_minutes}-minute session "
            f"in {suggested_subject}. You can do this!"
        )

    elif remaining > 0:
        suggested_minutes = min(
            remaining,
            st.session_state.focus_minutes
        )

        goal_message = (
            f"You've already focused for {today_minutes} minutes. "
            f"Try another {suggested_minutes}-minute session, "
            "then take a proper break."
        )

    else:
        goal_message = (
            "You reached your daily goal! 🎉 "
            "Celebrate your progress and rest if you need to."
        )

    st.write(goal_message)

    st.markdown("</div>", unsafe_allow_html=True)


    # ---------- Focus Buddy ----------
    st.markdown(
        '<div class="fp-card">',
        unsafe_allow_html=True
    )

    st.subheader("💬 Focus Buddy")
    st.caption("Supportive nudges, no guilt.")

    for message in st.session_state.chat[-4:]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input(
        "Ask for a study goal or encouragement…"
    )

    if prompt:
        st.session_state.chat.append({
            "role": "user",
            "content": prompt
        })

        lower_prompt = prompt.lower()

        if any(
            word in lower_prompt
            for word in ["goal", "plan", "today"]
        ):
            reply = goal_message

        elif any(
            word in lower_prompt
            for word in ["tired", "overwhelmed", "stress"]
        ):
            reply = (
                "Let's make it easier. Try just two minutes "
                "of one small task. You can decide whether "
                "to continue afterward."
            )

        elif any(
            word in lower_prompt
            for word in ["distract", "phone", "scroll"]
        ):
            reply = (
                "Put your phone out of reach, close distracting "
                "tabs, and try a 10-minute focus sprint."
            )

        else:
            reply = (
                f"Choose one small task and focus for "
                f"{min(10, st.session_state.focus_minutes)} minutes. "
                "Then check in with yourself."
            )

        st.session_state.chat.append({
            "role": "assistant",
            "content": reply
        })

        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


    # ---------- Reward system ----------
    st.markdown(
        '<div class="fp-card">',
        unsafe_allow_html=True
    )

    st.subheader("🏆 Reward shelf")

    st.markdown(
        f'<div class="fp-big">'
        f'Level {st.session_state.level}'
        f'</div>'
        f'<p class="fp-muted">'
        f'{st.session_state.xp} XP earned'
        f'</p>',
        unsafe_allow_html=True
    )

    xp_in_level = st.session_state.xp % 200

    st.progress(xp_in_level / 200)

    st.caption(
        f"{200 - xp_in_level} XP until your next level"
    )

    st.markdown("**Achievements**")

    for name, unlocked, *_ in achievements():
        if unlocked:
            st.write(f"🏅 {name}")
        else:
            st.write(f"🔒 {name}")

    st.markdown("</div>", unsafe_allow_html=True)
