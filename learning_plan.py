import streamlit as st
from datetime import datetime

from database import (
    assessments_collection,
    learning_resources_collection,
    progress_collection
)


# =====================================================
# LEARNING RESOURCES
# =====================================================

LEARNING_RESOURCES = {

    "Python": {
        "topics": [
            "Python Basics",
            "Functions and Modules",
            "Lists, Tuples, Sets and Dictionaries",
            "Object-Oriented Programming",
            "File Handling",
            "NumPy and Pandas"
        ],
        "resources": [
            "Python Programming Fundamentals",
            "Python Practice Problems",
            "NumPy and Pandas Basics"
        ]
    },

    "SQL": {
        "topics": [
            "SELECT and WHERE",
            "ORDER BY and GROUP BY",
            "Aggregate Functions",
            "JOIN Operations",
            "Subqueries",
            "Database Design"
        ],
        "resources": [
            "SQL Fundamentals",
            "SQL Query Practice",
            "Advanced SQL and JOINs"
        ]
    },

    "DSA": {
        "topics": [
            "Arrays and Strings",
            "Linked Lists",
            "Stacks and Queues",
            "Searching",
            "Sorting",
            "Trees and Graphs",
            "Time and Space Complexity"
        ],
        "resources": [
            "DSA Fundamentals",
            "Searching and Sorting Practice",
            "Data Structures Practice Problems"
        ]
    },

    "Machine Learning": {
        "topics": [
            "Introduction to Machine Learning",
            "Supervised Learning",
            "Unsupervised Learning",
            "Regression",
            "Classification",
            "Clustering",
            "Model Evaluation"
        ],
        "resources": [
            "Machine Learning Fundamentals",
            "Scikit-learn Practice",
            "Machine Learning Projects"
        ]
    },

    "Problem Solving": {
        "topics": [
            "Understanding Programming Problems",
            "Algorithm Design",
            "Pseudocode",
            "Flowcharts",
            "Brute Force Techniques",
            "Divide and Conquer",
            "Debugging"
        ],
        "resources": [
            "Problem Solving Fundamentals",
            "Algorithm Practice",
            "Programming Challenges"
        ]
    }
}


# =====================================================
# DETERMINE LEARNING PRIORITY
# =====================================================

def get_priority(score):

    if score < 40:
        return "High"

    elif score < 60:
        return "Medium"

    elif score < 80:
        return "Low"

    else:
        return "Maintenance"


# =====================================================
# CALCULATE ESTIMATED WEEKS
# =====================================================

def calculate_weeks(score):

    if score < 40:
        return 4

    elif score < 60:
        return 3

    elif score < 80:
        return 2

    else:
        return 1


# =====================================================
# LEARNING PLAN PAGE
# =====================================================

