import streamlit as st
from datetime import datetime

from database import assessments_collection, career_results_collection


# =====================================================
# CAREER PROFILES
# =====================================================

CAREER_PROFILES = {

    "AI / ML Engineer": {
        "skills": {
            "Python": 85,
            "SQL": 60,
            "DSA": 70,
            "Machine Learning": 90,
            "Problem Solving": 85
        }
    },

    "Data Scientist": {
        "skills": {
            "Python": 80,
            "SQL": 80,
            "DSA": 55,
            "Machine Learning": 90,
            "Problem Solving": 85
        }
    },

    "Data Analyst": {
        "skills": {
            "Python": 60,
            "SQL": 90,
            "DSA": 40,
            "Machine Learning": 55,
            "Problem Solving": 70
        }
    },

    "Python Developer": {
        "skills": {
            "Python": 90,
            "SQL": 60,
            "DSA": 75,
            "Machine Learning": 40,
            "Problem Solving": 85
        }
    },

    "Software Developer": {
        "skills": {
            "Python": 70,
            "SQL": 60,
            "DSA": 90,
            "Machine Learning": 30,
            "Problem Solving": 90
        }
    },

    "Backend Developer": {
        "skills": {
            "Python": 80,
            "SQL": 85,
            "DSA": 70,
            "Machine Learning": 30,
            "Problem Solving": 85
        }
    },

    "Machine Learning Developer": {
        "skills": {
            "Python": 85,
            "SQL": 60,
            "DSA": 70,
            "Machine Learning": 95,
            "Problem Solving": 90
        }
    },

    "Business / Data Intelligence Analyst": {
        "skills": {
            "Python": 55,
            "SQL": 85,
            "DSA": 35,
            "Machine Learning": 50,
            "Problem Solving": 80
        }
    }
}


# =====================================================
# CALCULATE CAREER MATCH
# =====================================================

def calculate_match(student_scores, career_requirements):

    total_difference = 0
    number_of_skills = len(career_requirements)

    for skill, required_score in career_requirements.items():

        student_score = student_scores.get(skill, 0)

        difference = abs(
            student_score - required_score
        )

        total_difference += difference

    average_difference = (
        total_difference / number_of_skills
    )

    match_percentage = round(
        max(0, 100 - average_difference)
    )

    return match_percentage


# =====================================================
# FIND SKILL GAPS FOR CAREER
# =====================================================

def find_career_gaps(student_scores, career_requirements):

    gaps = []

    for skill, required_score in career_requirements.items():

        student_score = student_scores.get(skill, 0)

        if student_score < required_score:

            gap = required_score - student_score

            gaps.append({
                "skill": skill,
                "student_score": student_score,
                "required_score": required_score,
                "gap": gap
            })

    gaps.sort(
        key=lambda x: x["gap"],
        reverse=True
    )

    return gaps


# =====================================================
# CAREER MATCHING PAGE
# =====================================================

def career_matching_page():

    student = st.session_state.get("student")

    if not student:

        st.warning("Please login first.")
        return

    st.title("🎯 Career Guidance")

    st.write(
        "Your assessment skills are compared with "
        "skill requirements for different career paths."
    )

    st.info(
        "These matches are based on your current assessment "
        "performance and are intended to help you explore "
        "career paths."
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

        st.warning(
            "Please complete the skill assessment first."
        )

        if st.button(
            "📝 Take Assessment",
            use_container_width=True
        ):

            st.session_state["page"] = "assessment"
            st.rerun()

        return

    # =================================================
    # GET STUDENT SCORES
    # =================================================

    student_scores = latest_assessment.get(
        "scores",
        {}
    )

    overall_score = latest_assessment.get(
        "overall_score",
        0
    )

    st.subheader("📊 Your Current Skills")

    st.metric(
        "Overall Assessment Score",
        f"{overall_score}%"
    )

    for skill, score in student_scores.items():

        st.write(
            f"**{skill}: {score}%**"
        )

        st.progress(
            score / 100
        )

    st.divider()

    # =================================================
    # CALCULATE ALL CAREER MATCHES
    # =================================================

    career_matches = []

    for career, profile in CAREER_PROFILES.items():

        match_percentage = calculate_match(
            student_scores,
            profile["skills"]
        )

        gaps = find_career_gaps(
            student_scores,
            profile["skills"]
        )

        career_matches.append({
            "career": career,
            "match": match_percentage,
            "gaps": gaps
        })

    # Sort by match percentage
    career_matches.sort(
        key=lambda x: x["match"],
        reverse=True
    )

    # =================================================
    # DISPLAY CAREER MATCHES
    # =================================================

    st.subheader("🔎 Career Matches")

    st.write(
        "Explore how your current skills compare "
        "with each career profile."
    )

    for index, career_data in enumerate(
        career_matches
    ):

        career = career_data["career"]
        match = career_data["match"]
        gaps = career_data["gaps"]

        with st.expander(
            f"🎯 {career} — {match}% match"
        ):

            st.write(
                f"### {career}"
            )

            st.progress(
                match / 100
            )

            st.metric(
                "Skill Match",
                f"{match}%"
            )

            # -----------------------------------------
            # Career strengths
            # -----------------------------------------

            requirements = CAREER_PROFILES[
                career
            ]["skills"]

            strong_skills = []

            for skill, required_score in requirements.items():

                student_score = student_scores.get(
                    skill,
                    0
                )

                if student_score >= required_score:

                    strong_skills.append(skill)

            st.write("**✓ Skills meeting the requirement:**")

            if strong_skills:

                for skill in strong_skills:

                    st.success(
                        f"✓ {skill}"
                    )

            else:

                st.info(
                    "You currently do not meet the "
                    "target level for these skills."
                )

            # -----------------------------------------
            # Career skill gaps
            # -----------------------------------------

            st.write(
                "**⚠ Skills to improve:**"
            )

            if gaps:

                for gap in gaps:

                    st.warning(
                        f"{gap['skill']}: "
                        f"{gap['student_score']}% "
                        f"→ Target {gap['required_score']}%"
                    )

            else:

                st.success(
                    "🎉 Your current scores meet "
                    "all target skill levels."
                )

    st.divider()

    # =================================================
    # SAVE CAREER RESULTS
    # =================================================

    if st.button(
        "💾 Save Career Analysis",
        use_container_width=True
    ):

        career_result_data = {

            "student_email": student["email"],

            "student_name": student["name"],

            "student_scores": student_scores,

            "career_matches": [

                {
                    "career": item["career"],
                    "match_percentage": item["match"],
                    "skill_gaps": item["gaps"]
                }

                for item in career_matches
            ],

            "created_at": datetime.now()
        }

        career_results_collection.insert_one(
            career_result_data
        )

        st.success(
            "✅ Career analysis saved successfully!"
        )

    st.divider()

    # =================================================
    # NEXT STEP
    # =================================================

    st.subheader("📚 Next Step")

    st.write(
        "After exploring your career matches, "
        "you can generate a personalized learning plan "
        "based on your skill gaps."
    )

    if st.button(
        "📚 View Learning Plan",
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
