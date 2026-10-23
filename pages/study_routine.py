
import streamlit as st
import pandas as pd
from datetime import date, timedelta

from services.state import minutes_today



# ---------- PAGE STYLING ----------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #100b20, #19102e, #0c1226);
        color: #f5f3ff;
    }

    .routine-card {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(190, 160, 255, 0.18);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 12px;
    }

    .muted {
        color: #b9b0d0;
        font-size: 14px;
    }

    h1, h2, h3 {
        color: #f5f3ff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- SESSION STATE ----------
if "study_goal_minutes" not in st.session_state:
    st.session_state.study_goal_minutes = 120

if "weekly_routine" not in st.session_state:
    st.session_state.weekly_routine = {
        "Monday": 2.0,
        "Tuesday": 2.5,
        "Wednesday": 1.5,
        "Thursday": 3.0,
        "Friday": 2.0,
        "Saturday": 4.0,
        "Sunday": 1.0,
    }

if "subjects" not in st.session_state:
    st.session_state.subjects = [
        "Models of Computation",
        "Data Structures",
        "Object-Oriented Programming",
        "Mathematics",
    ]

if "subject_progress" not in st.session_state:
    st.session_state.subject_progress = {
        subject: 0 for subject in st.session_state.subjects
    }

# ---------- HEADER ----------
st.title("📊 Your Study Routine")
st.markdown(
    "Build consistency, track your study hours, and improve one day at a time."
)

st.write("")

# ---------- TOP METRICS ----------
today_minutes = minutes_today()
weekly_hours = sum(st.session_state.weekly_routine.values())
daily_goal = st.session_state.study_goal_minutes

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Today's Focus", f"{today_minutes // 60}h {today_minutes % 60}m")

with col2:
    st.metric("Weekly Study Hours", f"{weekly_hours:.1f} hrs")

with col3:
    st.metric("Daily Goal", f"{daily_goal // 60} minutes")

st.divider()

# ---------- DAILY GOAL ----------
st.subheader("🎯 Daily Study Goal")

new_goal = st.slider(
    "How many minutes do you want to study each day?",
    min_value=30,
    max_value=480,
    step=15,
    value=int(st.session_state.study_goal_minutes),
)

st.session_state.study_goal_minutes = new_goal

goal_progress = min(today_minutes / new_goal, 1.0) if new_goal else 0

st.progress(goal_progress)

if today_minutes >= new_goal:
    st.success("Daily goal completed! Great work 🎉")
else:
    remaining = new_goal - today_minutes
    st.info(f"{remaining} more minutes to reach today's goal.")

st.divider()

# ---------- WEEKLY STUDY CHART ----------
st.subheader("📅 Weekly Study Overview")

weekly_data = pd.DataFrame(
    {
        "Day": list(st.session_state.weekly_routine.keys()),
        "Hours Studied": list(st.session_state.weekly_routine.values()),
    }
)

st.bar_chart(
    weekly_data.set_index("Day"),
    y="Hours Studied",
)

average_hours = weekly_data["Hours Studied"].mean()

st.caption(
    f"Your planned weekly average is {average_hours:.1f} hours per day."
)

st.divider()

# ---------- EDIT WEEKLY ROUTINE ----------
st.subheader("🗓️ Customize Your Routine")

st.caption(
    "Set your planned study hours for each day. These are routine targets, "
    "not automatically recorded study sessions."
)

with st.form("weekly_routine_form"):
    updated_hours = {}

    days = list(st.session_state.weekly_routine.keys())
    columns = st.columns(2)

    for index, day in enumerate(days):
        with columns[index % 2]:
            updated_hours[day] = st.number_input(
                f"{day}",
                min_value=0.0,
                max_value=16.0,
                step=0.5,
                value=float(st.session_state.weekly_routine[day]),
                key=f"routine_{day}",
            )

    save_routine = st.form_submit_button(
        "💾 Save Weekly Routine",
        use_container_width=True,
    )

    if save_routine:
        st.session_state.weekly_routine = updated_hours
        st.success("Your weekly routine has been updated!")
        st.rerun()

st.divider()

# ---------- SUBJECT TRACKER ----------
st.subheader("📚 Subject Progress")

st.caption(
    "Update the percentage of each subject's syllabus you have completed."
)

subjects = st.session_state.subjects

for subject in subjects:
    with st.container(border=True):
        st.markdown(f"**{subject}**")

        current_progress = st.session_state.subject_progress.get(subject, 0)

        progress = st.slider(
            f"Completion for {subject}",
            min_value=0,
            max_value=100,
            value=int(current_progress),
            step=5,
            key=f"progress_{subject}",
        )

        st.session_state.subject_progress[subject] = progress
        st.progress(progress / 100)

        if progress == 100:
            st.success("Subject completed! 🎉")
        else:
            st.caption(f"{progress}% completed")

# ---------- ADD SUBJECT ----------
with st.expander("➕ Add a new subject"):
    new_subject = st.text_input(
        "Subject name",
        placeholder="e.g. Database Management Systems",
    )

    if st.button("Add Subject", use_container_width=True):
        clean_subject = new_subject.strip()

        if not clean_subject:
            st.warning("Enter a subject name first.")
        elif clean_subject in st.session_state.subjects:
            st.warning("This subject already exists.")
        else:
            st.session_state.subjects.append(clean_subject)
            st.session_state.subject_progress[clean_subject] = 0
            st.success(f"{clean_subject} added successfully!")
            st.rerun()

st.divider()

# ---------- MOTIVATION ----------
st.subheader("✨ Keep Going")

completed_subjects = sum(
    1
    for progress in st.session_state.subject_progress.values()
    if progress == 100
)

total_subjects = len(st.session_state.subject_progress)

st.markdown(
    f"""
    <div class="routine-card">
        <h3>Small steps make big progress.</h3>
        <p class="muted">
            You've completed {completed_subjects} out of {total_subjects}
            tracked subjects. Keep showing up for your goals!
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.button("⏱️ Start a Focus Session", use_container_width=True):
    st.switch_page("pages/focus_timer.py")
