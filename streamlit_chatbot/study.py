import streamlit as st
import time
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# =====================================================
# PAGE SETUP
# =====================================================
st.set_page_config(
    page_title="Smart Study Scheduler",
    layout="wide"
)

st.title("📅 Smart Study Scheduler")

# =====================================================
# SESSION STATE
# =====================================================
if "xp" not in st.session_state:
    st.session_state.xp = 0

if "study_sessions" not in st.session_state:
    st.session_state.study_sessions = []

if "study_start" not in st.session_state:
    st.session_state.study_start = None

if "study_target" not in st.session_state:
    st.session_state.study_target = 0

if "music_links" not in st.session_state:
    st.session_state.music_links = []

# =====================================================
# XP SYSTEM
# =====================================================
def add_xp(x):
    st.session_state.xp += x

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
    [
        "Dashboard",
        "Study Timer",
        "Weekly Scheduler"
    ]
)

# =====================================================
# DASHBOARD
# =====================================================
if page == "Dashboard":

    st.header("📊 Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("⭐ XP", st.session_state.xp)

    with col2:
        st.metric(
            "📚 Study Sessions",
            len(st.session_state.study_sessions)
        )

    if st.session_state.study_sessions:

        st.subheader("📈 Study Progress")

        plt.figure(figsize=(8, 4))

        plt.plot(
            st.session_state.study_sessions,
            marker="o"
        )

        plt.title("Study Minutes Per Session")

        plt.xlabel("Session")

        plt.ylabel("Minutes")

        st.pyplot(plt)

# =====================================================
# STUDY TIMER + MUSIC
# =====================================================
elif page == "Study Timer":

    st.header("⏱ Study Timer")

    # ================= MUSIC =================
    st.subheader("🎵 Study Music")

    music_url = st.text_input(
        "Add YouTube or music link"
    )

    if st.button("Add Music"):

        if music_url:

            st.session_state.music_links.append(
                music_url
            )

            st.success("Music added!")

    # ================= PLAYLIST =================
    if st.session_state.music_links:

        st.subheader("🎧 Playlist")

        for i, link in enumerate(
            st.session_state.music_links
        ):

            st.write(f"{i+1}. {link}")

            if (
                "youtube.com" in link
                or
                "youtu.be" in link
            ):

                st.video(link)

    # ================= TIMER =================
    mins = st.number_input(
        "Study Minutes",
        5,
        300,
        25
    )

    if st.button("Start Study Session"):

        st.session_state.study_start = time.time()

        st.session_state.study_target = mins * 60

        st.success("Study session started!")

    if st.session_state.study_start:

        elapsed = (
            time.time()
            -
            st.session_state.study_start
        )

        remaining = (
            st.session_state.study_target
            -
            elapsed
        )

        if remaining > 0:

            st.info(
                f"📚 Studying... "
                f"{int(remaining)} seconds left"
            )

            time.sleep(1)

            st.rerun()

        else:

            st.success("✅ Session Complete!")

            st.session_state.study_sessions.append(mins)

            add_xp(30)

            st.session_state.study_start = None

# =====================================================
# WEEKLY SMART SCHEDULER
# =====================================================
elif page == "Weekly Scheduler":

    st.header("📅 AI Weekly Scheduler")

    st.write(
        "Insert your lecture sessions and rest time. "
        "The AI will automatically arrange revision sessions."
    )

    # ================= SUBJECTS =================
    subjects = st.text_input(
        "Subjects (comma separated)",
        "Math,Chemistry,Physics,English"
    )

    subject_list = [
        s.strip()
        for s in subjects.split(",")
    ]

    # ================= PREFERENCE =================
    st.subheader("🧠 Study Preference")

    preferred_study_length = st.selectbox(
        "Preferred Study Session Length",
        [30, 45, 60, 90, 120]
    )

    # ================= DAYS =================
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    for day in days:

        st.markdown("---")

        st.subheader(f"📌 {day}")

        # ================= LECTURE =================
        st.write("🎓 Lecture Session")

        lec_start = st.time_input(
            f"{day} Lecture Start",
            value=datetime.strptime(
                "10:00",
                "%H:%M"
            ).time(),
            key=f"lec_start_{day}"
        )

        lec_end = st.time_input(
            f"{day} Lecture End",
            value=datetime.strptime(
                "12:00",
                "%H:%M"
            ).time(),
            key=f"lec_end_{day}"
        )

        # ================= REST =================
        st.write("😴 Rest Session")

        rest_start = st.time_input(
            f"{day} Rest Start",
            value=datetime.strptime(
                "13:30",
                "%H:%M"
            ).time(),
            key=f"rest_start_{day}"
        )

        rest_end = st.time_input(
            f"{day} Rest End",
            value=datetime.strptime(
                "14:30",
                "%H:%M"
            ).time(),
            key=f"rest_end_{day}"
        )

        # ================= GENERATE =================
        if st.button(
            f"Generate {day} Schedule"
        ):

            lecture_start_mins = time_to_minutes(
                lec_start
            )

            lecture_end_mins = time_to_minutes(
                lec_end
            )

            rest_start_mins = time_to_minutes(
                rest_start
            )

            rest_end_mins = time_to_minutes(
                rest_end
            )

            study_blocks = []

            current_time = lecture_end_mins + 30

            subject_index = 0

            while (
                current_time
                +
                preferred_study_length
                <=
                1320
            ):

                # avoid rest session
                if (
                    current_time
                    >=
                    rest_start_mins
                    and
                    current_time
                    <
                    rest_end_mins
                ):

                    current_time = rest_end_mins

                    continue

                end_time = (
                    current_time
                    +
                    preferred_study_length
                )

                subject = subject_list[
                    subject_index
                    %
                    len(subject_list)
                ]

                study_blocks.append(
                    (
                        subject,
                        current_time,
                        end_time
                    )
                )

                current_time = (
                    end_time
                    +
                    15
                )

                subject_index += 1

            # ================= DISPLAY =================
            st.success(
                f"✅ {day} Schedule Generated!"
            )

            st.write(
                f"🎓 Lecture: "
                f"{minutes_to_time(lecture_start_mins)}"
                f" - "
                f"{minutes_to_time(lecture_end_mins)}"
            )

            st.write(
                f"😴 Rest: "
                f"{minutes_to_time(rest_start_mins)}"
                f" - "
                f"{minutes_to_time(rest_end_mins)}"
            )

            st.subheader("📚 AI Revision Schedule")

            for block in study_blocks:

                st.write(
                    f"📖 {block[0]} | "
                    f"{minutes_to_time(block[1])}"
                    f" - "
                    f"{minutes_to_time(block[2])}"
                )

            add_xp(20)