def learning_plan_page():

    student = st.session_state.get("student")

    if not student:

        st.warning("Please login first.")
        return

    st.title("📚 Personalized Learning Plan")

    st.write(
        "Your learning plan is generated using your "
        "assessment performance and identified skill gaps."
    )

    st.info(
        "Skills with lower assessment scores receive "
        "higher learning priority."
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
    # GET SCORES
    # =================================================

    scores = latest_assessment.get(
        "scores",
        {}
    )

    # =================================================
    # SELECT CAREER
    # =================================================

    st.subheader("🎯 Select Your Target Career")

    career_options = [
        "AI / ML Engineer",
        "Data Scientist",
        "Data Analyst",
        "Python Developer",
        "Software Developer",
        "Backend Developer",
        "Machine Learning Developer",
        "Business / Data Intelligence Analyst"
    ]

    selected_career = st.selectbox(
        "Choose a career to build your learning plan:",
        career_options
    )

    st.divider()

    # =================================================
    # FIND SKILL GAPS
    # =================================================

    skill_plan = []

    for skill, score in scores.items():

        priority = get_priority(score)

        weeks = calculate_weeks(score)

        skill_plan.append({
            "skill": skill,
            "score": score,
            "priority": priority,
            "weeks": weeks
        })

    # Lowest scores first
    skill_plan.sort(
        key=lambda x: x["score"]
    )

    # =================================================
    # OVERALL LEARNING DURATION
    # =================================================

    total_weeks = max(
        item["weeks"]
        for item in skill_plan
    )

    st.subheader("🗓️ Estimated Learning Duration")

    st.metric(
        "Recommended Duration",
        f"{total_weeks} weeks"
    )

    st.caption(
        "The duration is an estimate based on your current "
        "assessment scores and is intended for planning."
    )

    st.divider()

    # =================================================
    # LEARNING PLAN
    # =================================================

    st.subheader(
        f"📖 Learning Roadmap for {selected_career}"
    )

    for item in skill_plan:

        skill = item["skill"]
        score = item["score"]
        priority = item["priority"]
        weeks = item["weeks"]

        resource_data = LEARNING_RESOURCES.get(
            skill
        )

        if not resource_data:
            continue

        with st.expander(
            f"{skill} — {score}% — {priority} Priority"
        ):

            st.write(
                f"**Current Score:** {score}%"
            )

            st.write(
                f"**Priority:** {priority}"
            )

            st.write(
                f"**Estimated Learning Time:** "
                f"{weeks} week(s)"
            )

            st.write("### 📌 Topics to Learn")

            for topic in resource_data["topics"]:

                st.write(
                    f"• {topic}"
                )

            st.write("### 🔗 Recommended Resources")

            for resource in resource_data["resources"]:

                st.write(
                    f"📘 {resource}"
                )

    st.divider()

    # =================================================
    # WEEKLY PLAN
    # =================================================

    st.subheader("📅 Suggested Weekly Routine")

    weekly_plan = [
        ("Monday", "Learn new concepts"),
        ("Tuesday", "Practice coding problems"),
        ("Wednesday", "Continue topic learning"),
        ("Thursday", "Solve practice questions"),
        ("Friday", "Build a small practical task"),
        ("Saturday", "Revise and take a mini test"),
        ("Sunday", "Review progress and weak areas")
    ]

    for day, activity in weekly_plan:

        st.write(
            f"**{day}:** {activity}"
        )

    st.divider()

    # =================================================
    # SAVE LEARNING RESOURCES
    # =================================================

    if st.button(
        "💾 Save My Learning Plan",
        use_container_width=True
    ):

        learning_plan_data = {

            "student_email": student["email"],

            "student_name": student["name"],

            "target_career": selected_career,

            "skills": skill_plan,

            "total_weeks": total_weeks,

            "created_at": datetime.now()
        }

        learning_resources_collection.insert_one(
            learning_plan_data
        )

        # ---------------------------------------------
        # Create initial progress document
        # ---------------------------------------------

        progress_data = {

            "student_email": student["email"],

            "student_name": student["name"],

            "target_career": selected_career,

            "skills": {
                item["skill"]: {
                    "initial_score": item["score"],
                    "current_score": item["score"],
                    "status": "Not Started"
                }
                for item in skill_plan
            },

            "overall_progress": 0,

            "created_at": datetime.now(),

            "updated_at": datetime.now()
        }

        progress_collection.insert_one(
            progress_data
        )

        st.success(
            "✅ Learning plan saved successfully!"
        )

    st.divider()

    # =================================================
    # NEXT STEP
    # =================================================

    st.subheader("📈 Track Your Progress")

    st.write(
        "Once you start learning, you can update your "
        "skill progress and monitor your improvement."
    )

    if st.button(
        "📈 View Progress",
        use_container_width=True
    ):

        st.session_state["page"] = "progress"
        st.rerun()

    # =================================================
    # NAVIGATION
    # =================================================

    if st.button(
        "🎯 Back to Career Guidance",
        use_container_width=True
    ):

        st.session_state["page"] = "career"
        st.rerun()

    if st.button(
        "⬅️ Back to Dashboard",
        use_container_width=True
    ):

        st.session_state["page"] = "dashboard"
        st.rerun()
