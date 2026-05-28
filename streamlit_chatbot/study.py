import streamlit as st
import time
import matplotlib.pyplot as plt
from datetime import datetime

# =====================================================
# PAGE SETUP
# =====================================================
st.set_page_config(
    page_title="Smart Academic Operating System",
    layout="wide"
)

st.title("🎓 Smart Academic Operating System")

# =====================================================
# SESSION STATE
# =====================================================
if "xp" not in st.session_state:
    st.session_state.xp = 0

if "tokens" not in st.session_state:
    st.session_state.tokens = 0

if "study_sessions" not in st.session_state:
    st.session_state.study_sessions = []

if "subject_history" not in st.session_state:
    st.session_state.subject_history = {}

# =====================================================
# XP SYSTEM
# =====================================================
def add_xp(x):
    st.session_state.xp += x

# =====================================================
# TOKEN SYSTEM
# =====================================================
def add_tokens(x):
    st.session_state.tokens += x

def spend_tokens(cost):
    if st.session_state.tokens >= cost:
        st.session_state.tokens -= cost
        return True
    return False

# =====================================================
# TIME FUNCTIONS
# =====================================================
def time_to_minutes(t):
    return t.hour * 60 + t.minute


def minutes_to_time(minutes):
    h = minutes // 60
    m = minutes % 60
    suffix = "AM"

    if h >= 12:
        suffix = "PM"

    display_h = h % 12
    if display_h == 0:
        display_h = 12

    return f"{display_h}:{m:02d} {suffix}"

# =====================================================
# SIDEBAR
# =====================================================
page = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Study Timer", "AI Weekly Scheduler", "Game Shop"]
)

