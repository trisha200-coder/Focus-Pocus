import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta

def initialize_state():
    defaults = {
        "logged_in": False,
        "authenticated": False,
        "user_name": "Student",
        "login_email": "",
        "current_page": "Login",
        "subjects": ["Data Structures", "Mathematics", "Machine Learning"],
        "sessions": [],
        "focus_minutes": 25,
        "daily_goal": 120,
        "streak": 0,
        "last_study_day": "",
        "xp": 0,
        "level": 1,
        "timer_running": False,
        "timer_end": None,
        "timer_subject": "Data Structures",
        "timer_duration": 25,
        "timer_paused_remaining": None,
        "chat": [
            {"role": "assistant", "content": "Hey! I'm your Focus Buddy 🌙 Tell me what you're studying today."}
        ],
        "study_goal_minutes": 120,
        "weekly_routine": {
            "Monday": 2.0, "Tuesday": 2.5, "Wednesday": 1.5,
            "Thursday": 3.0, "Friday": 2.0, "Saturday": 4.0, "Sunday": 1.0
        }
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def minutes_today():
    today_s = date.today().isoformat()
    return sum(s.get("minutes", 0) for s in st.session_state.get("sessions", []) if s.get("date") == today_s)

def award_session(subject, minutes):
    today_s = date.today().isoformat()
    if st.session_state.last_study_day != today_s:
        yesterday_s = (date.today() - timedelta(days=1)).isoformat()
        if st.session_state.last_study_day == yesterday_s:
            st.session_state.streak += 1
        else:
            st.session_state.streak = 1
        st.session_state.last_study_day = today_s
    xp_gain = max(1, minutes * 2)
    st.session_state.xp += xp_gain
    st.session_state.level = st.session_state.xp // 200 + 1
    st.session_state.sessions.append({
        "date": today_s,
        "subject": subject,
        "minutes": minutes,
        "xp": xp_gain,
        "completed_at": datetime.now().strftime("%H:%M")
    })
    st.session_state.timer_running = False
    st.session_state.timer_end = None
    st.session_state.timer_paused_remaining = None

def achievements():
    sessions = st.session_state.get("sessions", [])
    total_mins = sum(s.get("minutes", 0) for s in sessions)
    return [
        ("🌱 First Focus", len(sessions) >= 1),
        ("⏳ Deep Work", total_mins >= 60),
        ("🔥 Five Sessions", len(sessions) >= 5),
        ("⚡ 100 XP Club", st.session_state.get("xp", 0) >= 100),
        ("📚 Triple Threat", len(set(s.get("subject") for s in sessions)) >= 3),
        ("🌟 Master of Focus", st.session_state.get("streak", 0) >= 3),
    ]
