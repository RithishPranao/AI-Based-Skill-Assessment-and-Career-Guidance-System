import streamlit as st
from database import assessments_collection


# =====================================================
# SKILL LEVEL
# =====================================================

def get_skill_level(score):

    if score >= 80:
        return "Strong", "You have a strong understanding of this skill."

    elif score >= 60:
        return "Good", "You have a good understanding, but there is room for improvement."

    elif score >= 40:
        return "Needs Improvement", "You understand the basics but need more practice."

    else:
        return "Skill Gap", "This skill needs more learning and practice."


# =====================================================
# SKILL ANALYSIS PAGE
# =====================================================

def skill_analysis_page():

    student = st.session_state.get("student")

    if not student:
        st.warning("Please login first.")
        return

    st.title("📊 Skill Gap Analysis")

    st.write(
        "This page analyzes your assessment performance "
        "and identifies your strengths and areas that need improvement."
    )

    st.divider()

    # =================================================
    # GET LATEST ASSESSMENT
    # =================================================

    latest_assessment = assessments_collection.find_one(
        {"student_email": student["email"]},
        sort=[("completed_at", -1)]
    )

    if not latest_assessment:

        st.info(
            "You have not completed a skill assessment yet."
        )

        if st.button(
            "📝 Take Assessment",
            use_container_width=True
        ):

            st.session_state["page"] = "assessment"
            st.rerun()

        return

    # =================================================
    # GET SCORES
    # =================================================

    scores = latest_assessment.get("scores", {})
    overall_score = latest_assessment.get("overall_score", 0)

    # =================================================
    # OVERALL SCORE
    # =================================================

    st.subheader("🎯 Overall Performance")

    st.metric(
        "Overall Skill Score",
        f"{overall_score}%"
    )

    st.progress(
        overall_score / 100
    )

    st.divider()

    # =================================================
    # INDIVIDUAL SKILLS
    # =================================================

    st.subheader("📚 Skill-wise Performance")

    for skill, score in scores.items():

        level, description = get_skill_level(score)

        st.write(
            f"### {skill}"
        )

        st.progress(
            score / 100
        )

        st.write(
            f"**Score:** {score}%"
        )

        st.write(
            f"**Level:** {level}"
        )

        st.caption(
            description
        )

        st.divider()

    # =================================================
    # FIND STRENGTHS AND GAPS
    # =================================================

    strong_skills = []
    improvement_skills = []
    gap_skills = []

    for skill, score in scores.items():

        if score >= 80:

            strong_skills.append(skill)

        elif score >= 40:

            improvement_skills.append(skill)

        else:

            gap_skills.append(skill)

    # =================================================
    # STRENGTHS
    # =================================================

    st.subheader("💪 Your Strengths")

    if strong_skills:

        for skill in strong_skills:

            st.success(
                f"✓ {skill}"
            )

    else:

        st.info(
            "No skill has reached the Strong level yet."
        )

    # =================================================
    # NEEDS IMPROVEMENT
    # =================================================

    st.subheader("📈 Skills to Improve")

    if improvement_skills:

        for skill in improvement_skills:

            st.warning(
                f"⚠ {skill}"
            )

    else:

        st.info(
            "No skills currently fall into this category."
        )

    # =================================================
    # SKILL GAPS
    # =================================================

    st.subheader("🚨 Skill Gaps")

    if gap_skills:

        for skill in gap_skills:

            st.error(
                f"❌ {skill}"
            )

    else:

        st.success(
            "🎉 No major skill gaps detected!"
        )

    st.divider()

    # =================================================
    # NEXT STEP
    # =================================================

    st.subheader("🚀 What's Next?")

    st.write(
        "Your skill analysis is complete. "
        "The next step is to match your skills with suitable career paths."
    )

    if st.button(
        "🎯 Explore Career Matches",
        use_container_width=True
    ):

        st.session_state["page"] = "career"

        st.rerun()

    # =================================================
    # BACK TO DASHBOARD
    # =================================================

    if st.button(
        "⬅️ Back to Dashboard",
        use_container_width=True
    ):

        st.session_state["page"] = "dashboard"

        st.rerun()