# =====================================================
# DASHBOARD
# =====================================================
if page == "Dashboard":

    st.header("📊 Weekly Analytics Dashboard")

    total_minutes = sum(st.session_state.study_sessions)
    total_hours = round(total_minutes / 60, 1)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("⭐ XP", st.session_state.xp)

    with col2:
        st.metric("🪙 Tokens", st.session_state.tokens)

    with col3:
        st.metric("🧠 Sessions", len(st.session_state.study_sessions))

    productivity_score = min(100, len(st.session_state.study_sessions) * 10)

    st.subheader("🔥 Productivity Score")
    st.progress(productivity_score)

    st.write(f"Score: {productivity_score}/100")

    if total_hours >= 40:
        st.error("High burnout risk detected.")
    elif total_hours >= 25:
        st.warning("Moderate workload detected.")
    else:
        st.success("Healthy study balance detected.")

    if st.session_state.subject_history:

        st.subheader("📚 Most Studied Subjects")

        sorted_subjects = sorted(
            st.session_state.subject_history.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for subject, mins in sorted_subjects:
            st.write(f"📖 {subject} : {mins} mins")

    if st.session_state.study_sessions:

        st.subheader("📈 Study Analytics")

        plt.figure(figsize=(10, 4))
        plt.plot(st.session_state.study_sessions, marker="o")
        plt.title("Study Minutes Per Session")
        plt.xlabel("Session")
        plt.ylabel("Minutes")

        st.pyplot(plt)

# =====================================================
# STUDY TIMER
# =====================================================
elif page == "Study Timer":

    st.header("⏱ Smart Study Timer")

    study_mode = st.selectbox(
        "Select Study Mode",
        ["Deep Focus", "Balanced", "Light Revision"]
    )

    if study_mode == "Deep Focus":
        default_time = 90
        break_time = 20
    elif study_mode == "Balanced":
        default_time = 60
        break_time = 15
    else:
        default_time = 30
        break_time = 10

    st.info(f"Recommended Study: {default_time} mins | Break: {break_time} mins")

    mins = st.number_input("Study Minutes", 5, 300, default_time)
    subject = st.text_input("Subject Studied")

    if st.button("Start Study Session"):

        progress_bar = st.progress(0)
        status = st.empty()

        for i in range(mins * 60):

            progress_bar.progress(i / (mins * 60))
            status.info(f"📚 Studying... {mins*60 - i} sec remaining")
            time.sleep(1)

        st.success("✅ Study Session Complete!")

        st.session_state.study_sessions.append(mins)

        if subject:
            if subject not in st.session_state.subject_history:
                st.session_state.subject_history[subject] = 0

            st.session_state.subject_history[subject] += mins

        add_xp(30)
        add_tokens(mins // 10)

# =====================================================
# AI WEEKLY SCHEDULER (UPDATED)
# =====================================================
elif page == "AI Weekly Scheduler":

    st.header("📅 AI Adaptive Weekly Scheduler")

    subjects = st.text_input(
        "Subjects (comma separated)",
        "Math,Chemistry,Physics,English"
    )

    subject_list = [s.strip() for s in subjects.split(",")]

    priority_dict = {}

    for subject in subject_list:
        priority = st.selectbox(
            f"{subject} Priority",
            ["High", "Medium", "Low"],
            key=subject
        )
        priority_dict[subject] = priority

    energy_mode = st.selectbox(
        "When are you most productive?",
        ["Morning", "Afternoon", "Night"]
    )

    study_mode = st.selectbox(
        "Study Intensity",
        ["Deep Focus", "Balanced", "Light Revision"]
    )

    if study_mode == "Deep Focus":
        study_length = 90
        break_length = 20
    elif study_mode == "Balanced":
        study_length = 60
        break_length = 15
    else:
        study_length = 30
        break_length = 10

    weights = {"High": 3, "Medium": 2, "Low": 1}

    weighted_subjects = []
    for subject in subject_list:
        weighted_subjects += [subject] * weights[priority_dict[subject]]

    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    # =====================================================
    # NEW: STUDY SESSION FUNCTION INSIDE WEEKLY SCHEDULER
    # =====================================================

    def get_blocked_times(day, lecture_count, study_count):
        blocks = []

        # lectures
        for i in range(lecture_count):
            start = st.session_state.get(f"{day}ls{i}", None)
            end = st.session_state.get(f"{day}le{i}", None)

            if start and end:
                blocks.append((time_to_minutes(start), time_to_minutes(end)))

        # study sessions
        for i in range(study_count):
            start = st.session_state.get(f"{day}ss{i}", None)
            end = st.session_state.get(f"{day}se{i}", None)

            if start and end:
                blocks.append((time_to_minutes(start), time_to_minutes(end)))

        return blocks

    # =====================================================
    # DAY LOOP
    # =====================================================
    for day in days:

        st.markdown("---")

        with st.expander(f"📌 {day}"):

            lecture_count = st.number_input(
                f"{day} Lectures",
                0, 6, 2,
                key=f"lec_{day}"
            )

            study_count = st.number_input(
                f"{day} Study Sessions",
                0, 6, 1,
                key=f"study_{day}"
            )

            # lecture inputs
            for i in range(lecture_count):
                st.time_input(f"{day} Lecture {i+1} Start", key=f"{day}ls{i}")
                st.time_input(f"{day} Lecture {i+1} End", key=f"{day}le{i}")

            # study inputs (SAME FORMAT AS LECTURES)
            for i in range(study_count):
                st.time_input(f"{day} Study {i+1} Start", key=f"{day}ss{i}")
                st.time_input(f"{day} Study {i+1} End", key=f"{day}se{i}")

            if st.button(f"Generate {day} Schedule"):

                blocked_times = get_blocked_times(day, lecture_count, study_count)

                current_time = (
                    480 if energy_mode == "Morning"
                    else 780 if energy_mode == "Afternoon"
                    else 1140
                )

                study_blocks = []
                subject_index = 0

                while current_time < 1320:

                    for block in blocked_times:
                        if block[0] <= current_time < block[1]:
                            current_time = block[1] + 10
                            break

                    end_time = current_time + study_length

                    if end_time > 1320:
                        break

                    subject = weighted_subjects[subject_index % len(weighted_subjects)]

                    study_blocks.append((subject, current_time, end_time))

                    current_time = end_time + break_length
                    subject_index += 1

                st.success(f"✅ {day} Schedule Generated!")

                for s, start, end in study_blocks:
                    st.write(f"📖 {s} | {minutes_to_time(start)} - {minutes_to_time(end)}")

                add_xp(20)

# =====================================================
# GAME SHOP
# =====================================================
elif page == "Game Shop":

    st.header("🎮 Reward Shop")

    st.write(f"🪙 Your Tokens: {st.session_state.tokens}")

    shop_items = {
        "5 min break skip": 3,
        "1 extra XP boost (+50 XP)": 5,
        "Unlock dark mode theme (fake feature)": 10,
        "Study streak shield (protect streak)": 8
    }

    for item, cost in shop_items.items():

        col1, col2 = st.columns([3, 1])

        with col1:
            st.write(f"🎁 {item} — {cost} tokens")

        with col2:
            if st.button(f"Buy {item}", key=item):

                if spend_tokens(cost):
                    st.success(f"Purchased {item}!")
                    if "XP boost" in item:
                        add_xp(50)
                else:
                    st.error("Not enough tokens!")