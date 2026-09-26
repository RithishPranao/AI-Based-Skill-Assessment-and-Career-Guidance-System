import streamlit as st
from datetime import datetime

from database import progress_collection


# =====================================================
# GET LATEST PROGRESS
# =====================================================

def get_latest_progress(student_email):

    return progress_collection.find_one(
        {"student_email": student_email},
        sort=[("created_at", -1)]
    )


# =====================================================
# GET STATUS
# =====================================================

def get_status(initial_score, current_score):

    if current_score >= 80:
        return "Completed"

    elif current_score > initial_score:
        return "In Progress"

    else:
        return "Not Started"


# =====================================================
# PROGRESS PAGE
# =====================================================

def progress_page():

    student = st.session_state.get("student")

    if not student:

        st.warning("Please login first.")
        return

    st.title("📈 Progress Tracking")

    st.write(
        "Track how your skills improve after following "
        "your personalized learning plan."
    )

    st.info(
        "Update your current skill scores after practicing "
        "or completing learning activities."
    )

    st.divider()

    # =================================================
    # GET PROGRESS DOCUMENT
    # =================================================

    progress_data = get_latest_progress(
        student["email"]
    )

    if not progress_data:

        st.warning(
            "No learning progress found."
        )

        st.write(
            "Please save a learning plan first."
        )

        if st.button(
            "📚 Go to Learning Plan",
            use_container_width=True
        ):

            st.session_state["page"] = "learning"
            st.rerun()

        return

    # =================================================
    # BASIC INFORMATION
    # =================================================

    target_career = progress_data.get(
        "target_career",
        "Not selected"
    )

    skills = progress_data.get(
        "skills",
        {}
    )

    st.subheader("🎯 Target Career")

    st.write(
        f"**{target_career}**"
    )

    st.divider()

    # =================================================
    # UPDATE CURRENT SCORES
    # =================================================

    st.subheader("📝 Update Your Skill Progress")

    st.caption(
        "Enter your latest estimated skill scores "
        "from 0 to 100."
    )

    updated_skills = {}

    for skill, data in skills.items():

        initial_score = data.get(
            "initial_score",
            0
        )

        current_score = data.get(
            "current_score",
            initial_score
        )

        new_score = st.number_input(
            f"{skill}",
            min_value=0,
            max_value=100,
            value=int(current_score),
            step=5,
            key=f"progress_{skill}"
        )

        updated_skills[skill] = {
            "initial_score": initial_score,
            "current_score": new_score,
            "status": get_status(
                initial_score,
                new_score
            )
        }

    # =================================================
    # SAVE UPDATED PROGRESS
    # =================================================

    if st.button(
        "💾 Update Progress",
        use_container_width=True
    ):

        progress_collection.update_one(
            {
                "_id": progress_data["_id"]
            },
            {
                "$set": {
                    "skills": updated_skills,
                    "updated_at": datetime.now()
                }
            }
        )

        st.success(
            "✅ Your progress has been updated!"
        )

        st.rerun()

    st.divider()

    # =================================================
    # CALCULATE OVERALL PROGRESS
    # =================================================

    total_improvement = 0
    total_possible_improvement = 0

    for skill, data in updated_skills.items():

        initial_score = data["initial_score"]
        current_score = data["current_score"]

        improvement = current_score - initial_score

        total_improvement += max(
            improvement,
            0
        )

        total_possible_improvement += max(
            100 - initial_score,
            0
        )

    if total_possible_improvement > 0:

        overall_progress = round(
            (
                total_improvement
                / total_possible_improvement
            ) * 100
        )

    else:

        overall_progress = 100

    overall_progress = min(
        max(overall_progress, 0),
        100
    )

    # =================================================
    # OVERALL PROGRESS
    # =================================================

    st.subheader("📊 Overall Progress")

    st.metric(
        "Learning Progress",
        f"{overall_progress}%"
    )

    st.progress(
        overall_progress / 100
    )

    st.divider()

    # =================================================
    # SKILL-WISE PROGRESS
    # =================================================

    st.subheader("📚 Skill-wise Progress")

    for skill, data in updated_skills.items():

        initial_score = data["initial_score"]
        current_score = data["current_score"]
        status = data["status"]

        improvement = (
            current_score - initial_score
        )

        st.write(
            f"### {skill}"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Initial",
                f"{initial_score}%"
            )

        with col2:

            st.metric(
                "Current",
                f"{current_score}%"
            )

        with col3:

            if improvement >= 0:

                st.metric(
                    "Improvement",
                    f"+{improvement}%"
                )

            else:

                st.metric(
                    "Change",
                    f"{improvement}%"
                )

        st.progress(
            current_score / 100
        )

        st.write(
            f"**Status:** {status}"
        )

        st.divider()

    # =================================================
    # ACHIEVEMENT MESSAGE
    # =================================================

    completed_skills = sum(
        1
        for data in updated_skills.values()
        if data["status"] == "Completed"
    )

    total_skills = len(
        updated_skills
    )

    st.subheader("🏆 Achievement Summary")

    st.write(
        f"You have reached the Completed level "
        f"in **{completed_skills} out of "
        f"{total_skills} skills**."
    )

    if overall_progress == 0:

        st.info(
            "Start practicing your skill gaps "
            "and update your progress regularly."
        )

    elif overall_progress < 50:

        st.info(
            "Good start! Keep practicing consistently "
            "to improve your skills."
        )

    elif overall_progress < 80:

        st.success(
            "Great progress! Continue following "
            "your learning plan."
        )

    else:

        st.success(
            "🎉 Excellent progress! You are making "
            "strong improvements across your skills."
        )

    st.divider()

    # =================================================
    # NAVIGATION
    # =================================================

    if st.button(
        "📚 Back to Learning Plan",
        use_container_width=True
    ):

        st.session_state["page"] = "learning"
        st.rerun()

    if st.button(
        "⬅️ Back to Dashboard",
        use_container_width=True
    ):

        st.session_state["page"] = "dashboard"
        st.rerun()
