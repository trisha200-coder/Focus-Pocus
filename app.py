import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
from pathlib import Path

st.set_page_config(page_title="Focus Pocus", page_icon="🌙", layout="wide", initial_sidebar_state="expanded")

# ---------- Theme ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root { --bg:#0b0a12; --panel:#151321; --panel2:#1b172b; --line:#302842; --purple:#a78bfa; --pink:#e879f9; --mint:#8cf0cf; --muted:#aaa4bc; }
.stApp { background: radial-gradient(ellipse at 80% 0%, #24163a 0%, #0b0a12 48%); color:#f7f4ff; font-family:'DM Sans',sans-serif; }
h1,h2,h3,h4 {font-family:'Space Grotesk',sans-serif !important; letter-spacing:-.035em;}
[data-testid="stSidebar"] { background:#100e19; border-right:1px solid #2b243a; }
[data-testid="stSidebar"] * { color:#f7f4ff; }
div[data-testid="stMetric"] { background:linear-gradient(145deg,#1c182a,#13111d); padding:18px 20px; border:1px solid #302842; border-radius:18px; }
div[data-testid="stMetricLabel"] {color:#aaa4bc;}
div[data-testid="stMetricValue"] {color:#f7f4ff;font-family:'Space Grotesk',sans-serif;}
.stButton>button {border-radius:12px;border:1px solid #45365e;background:linear-gradient(135deg,#9b7cf5,#7653d6);color:white;font-weight:650;min-height:42px;}
.stButton>button:hover {border-color:#d9c9ff;color:white;box-shadow:0 0 22px #9b7cf533;}
.stTextInput input,.stNumberInput input,.stSelectbox div[data-baseweb="select"],.stTextArea textarea {background:#171421!important;color:#fff!important;border:1px solid #393047!important;border-radius:12px!important;}
hr {border-color:#302842;}
div[data-testid="stProgressBar"] > div > div {background:linear-gradient(90deg,#9b7cf5,#e879f9);}
.fp-card {background:linear-gradient(145deg,rgba(32,27,47,.96),rgba(19,17,29,.96));border:1px solid #332a45;border-radius:20px;padding:20px 22px;margin-bottom:12px;box-shadow:0 14px 45px #00000018;}
.fp-eyebrow {color:#b9a7f9;text-transform:uppercase;font-size:.72rem;font-weight:700;letter-spacing:.14em;}
.fp-muted {color:#aaa4bc;font-size:.92rem;}
.fp-big {font-family:'Space Grotesk';font-size:2rem;font-weight:700;line-height:1.15;}
.fp-pill {display:inline-block;padding:5px 10px;border-radius:100px;background:#302445;color:#d8caff;font-size:.75rem;border:1px solid #493663;}
</style>
""", unsafe_allow_html=True)

# ---------- Session state ----------
def init(key, value):
    if key not in st.session_state: st.session_state[key] = value

init("authenticated", False)
init("user_name", "Student")
init("page", "Login")
init("subjects", ["Data Structures", "Mathematics", "Machine Learning"])
init("sessions", [])
init("focus_minutes", 25)
init("daily_goal", 120)
init("streak", 0)
init("last_study_day", "")
init("xp", 0)
init("level", 1)
init("timer_running", False)
init("timer_end", None)
init("timer_subject", "Data Structures")
init("timer_started_at", None)
init("timer_duration", 25)
init("timer_paused_remaining", None)
init("chat", [{"role":"assistant","content":"Hey! I'm your Focus Buddy 🌙 Tell me what you're studying, or ask me to suggest a realistic goal for today."}])
init("login_mode", "Sign in")

PAGES = ["Login", "Dashboard", "Study Routine", "Focus Timer"]

def go(page):
    st.session_state.page = page
    st.rerun()

def get_minutes_by_day(days=7):
    today = date.today()
    result = []
    for i in range(days-1, -1, -1):
        d = today - timedelta(days=i)
        mins = sum(s["minutes"] for s in st.session_state.sessions if s["date"] == d.isoformat())
        result.append({"Day": d.strftime("%a"), "Date": d.isoformat(), "Hours studied": round(mins/60, 2), "Minutes": mins})
    return pd.DataFrame(result)

def award_session(subject, minutes):
    today_s = date.today().isoformat()
    if st.session_state.last_study_day != today_s:
        if st.session_state.last_study_day == (date.today()-timedelta(days=1)).isoformat():
            st.session_state.streak += 1
        else:
            st.session_state.streak = 1
        st.session_state.last_study_day = today_s
    xp_gain = max(1, minutes * 2)
    st.session_state.xp += xp_gain
    st.session_state.level = st.session_state.xp // 200 + 1
    st.session_state.sessions.append({"date":today_s, "subject":subject, "minutes":minutes, "xp":xp_gain, "completed_at":datetime.now().strftime("%H:%M")})
    st.session_state.timer_running = False
    st.session_state.timer_end = None
    st.session_state.timer_paused_remaining = None

def achievements():
    sessions = st.session_state.sessions
    total_mins = sum(s["minutes"] for s in sessions)
    return [
        ("🌱 First Focus", len(sessions) >= 1, "Complete your first session"),
        ("⏳ Deep Work", total_mins >= 60, "Study for 60 minutes total"),
        ("🔥 Five Sessions", len(sessions) >= 5, "Complete five sessions"),
        ("💎 500 XP", st.session_state.xp >= 500, "Earn 500 XP"),
    ]

def header_kicker(text):
    st.markdown(f'<div class="fp-eyebrow">{text}</div>', unsafe_allow_html=True)

# ---------- Login ----------
if not st.session_state.authenticated:
    st.sidebar.markdown("## 🌙 Focus Pocus")
    st.sidebar.caption("Less scrolling. More becoming.")
    st.sidebar.markdown("---")
    st.sidebar.info("A calmer way to build focus, one session at a time.")
    left, center, right = st.columns([1, 1.15, 1])
    with center:
        st.write("")
        st.write("")
        st.markdown('<div class="fp-card">', unsafe_allow_html=True)
        st.markdown('<div class="fp-eyebrow">YOUR PERSONAL STUDY SPACE</div>', unsafe_allow_html=True)
        st.markdown("# 🌙 Focus Pocus")
        st.markdown("### Make a little progress. Then a little more.")
        st.markdown('<p class="fp-muted">Sign in to plan your day, focus with intention, and celebrate the work you actually do.</p>', unsafe_allow_html=True)
        mode = st.radio("Account", ["Sign in", "Create account"], horizontal=True, label_visibility="collapsed")
        with st.form("login_form"):
            name = st.text_input("Your name", value=st.session_state.user_name if st.session_state.user_name != "Student" else "")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Enter your study space", use_container_width=True)
        if submit:
            if name.strip() and email.strip() and password.strip():
                st.session_state.user_name = name.strip().split()[0]
                st.session_state.authenticated = True
                st.session_state.page = "Dashboard"
                st.rerun()
            else: st.warning("Please fill in all three fields. This is a frontend demo; authentication is not connected to a server.")
        st.caption("Demo sign-in only · Your progress stays in this browser session.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ---------- Sidebar navigation ----------
with st.sidebar:
    st.markdown("# 🌙 Focus Pocus")
    st.caption("LESS SCROLLING. MORE BECOMING.")
    st.markdown("---")
    st.markdown(f"**Hey, {st.session_state.user_name} 👋**")
    st.caption("Your focus space")
    for p, icon in [("Dashboard","◈"),("Study Routine","▦"),("Focus Timer","◷")]:
        if st.button(f"{icon}   {p}", key=f"nav_{p}", use_container_width=True):
            go(p)
    st.markdown("---")
    st.markdown('<div class="fp-eyebrow">YOUR PROGRESS</div>', unsafe_allow_html=True)
    st.metric("Current level", st.session_state.level)
    st.progress((st.session_state.xp % 200)/200, text=f"{st.session_state.xp % 200}/200 XP to next level")
    st.caption(f"✨ {st.session_state.xp} total XP  ·  🔥 {st.session_state.streak}-day streak")
    if st.button("Log out", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.page = "Login"
        st.rerun()

# ---------- Dashboard ----------
if st.session_state.page == "Dashboard":
    header_kicker("YOUR SPACE · YOUR PACE")
    st.title(f"Good to see you, {st.session_state.user_name} ✨")
    st.markdown("Small, focused sessions add up. Let's make today count.")
    df = get_minutes_by_day(7)
    today_minutes = int(df.iloc[-1]["Minutes"])
    total_sessions = len(st.session_state.sessions)
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Focused today", f"{today_minutes//60}h {today_minutes%60:02d}m")
    c2.metric("Daily goal", f"{st.session_state.daily_goal//60}h {st.session_state.daily_goal%60:02d}m")
    c3.metric("Current streak", f"🔥 {st.session_state.streak} days")
    c4.metric("Focus XP", f"✨ {st.session_state.xp}")
    st.markdown("---")
    main, side = st.columns([1.65, 1], gap="large")
    with main:
        st.subheader("Pick a subject")
        st.caption("Choose a subject to start a focus session.")
        cols = st.columns(2)
        for i, subject in enumerate(st.session_state.subjects):
            with cols[i%2]:
                st.markdown('<div class="fp-card">', unsafe_allow_html=True)
                st.markdown(f"### 📘 {subject}")
                count = sum(1 for s in st.session_state.sessions if s["subject"] == subject)
                mins = sum(s["minutes"] for s in st.session_state.sessions if s["subject"] == subject)
                st.caption(f"{count} sessions · {mins//60}h {mins%60:02d}m studied")
                if st.button("Start focus →", key=f"subject_{i}", use_container_width=True):
                    st.session_state.timer_subject = subject
                    st.session_state.timer_duration = st.session_state.focus_minutes
                    st.session_state.page = "Focus Timer"
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
        with st.expander("＋ Add a subject"):
            with st.form("add_subject"):
                new_subject = st.text_input("Subject name", placeholder="e.g. Operating Systems")
                add = st.form_submit_button("Add subject")
            if add:
                if new_subject.strip() and new_subject.strip() not in st.session_state.subjects:
                    st.session_state.subjects.append(new_subject.strip())
                    st.success(f"Added {new_subject.strip()}")
                    st.rerun()
                else: st.warning("Enter a new subject name.")
        st.subheader("Your weekly rhythm")
        st.bar_chart(df.set_index("Day")[["Hours studied"]], height=210)
        st.caption("Hours studied per day, based on completed sessions.")
        if st.button("View study routine →", use_container_width=True): go("Study Routine")
    with side:
        st.markdown('<div class="fp-card">', unsafe_allow_html=True)
        st.markdown("### 🌱 Today's goal")
        goal_hours = st.session_state.daily_goal // 60
        goal_rem = st.session_state.daily_goal % 60
        remaining = max(0, st.session_state.daily_goal - today_minutes)
        st.markdown(f'<div class="fp-big">{remaining//60}h {remaining%60:02d}m</div><p class="fp-muted">left to reach your goal</p>', unsafe_allow_html=True)
        st.progress(min(1, today_minutes/max(1,st.session_state.daily_goal)))
        if today_minutes == 0:
            goal_msg = f"Try one {st.session_state.focus_minutes}-minute session in {st.session_state.subjects[0] if st.session_state.subjects else 'your favourite subject'} to get started. Keep it small and doable."
        elif remaining > 0:
            goal_msg = f"You've already focused for {today_minutes} minutes. Try one more {min(st.session_state.focus_minutes, remaining)}-minute session, then take a proper break."
        else:
            goal_msg = "You reached your goal! You can stop here guilt-free or continue if you genuinely feel up to it."
        st.write(goal_msg)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('<div class="fp-card">', unsafe_allow_html=True)
        st.markdown("### 💬 Focus Buddy")
        st.caption("Supportive nudges, no guilt.")
        for msg in st.session_state.chat[-4:]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        prompt = st.chat_input("Ask for a study goal or encouragement…", key="dashboard_chat")
        if prompt:
            st.session_state.chat.append({"role":"user","content":prompt})
            low = prompt.lower()
            if "goal" in low or "plan" in low or "today" in low:
                reply = goal_msg
            elif "tired" in low or "overwhelmed" in low:
                reply = "Let's make this lighter. Try just two minutes: open the material and do one tiny task. You can decide whether to continue after that."
            elif "distract" in low or "phone" in low:
                reply = "Put your phone just out of reach, close one distracting tab, and try a 10-minute focus sprint. No need to be perfect."
            else:
                reply = f"Let's keep it manageable: choose one small task for {st.session_state.timer_subject}, focus for {min(10,st.session_state.focus_minutes)} minutes, then check in with yourself."
            st.session_state.chat.append({"role":"assistant","content":reply})
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('<div class="fp-card">', unsafe_allow_html=True)
        st.markdown("### 🏆 Reward shelf")
        st.markdown(f'<div class="fp-big">Level {st.session_state.level}</div><p class="fp-muted">{st.session_state.xp} XP earned</p>', unsafe_allow_html=True)
        st.progress((st.session_state.xp % 200)/200)
        st.caption(f"{200-(st.session_state.xp%200)} XP until next level")
        for name, unlocked, desc in achievements():
            st.write(("🏅 " if unlocked else "🔒 ") + name)
            if unlocked: st.caption(desc)
        st.markdown("</div>", unsafe_allow_html=True)

# ---------- Study Routine ----------
elif st.session_state.page == "Study Routine":
    header_kicker("BUILD A ROUTINE THAT FITS YOUR LIFE")
    st.title("Study Routine")
    st.markdown("Look at your progress, adjust your plan, and keep the next step realistic.")
    df = get_minutes_by_day(7)
    week_total = int(df["Minutes"].sum())
    today_min = int(df.iloc[-1]["Minutes"])
    prior_total = int(df.iloc[:-1]["Minutes"].sum())
    a,b,c = st.columns(3)
    a.metric("This week", f"{week_total/60:.1f} h")
    b.metric("Daily average", f"{week_total/7/60:.1f} h")
    change = ((week_total-prior_total)/prior_total*100) if prior_total else 0
    c.metric("Vs. previous 6 days", f"{change:+.0f}%", help="Compares today's-plus-week view with the prior six days; trend is descriptive, not a grade.")
    st.markdown("---")
    chart, settings = st.columns([1.5,1], gap="large")
    with chart:
        st.subheader("Hours studied per day")
        st.bar_chart(df.set_index("Day")[["Hours studied"]], height=300)
        st.subheader("Weekly progress")
        if prior_total > 0:
            st.write(f"You studied **{week_total/60:.1f} hours** over the last 7 days, compared with **{prior_total/60:.1f} hours** across the prior 6 days shown in this view.")
        else:
            st.info("Complete a few sessions to see your study trend. Every session counts; no streak pressure.")
        st.dataframe(df[["Day","Hours studied"]], use_container_width=True, hide_index=True)
    with settings:
        st.markdown('<div class="fp-card">', unsafe_allow_html=True)
        st.subheader("Edit your plan")
        with st.form("routine_settings"):
            daily_goal = st.number_input("Daily goal (minutes)", min_value=15, max_value=720, value=int(st.session_state.daily_goal), step=15)
            focus_length = st.number_input("Focus session length (minutes)", min_value=1, max_value=180, value=int(st.session_state.focus_minutes), step=5)
            break_length = st.number_input("Break length (minutes)", min_value=1, max_value=60, value=int(st.session_state.get("break_minutes",5)), step=1)
            saved = st.form_submit_button("Save routine", use_container_width=True)
        if saved:
            st.session_state.daily_goal = int(daily_goal)
            st.session_state.focus_minutes = int(focus_length)
            st.session_state.break_minutes = int(break_length)
            st.success("Your routine has been updated.")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('<div class="fp-card">', unsafe_allow_html=True)
        st.subheader("Your streak")
        st.markdown(f'<div class="fp-big">🔥 {st.session_state.streak} days</div>', unsafe_allow_html=True)
        st.caption("A streak is a gentle signal of consistency, not a measure of your worth.")
        st.markdown("</div>", unsafe_allow_html=True)
    if st.session_state.sessions:
        st.subheader("Recent focus sessions")
        sdf = pd.DataFrame(st.session_state.sessions[-10:][::-1])
        st.dataframe(sdf[["date","completed_at","subject","minutes","xp"]].rename(columns={"date":"Date","completed_at":"Time","subject":"Subject","minutes":"Minutes","xp":"XP"}), use_container_width=True, hide_index=True)
    else:
        st.info("Your completed sessions will appear here.")

# ---------- Focus Timer ----------
elif st.session_state.page == "Focus Timer":
    header_kicker("ONE THING AT A TIME")
    st.title("Focus Timer")
    st.markdown("You don't need a perfect session. You just need a place to begin.")
    subjects = st.session_state.subjects or ["General study"]
    if st.session_state.timer_subject not in subjects: st.session_state.timer_subject = subjects[0]
    selector, duration_col = st.columns([1.4,1])
    with selector:
        st.selectbox("Studying", subjects, key="timer_subject")
    with duration_col:
        st.number_input("Session length (minutes)", min_value=1, max_value=180, value=int(st.session_state.timer_duration), step=5, key="timer_duration")
    if st.session_state.timer_running and st.session_state.timer_end:
        seconds_left = max(0, int((st.session_state.timer_end - datetime.now()).total_seconds()))
    elif st.session_state.timer_paused_remaining is not None:
        seconds_left = st.session_state.timer_paused_remaining
    else:
        seconds_left = int(st.session_state.timer_duration)*60
    mm, ss = divmod(seconds_left, 60)
    left, center, right = st.columns([1,1.5,1])
    with center:
        st.markdown('<div class="fp-card" style="text-align:center;padding:36px 20px;">', unsafe_allow_html=True)
        st.markdown('<div class="fp-eyebrow">YOUR CURRENT SESSION</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-family:Space Grotesk;font-size:5rem;font-weight:700;letter-spacing:-.06em;color:#d4c4ff;">{mm:02d}:{ss:02d}</div>', unsafe_allow_html=True)
        st.markdown(f'<p class="fp-muted">📘 {st.session_state.timer_subject} · {st.session_state.timer_duration} minute session</p>', unsafe_allow_html=True)
        st.progress(min(1, max(0, 1-seconds_left/max(1,int(st.session_state.timer_duration)*60))))
        if st.session_state.timer_running:
            if seconds_left <= 0:
                award_session(st.session_state.timer_subject, int(st.session_state.timer_duration))
                st.success(f"Session complete! You earned {int(st.session_state.timer_duration)*2} XP. Take a breath before your next task.")
                st.rerun()
            else:
                st.info("Timer running. Refresh this page to update the displayed countdown; browser-side auto-refresh is not enabled.")
                if st.button("Pause session", use_container_width=True):
                    st.session_state.timer_paused_remaining = seconds_left
                    st.session_state.timer_running = False
                    st.session_state.timer_end = None
                    st.rerun()
        elif st.session_state.timer_paused_remaining is not None:
            if st.button("Resume session", use_container_width=True):
                st.session_state.timer_end = datetime.now()+timedelta(seconds=st.session_state.timer_paused_remaining)
                st.session_state.timer_running = True
                st.session_state.timer_paused_remaining = None
                st.rerun()
            if st.button("Reset timer", use_container_width=True):
                st.session_state.timer_paused_remaining = None
                st.session_state.timer_running = False
                st.rerun()
        else:
            if st.button("Start focus session", use_container_width=True):
                st.session_state.timer_end = datetime.now()+timedelta(minutes=int(st.session_state.timer_duration))
                st.session_state.timer_running = True
                st.session_state.timer_paused_remaining = None
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.caption("XP is awarded only when a session completes. Demo data is held in Streamlit session state and may reset when the session ends.")

# ---------- Fallback ----------
else:
    go("Dashboard")
