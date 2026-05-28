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

if "study_sessions" not in st.session_state:
    st.session_state.study_sessions = []

if "subject_history" not in st.session_state:
    st.session_state.subject_history = {}

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
        "AI Weekly Scheduler"
    ]
)

# =====================================================
# DASHBOARD
# =====================================================
if page == "Dashboard":

    st.header("📊 Weekly Analytics Dashboard")

    total_minutes = sum(
        st.session_state.study_sessions
    )

    total_hours = round(
        total_minutes / 60,
        1
    )

    # ================= METRICS =================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "⭐ XP",
            st.session_state.xp
        )

    with col2:
        st.metric(
            "📚 Total Study Hours",
            total_hours
        )

    with col3:
        st.metric(
            "🧠 Sessions",
            len(st.session_state.study_sessions)
        )

    # ================= PRODUCTIVITY SCORE =================
    productivity_score = min(
        100,
        len(st.session_state.study_sessions) * 10
    )

    st.subheader("🔥 Productivity Score")

    st.progress(productivity_score)

    st.write(
        f"Score: {productivity_score}/100"
    )

    # ================= BURNOUT DETECTION =================
    st.subheader("⚠ Burnout Detection")

    if total_hours >= 40:

        st.error(
            "High burnout risk detected."
        )

    elif total_hours >= 25:

        st.warning(
            "Moderate workload detected."
        )

    else:

        st.success(
            "Healthy study balance detected."
        )

    # ================= STUDY GRAPH =================
    if st.session_state.study_sessions:

        st.subheader("📈 Study Analytics")

        plt.figure(figsize=(10, 4))

        plt.plot(
            st.session_state.study_sessions,
            marker="o"
        )

        plt.title(
            "Study Minutes Per Session"
        )

        plt.xlabel("Session")

        plt.ylabel("Minutes")

        st.pyplot(plt)

# =====================================================
# STUDY TIMER + SMART STUDY MODE
# =====================================================
elif page == "Study Timer":

    st.header("⏱ Smart Study Timer")

    # ================= STUDY MODE =================
    st.subheader("🧠 Smart Study Mode")

    study_mode = st.selectbox(
        "Select Study Mode",
        [
            "Deep Focus",
            "Balanced",
            "Light Revision"
        ]
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

    st.info(
        f"Recommended Study: "
        f"{default_time} mins | "
        f"Break: {break_time} mins"
    )

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
        default_time
    )

    subject = st.text_input(
        "Subject Studied"
    )

    if st.button("Start Study Session"):

        progress_bar = st.progress(0)

        status = st.empty()

        for i in range(mins * 60):

            remaining = (
                mins * 60
                -
                i
            )

            progress = (
                i
                /
                (mins * 60)
            )

            progress_bar.progress(progress)

            status.info(
                f"📚 Studying... "
                f"{remaining} sec remaining"
            )

            time.sleep(1)

        st.success(
            "✅ Study Session Complete!"
        )

        st.session_state.study_sessions.append(
            mins
        )

        if subject:

            if (
                subject
                not in
                st.session_state.subject_history
            ):

                st.session_state.subject_history[
                    subject
                ] = 0

            st.session_state.subject_history[
                subject
            ] += mins

        add_xp(30)

# =====================================================
# AI WEEKLY SCHEDULER
# =====================================================
elif page == "AI Weekly Scheduler":

    st.header("📅 AI Adaptive Weekly Scheduler")

    st.write(
        "Insert lectures, rest periods, and preferences. "
        "The AI will intelligently organise revision sessions."
    )

    # =====================================================
    # SUBJECTS
    # =====================================================
    subjects = st.text_input(
        "Subjects (comma separated)",
        "Math,Chemistry,Physics,English"
    )

    subject_list = [
        s.strip()
        for s in subjects.split(",")
    ]

    # =====================================================
    # PRIORITY ENGINE
    # =====================================================
    st.subheader("🔥 Subject Priority")

    priority_dict = {}

    for subject in subject_list:

        priority = st.selectbox(
            f"{subject} Priority",
            [
                "High",
                "Medium",
                "Low"
            ],
            key=subject
        )

        priority_dict[subject] = priority

    # =====================================================
    # ENERGY MODE
    # =====================================================
    st.subheader("🧠 Energy-Based Scheduling")

    energy_mode = st.selectbox(
        "When are you most productive?",
        [
            "Morning",
            "Afternoon",
            "Night"
        ]
    )

    # =====================================================
    # STUDY MODE
    # =====================================================
    st.subheader("📚 Smart Study Mode")

    study_mode = st.selectbox(
        "Study Intensity",
        [
            "Deep Focus",
            "Balanced",
            "Light Revision"
        ]
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

    # =====================================================
    # PRIORITY WEIGHTS
    # =====================================================
    weights = {
        "High": 3,
        "Medium": 2,
        "Low": 1
    }

    weighted_subjects = []

    for subject in subject_list:

        repeat = weights[
            priority_dict[subject]
        ]

        for i in range(repeat):

            weighted_subjects.append(
                subject
            )

    # =====================================================
    # DAYS
    # =====================================================
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    # =====================================================
    # DAILY INPUTS
    # =====================================================
    for day in days:

        st.markdown("---")

        with st.expander(f"📌 {day}"):

            # ================= LECTURES =================
            lecture_count = st.number_input(
                f"{day} Number of Lectures",
                0,
                6,
                2,
                key=f"lecture_count_{day}"
            )

            blocked_times = []

            for i in range(lecture_count):

                st.write(
                    f"🎓 Lecture {i+1}"
                )

                lec_start = st.time_input(
                    f"{day} Lecture {i+1} Start",
                    key=f"{day}_lec_start_{i}"
                )

                lec_end = st.time_input(
                    f"{day} Lecture {i+1} End",
                    key=f"{day}_lec_end_{i}"
                )

                blocked_times.append(
                    (
                        time_to_minutes(
                            lec_start
                        ),
                        time_to_minutes(
                            lec_end
                        ),
                        "Lecture"
                    )
                )

            # ================= REST =================
            rest_count = st.number_input(
                f"{day} Number of Rest Sessions",
                0,
                4,
                1,
                key=f"rest_count_{day}"
            )

            for i in range(rest_count):

                st.write(
                    f"😴 Rest {i+1}"
                )

                rest_start = st.time_input(
                    f"{day} Rest {i+1} Start",
                    key=f"{day}_rest_start_{i}"
                )

                rest_end = st.time_input(
                    f"{day} Rest {i+1} End",
                    key=f"{day}_rest_end_{i}"
                )

                blocked_times.append(
                    (
                        time_to_minutes(
                            rest_start
                        ),
                        time_to_minutes(
                            rest_end
                        ),
                        "Rest"
                    )
                )

            # =====================================================
            # GENERATE SCHEDULE
            # =====================================================
            if st.button(
                f"Generate {day} Schedule"
            ):

                blocked_times.sort()

                study_blocks = []

                # =====================================================
                # ENERGY START TIME
                # =====================================================
                if energy_mode == "Morning":

                    current_time = 480

                elif energy_mode == "Afternoon":

                    current_time = 780

                else:

                    current_time = 1140

                subject_index = 0

                while current_time < 1320:

                    blocked = False

                    for block in blocked_times:

                        block_start = block[0]
                        block_end = block[1]

                        if (
                            current_time
                            >=
                            block_start
                            and
                            current_time
                            <
                            block_end
                        ):

                            current_time = (
                                block_end
                                +
                                15
                            )

                            blocked = True

                            break

                    if blocked:

                        continue

                    end_time = (
                        current_time
                        +
                        study_length
                    )

                    if end_time > 1320:

                        break

                    subject = weighted_subjects[
                        subject_index
                        %
                        len(weighted_subjects)
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
                        break_length
                    )

                    subject_index += 1

                # =====================================================
                # DISPLAY
                # =====================================================
                st.success(
                    f"✅ {day} Schedule Generated!"
                )

                st.subheader(
                    "📚 AI Revision Schedule"
                )

                for block in study_blocks:

                    st.write(
                        f"📖 {block[0]} | "
                        f"{minutes_to_time(block[1])}"
                        f" - "
                        f"{minutes_to_time(block[2])}"
                    )

                # =====================================================
                # TIMELINE CHART
                # =====================================================
                st.subheader(
                    "📊 Daily Timeline"
                )

                fig, ax = plt.subplots(
                    figsize=(10, 2)
                )

                y_pos = 1

                for block in study_blocks:

                    start = block[1]
                    duration = (
                        block[2]
                        -
                        block[1]
                    )

                    ax.barh(
                        y_pos,
                        duration,
                        left=start
                    )

                ax.set_xlim(0, 1440)

                ax.set_xlabel(
                    "Minutes in Day"
                )

                ax.set_yticks([])

                st.pyplot(fig)

                add_xp(20)