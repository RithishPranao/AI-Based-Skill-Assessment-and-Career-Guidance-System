import streamlit as st
import hashlib
import importlib
import re
from datetime import datetime

from database import (
    students_collection,
    parents_collection,
    assessments_collection,
    career_results_collection,
    learning_resources_collection,
    progress_collection,
)

from assessment import (
    skill_assessment_page,
    assessment_instructions_page,
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="SkillPath AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# HTML HELPER
# =========================================================

def html(content):
    st.html(content)


# =========================================================
# GLOBAL CSS
# =========================================================

st.html(
    """
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    html, body, [class*="css"] {
        font-family: "Inter", sans-serif;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 5% 5%,
                rgba(99,102,241,.10),
                transparent 25%
            ),
            radial-gradient(
                circle at 95% 10%,
                rgba(6,182,212,.10),
                transparent 25%
            ),
            #f8fafc;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    #MainMenu,
    footer {
        visibility: hidden;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* SIDEBAR */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0f172a,
                #111827
            );
    }

    section[data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    section[data-testid="stSidebar"]
    .stButton > button {
        background: transparent !important;
        border: 1px solid transparent !important;
        color: #e2e8f0 !important;
        text-align: left !important;
    }

    section[data-testid="stSidebar"]
    .stButton > button:hover {
        background: rgba(255,255,255,.08) !important;
    }

    /* BRAND */

    .brand {
        text-align: center;
        padding: 10px 0 18px;
    }

    .brand-icon {
        width: 58px;
        height: 58px;
        margin: 0 auto 10px;
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        background:
            linear-gradient(
                135deg,
                #6366f1,
                #06b6d4
            );
        font-size: 28px;
    }

    .brand-name {
        font-size: 21px;
        font-weight: 800;
        color: white;
    }

    .brand-subtitle {
        color: #94a3b8 !important;
        font-size: 11px;
        margin-top: 4px;
    }

    /* LOGIN */

    .hero {
        padding: 45px 20px 30px 10px;
    }

    .badge {
        display: inline-block;
        padding: 8px 14px;
        border-radius: 999px;
        background: #eef2ff;
        color: #4f46e5;
        font-size: 12px;
        font-weight: 800;
        margin-bottom: 18px;
    }

    .hero-title {
        font-size: clamp(40px, 5vw, 64px);
        line-height: 1.03;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 20px;
    }

    .hero-title span {
        background:
            linear-gradient(
                90deg,
                #4f46e5,
                #0891b2
            );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-description {
        max-width: 650px;
        color: #64748b;
        font-size: 16px;
        line-height: 1.75;
        margin-bottom: 25px;
    }

    .feature-row {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }

    .feature-chip {
        display: inline-block;
        padding: 10px 13px;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        background: white;
        color: #334155;
        font-size: 12px;
        font-weight: 700;
    }

    .login-heading {
        color: #0f172a;
        font-size: 28px;
        font-weight: 800;
    }

    .login-description {
        color: #64748b;
        font-size: 13px;
        margin-bottom: 18px;
    }

    /* HERO */

    .dashboard-hero,
    .parent-hero {
        padding: 32px;
        border-radius: 26px;
        color: white;
        background:
            linear-gradient(
                135deg,
                #312e81,
                #4f46e5 55%,
                #0891b2
            );
        box-shadow:
            0 20px 45px
            rgba(79,70,229,.18);
        margin-bottom: 25px;
    }

    .dashboard-title,
    .parent-title {
        font-size: 31px;
        font-weight: 800;
    }

    .dashboard-subtitle,
    .parent-subtitle {
        color: rgba(255,255,255,.82);
        font-size: 14px;
        margin-top: 6px;
    }

    .section-title,
    .parent-section {
        color: #0f172a;
        font-size: 22px;
        font-weight: 800;
        margin: 28px 0 15px;
    }

    .card-title {
        color: #0f172a;
        font-size: 18px;
        font-weight: 800;
    }

    .card-description {
        color: #64748b;
        font-size: 13px;
        line-height: 1.6;
    }

    .score {
        color: #4f46e5;
        font-size: 46px;
        font-weight: 800;
        margin-top: 10px;
    }

    .score-marks {
        color: #64748b;
        font-size: 14px;
        font-weight: 600;
    }

    .profile-name {
        color: #0f172a;
        font-size: 21px;
        font-weight: 800;
    }

    .profile-detail {
        color: #64748b;
        font-size: 12px;
        margin-top: 5px;
    }

    .icon {
        width: 48px;
        height: 48px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #eef2ff;
        font-size: 23px;
        margin-bottom: 14px;
    }

    /* CARDS */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 20px !important;
        border-color: #e2e8f0 !important;
        background: rgba(255,255,255,.95);
        box-shadow:
            0 8px 25px
            rgba(15,23,42,.05);
    }

    /* BUTTONS */

    .stButton > button {
        min-height: 44px;
        border-radius: 12px !important;
        font-weight: 700 !important;
        border: 1px solid #e2e8f0 !important;
        transition: all .2s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        border-color: #6366f1 !important;
        color: #4f46e5 !important;
    }

    button[kind="primary"] {
        background:
            linear-gradient(
                135deg,
                #4f46e5,
                #06b6d4
            ) !important;
        color: white !important;
        border: none !important;
    }

    /* INPUTS */

    .stTextInput input,
    div[data-baseweb="select"] > div {
        border-radius: 12px !important;
        border: 1px solid #cbd5e1 !important;
        background: white !important;
    }

    /* METRICS */

    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 14px;
    }

    [data-testid="stMetricValue"] {
        color: #4f46e5 !important;
        font-weight: 800;
    }

    .status-success {
        padding: 12px 15px;
        border-radius: 12px;
        background: #ecfdf5;
        color: #047857;
        border: 1px solid #a7f3d0;
        font-size: 13px;
        font-weight: 700;
    }

    .status-empty {
        padding: 18px;
        border-radius: 14px;
        background: #f8fafc;
        color: #64748b;
        border: 1px solid #e2e8f0;
        font-size: 14px;
    }

    .history-card {
        padding: 17px;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        margin-bottom: 10px;
        background: white;
    }

    .data-card {
        padding: 20px;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        margin-bottom: 12px;
        background: white;
    }

    .data-title {
        color: #0f172a;
        font-size: 17px;
        font-weight: 800;
        margin-bottom: 7px;
    }

    .data-text {
        color: #64748b;
        font-size: 13px;
        line-height: 1.6;
    }

    .small-label {
        color: #64748b;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .5px;
    }

    .small-value {
        color: #0f172a;
        font-size: 14px;
        font-weight: 700;
        margin-top: 3px;
    }

    .parent-progress-bar {
        width: 100%;
        height: 12px;
        border-radius: 999px;
        background: #e2e8f0;
        overflow: hidden;
        margin: 8px 0 12px;
    }

    .parent-progress-fill {
        height: 100%;
        border-radius: 999px;
        background:
            linear-gradient(
                90deg,
                #4f46e5,
                #06b6d4
            );
    }

    </style>
    """
)


# =========================================================
# PASSWORD HASH
# =========================================================

def hash_password(password):
    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# =========================================================
# EMAIL VALIDATION
# =========================================================

def is_valid_email(email):
    """
    Checks whether the entered value has a valid
    basic email format.

    Examples:
    example@gmail.com       -> Valid
    student@college.edu     -> Valid
    studentgmail.com        -> Invalid
    student@                -> Invalid
    student@gmail           -> Invalid
    """

    if not email:
        return False

    email = email.strip()

    pattern = (
        r"^[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+"
        r"\.[A-Za-z]{2,}$"
    )

    return bool(
        re.match(
            pattern,
            email
        )
    )


# =========================================================
# NAVIGATION
# =========================================================

def go_to(page):
    st.session_state["page"] = page
    st.rerun()


def logout():
    st.session_state.clear()
    st.rerun()


def open_assessment_instructions():
    st.session_state["page"] = "assessment_intro"
    st.rerun()


# =========================================================
# MODULE LOADER
# =========================================================

def load_page_function(
    module_name,
    function_names
):

    try:
        module = importlib.import_module(
            module_name
        )
    except Exception:
        return None

    for function_name in function_names:

        function = getattr(
            module,
            function_name,
            None
        )

        if callable(function):
            return function

    return None


# =========================================================
# DATABASE HELPERS
# =========================================================

def load_latest_assessment(student_email):

    if not student_email:
        return None

    try:

        return assessments_collection.find_one(
            {
                "student_email":
                    student_email
            },
            sort=[
                (
                    "completed_at",
                    -1
                )
            ]
        )

    except Exception:

        return None


def load_assessment_history(student_email):

    if not student_email:
        return []

    try:

        return list(
            assessments_collection.find(
                {
                    "student_email":
                        student_email
                }
            ).sort(
                "completed_at",
                -1
            )
        )

    except Exception:

        return []


def load_career_results(student_email):

    if not student_email:
        return []

    try:

        return list(
            career_results_collection.find(
                {
                    "student_email":
                        student_email
                }
            ).sort(
                "created_at",
                -1
            )
        )

    except Exception:

        return []


def load_learning_resources(student_email):

    if not student_email:
        return []

    try:

        return list(
            learning_resources_collection.find(
                {
                    "student_email":
                        student_email
                }
            ).sort(
                "created_at",
                -1
            )
        )

    except Exception:

        return []


def load_progress_records(student_email):

    if not student_email:
        return []

    try:

        return list(
            progress_collection.find(
                {
                    "student_email":
                        student_email
                }
            ).sort(
                "_id",
                -1
            )
        )

    except Exception:

        return []


# =========================================================
# GENERAL HELPERS
# =========================================================

def first_value(
    document,
    keys,
    default="-"
):

    if not isinstance(
        document,
        dict
    ):
        return default

    for key in keys:

        if key in document:

            value = document.get(
                key
            )

            if (
                value is not None
                and value != ""
            ):
                return value

    return default


def format_date(value):

    if not value:
        return "-"

    if isinstance(
        value,
        datetime
    ):

        return value.strftime(
            "%d %b %Y, %I:%M %p"
        )

    return str(value)


def safe_percentage(value):

    try:

        value = float(value)

        if value <= 1:
            value *= 100

        return max(
            0,
            min(
                100,
                value
            )
        )

    except Exception:

        return 0


# =========================================================
# STUDENT SCORE
# =========================================================

def get_student_score(student_email):

    latest = load_latest_assessment(
        student_email
    )

    if not latest:

        return (
            {},
            {},
            0,
            0,
            None
        )

    scores = latest.get(
        "scores",
        {}
    )

    marks = latest.get(
        "skill_marks",
        {}
    )

    percentage = latest.get(
        "overall_score",
        latest.get(
            "overall_percentage",
            0
        )
    )

    overall_marks = latest.get(
        "overall_marks",
        latest.get(
            "obtained_marks",
            0
        )
    )

    return (
        scores,
        marks,
        safe_percentage(
            percentage
        ),
        overall_marks,
        latest
    )


# =========================================================
# STUDENT SIDEBAR
# =========================================================

def show_student_sidebar():

    student = st.session_state.get(
        "student",
        {}
    )

    name = student.get(
        "name",
        "Student"
    )

    with st.sidebar:

        html(
            """
            <div class="brand">

                <div class="brand-icon">
                    🎓
                </div>

                <div class="brand-name">
                    SkillPath AI
                </div>

                <div class="brand-subtitle">
                    Skill Assessment & Career Guidance
                </div>

            </div>
            """
        )

        st.divider()

        st.markdown(
            f"### 👋 {name}"
        )

        st.caption(
            student.get(
                "branch",
                "Student"
            )
        )

        st.divider()

        navigation = [

            (
                "🏠 Dashboard",
                "dashboard"
            ),

            (
                "📝 Skill Assessment",
                "assessment"
            ),

            (
                "🎯 Career Guidance",
                "career"
            ),

            (
                "📊 Skill Analysis",
                "skills"
            ),

            (
                "📚 Learning Plan",
                "learning"
            ),

            (
                "📈 Progress",
                "progress"
            ),

        ]

        for label, page in navigation:

            if st.button(
                label,
                key=f"student_nav_{page}",
                use_container_width=True
            ):

                if page == "assessment":

                    open_assessment_instructions()

                else:

                    go_to(page)

        st.divider()

        if st.button(
            "🚪 Logout",
            key="student_logout",
            use_container_width=True
        ):

            logout()


# =========================================================
# PARENT SIDEBAR
# =========================================================

def show_parent_sidebar():

    parent = st.session_state.get(
        "parent",
        {}
    )

    parent_name = parent.get(
        "name",
        "Parent"
    )

    with st.sidebar:

        html(
            """
            <div class="brand">

                <div class="brand-icon">
                    🎓
                </div>

                <div class="brand-name">
                    SkillPath AI
                </div>

                <div class="brand-subtitle">
                    Parent Portal
                </div>

            </div>
            """
        )

        st.divider()

        st.markdown(
            f"### 👋 {parent_name}"
        )

        st.caption(
            "Parent Account"
        )

        st.divider()

        navigation = [

            (
                "🏠 Dashboard",
                "parent_dashboard"
            ),

            (
                "👨‍🎓 Student Profile",
                "parent_student"
            ),

            (
                "📊 Assessment",
                "parent_assessment"
            ),

            (
                "🧠 Skill Analysis",
                "parent_skills"
            ),

            (
                "🎯 Career Guidance",
                "parent_career"
            ),

            (
                "📚 Learning Plan",
                "parent_learning"
            ),

            (
                "📈 Progress",
                "parent_progress"
            ),

        ]

        for label, page in navigation:

            if st.button(
                label,
                key=f"parent_nav_{page}",
                use_container_width=True
            ):

                go_to(page)

        st.divider()

        if st.button(
            "🔄 Refresh Data",
            key="parent_refresh",
            use_container_width=True
        ):

            st.rerun()

        if st.button(
            "🚪 Logout",
            key="parent_logout",
            use_container_width=True
        ):

            logout()


# =========================================================
# SIDEBAR ROUTER
# =========================================================

def show_sidebar():

    if st.session_state.get(
        "user_type"
    ) == "parent":

        show_parent_sidebar()

    else:

        show_student_sidebar()


# =========================================================
# STUDENT DASHBOARD
# =========================================================

def student_dashboard():

    student = st.session_state.get(
        "student",
        {}
    )

    email = student.get(
        "email"
    )

    (
        scores,
        marks,
        percentage,
        overall_marks,
        latest
    ) = get_student_score(
        email
    )

    name = student.get(
        "name",
        "Student"
    )

    first_name = (
        name.split()[0]
        if name
        else "Student"
    )

    html(
        f"""
        <div class="dashboard-hero">

            <div class="dashboard-title">
                Welcome back, {first_name} 👋
            </div>

            <div class="dashboard-subtitle">
                Continue building your skills and discover
                the career path that matches your strengths.
            </div>

        </div>
        """
    )

    col1, col2 = st.columns(
        [1, 2],
        gap="large"
    )

    with col1:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 👤 My Profile"
            )

            html(
                f"""
                <div class="profile-name">
                    {name}
                </div>

                <div class="profile-detail">
                    {student.get("email", "-")}
                </div>

                <div class="profile-detail">
                    {student.get("branch", "-")}
                </div>

                <div class="profile-detail">
                    Semester {student.get("semester", "-")}
                </div>
                """
            )

    with col2:

        with st.container(
            border=True
        ):

            html(
                """
                <div class="card-title">
                    📈 Your Assessment Performance
                </div>

                <div class="card-description">
                    Your latest skill assessment result.
                </div>
                """
            )

            if latest:

                html(
                    f"""
                    <div class="score">
                        {percentage:.0f}%
                    </div>

                    <div class="score-marks">
                        {int(overall_marks)} / 20 marks
                    </div>
                    """
                )

            else:

                html(
                    """
                    <div class="score">
                        --
                    </div>

                    <div class="score-marks">
                        Complete the assessment to see your score.
                    </div>
                    """
                )

    html(
        """
        <div class="section-title">
            Your Skills
        </div>
        """
    )

    skills = [
        "Python",
        "SQL",
        "DSA",
        "Machine Learning",
        "Problem Solving"
    ]

    columns = st.columns(5)

    for index, skill in enumerate(skills):

        with columns[index]:

            value = safe_percentage(
                scores.get(
                    skill,
                    0
                )
            )

            skill_mark = int(
                marks.get(
                    skill,
                    0
                ) or 0
            )

            st.metric(
                skill,
                f"{value:.0f}%"
            )

            st.caption(
                f"{skill_mark} / 4 marks"
            )


# =========================================================
# PARENT HERO
# =========================================================

def parent_hero(
    title,
    subtitle
):

    html(
        f"""
        <div class="parent-hero">

            <div class="parent-title">
                {title}
            </div>

            <div class="parent-subtitle">
                {subtitle}
            </div>

        </div>
        """
    )


# =========================================================
# GET CONNECTED STUDENT
# =========================================================

def get_connected_student():

    parent = st.session_state.get(
        "parent",
        {}
    )

    student_email = parent.get(
        "student_email",
        ""
    )

    if not student_email:
        return None

    try:

        return students_collection.find_one(
            {
                "email":
                    student_email.lower().strip()
            }
        )

    except Exception:

        return None


# =========================================================
# PARENT STUDENT PROFILE
# =========================================================

def parent_student_profile():

    student = get_connected_student()

    parent_hero(
        "👨‍🎓 Student Profile",
        "View the connected student's account information."
    )

    if not student:

        st.warning(
            "The connected student account could not be found."
        )

        return

    col1, col2 = st.columns(
        2,
        gap="large"
    )

    with col1:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 👤 Personal Information"
            )

            st.write(
                f"**Name:** {student.get('name', '-')}"
            )

            st.write(
                f"**Email:** {student.get('email', '-')}"
            )

            st.write(
                f"**Phone:** {student.get('phone', '-')}"
            )

    with col2:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 🎓 Academic Information"
            )

            st.write(
                f"**Branch:** {student.get('branch', '-')}"
            )

            st.write(
                f"**Semester:** {student.get('semester', '-')}"
            )

            html(
                """
                <div class="status-success">
                    ✓ Student account connected
                </div>
                """
            )


# =========================================================
# PARENT ASSESSMENT
# =========================================================

def parent_assessment_page():

    parent = st.session_state.get(
        "parent",
        {}
    )

    student_email = parent.get(
        "student_email"
    )

    parent_hero(
        "📊 Assessment Performance",
        "Monitor the student's latest assessment results and history."
    )

    (
        scores,
        marks,
        percentage,
        overall_marks,
        latest
    ) = get_student_score(
        student_email
    )

    if not latest:

        st.info(
            "The student has not completed an assessment yet."
        )

        return

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Overall Score",
            f"{percentage:.0f}%"
        )

    with col2:
        st.metric(
            "Marks Obtained",
            f"{int(overall_marks)} / 20"
        )

    with col3:
        st.metric(
            "Attempt",
            str(
                latest.get(
                    "attempt",
                    1
                )
            )
        )

    st.markdown(
        "### 🧠 Skill-wise Performance"
    )

    skills = [
        "Python",
        "SQL",
        "DSA",
        "Machine Learning",
        "Problem Solving"
    ]

    columns = st.columns(5)

    for index, skill in enumerate(skills):

        with columns[index]:

            skill_percentage = safe_percentage(
                scores.get(
                    skill,
                    0
                )
            )

            skill_mark = int(
                marks.get(
                    skill,
                    0
                ) or 0
            )

            st.metric(
                skill,
                f"{skill_percentage:.0f}%"
            )

            st.caption(
                f"{skill_mark} / 4 marks"
            )

    st.markdown(
        "### 📝 Assessment History"
    )

    history = load_assessment_history(
        student_email
    )

    if not history:

        st.info(
            "No assessment history available."
        )

        return

    for index, result in enumerate(history):

        result_percentage = safe_percentage(
            result.get(
                "overall_score",
                result.get(
                    "overall_percentage",
                    0
                )
            )
        )

        result_marks = result.get(
            "overall_marks",
            result.get(
                "obtained_marks",
                0
            )
        )

        attempt = result.get(
            "attempt",
            index + 1
        )

        completed_at = format_date(
            result.get(
                "completed_at"
            )
        )

        html(
            f"""
            <div class="history-card">

                <strong>
                    Assessment Attempt {attempt}
                </strong>

                <br>

                <span style="
                    color:#64748b;
                    font-size:13px;
                ">

                    Marks:
                    {int(result_marks)} / 20

                    &nbsp; • &nbsp;

                    Percentage:
                    {result_percentage:.0f}%

                    &nbsp; • &nbsp;

                    Completed:
                    {completed_at}

                </span>

            </div>
            """
        )


# =========================================================
# PARENT SKILL ANALYSIS
# =========================================================

def parent_skill_analysis():

    parent = st.session_state.get(
        "parent",
        {}
    )

    student_email = parent.get(
        "student_email"
    )

    parent_hero(
        "🧠 Skill Analysis",
        "Understand the student's strengths and areas that need improvement."
    )

    (
        scores,
        marks,
        percentage,
        overall_marks,
        latest
    ) = get_student_score(
        student_email
    )

    if not latest:

        st.info(
            "Complete an assessment first to generate skill analysis."
        )

        return

    skills = [
        "Python",
        "SQL",
        "DSA",
        "Machine Learning",
        "Problem Solving"
    ]

    for skill in skills:

        score = safe_percentage(
            scores.get(
                skill,
                0
            )
        )

        skill_mark = int(
            marks.get(
                skill,
                0
            ) or 0
        )

        html(
            f"""
            <div class="data-card">

                <div class="data-title">
                    {skill}
                </div>

                <div class="small-label">
                    Performance
                </div>

                <div class="small-value">
                    {score:.0f}% ({skill_mark} / 4 marks)
                </div>

                <div class="parent-progress-bar">

                    <div
                        class="parent-progress-fill"
                        style="width:{score}%"
                    ></div>

                </div>

            </div>
            """
        )


# =========================================================
# PARENT CAREER GUIDANCE
# =========================================================

def parent_career_guidance():

    parent = st.session_state.get(
        "parent",
        {}
    )

    student_email = parent.get(
        "student_email"
    )

    parent_hero(
        "🎯 Career Guidance",
        "View career recommendations based on the student's assessed skills."
    )

    results = load_career_results(
        student_email
    )

    if not results:

        html(
            """
            <div class="status-empty">
                No career guidance result is available yet.
                <br><br>
                The student needs to complete the skill assessment first.
            </div>
            """
        )

        return

    result = results[0]

    career_matches = result.get(
        "career_matches",
        []
    )

    student_scores = result.get(
        "student_scores",
        {}
    )

    if student_scores:

        st.markdown(
            "### 📊 Student Skill Scores"
        )

        score_columns = st.columns(
            len(student_scores)
        )

        for index, (
            skill,
            score
        ) in enumerate(
            student_scores.items()
        ):

            with score_columns[index]:

                st.metric(
                    skill,
                    f"{safe_percentage(score):.0f}%"
                )

    st.markdown(
        "### 🎯 Career Recommendations"
    )

    if not career_matches:

        st.info(
            "No career recommendations are available."
        )

        return

    for index, career_data in enumerate(
        career_matches
    ):

        if not isinstance(
            career_data,
            dict
        ):
            continue

        career_name = career_data.get(
            "career",
            "Career Recommendation"
        )

        match_percentage = safe_percentage(
            career_data.get(
                "match_percentage",
                0
            )
        )

        skill_gaps = career_data.get(
            "skill_gaps",
            []
        )

        with st.container(
            border=True
        ):

            html(
                f"""
                <div class="data-title">
                    🎯 {career_name}
                </div>

                <div class="data-text">
                    Career match based on the student's assessed skills.
                </div>
                """
            )

            st.progress(
                match_percentage / 100
            )

            st.metric(
                "Career Match",
                f"{match_percentage:.0f}%"
            )

            if skill_gaps:

                st.markdown(
                    "#### 📚 Skills to Improve"
                )

                for gap in skill_gaps:

                    if not isinstance(
                        gap,
                        dict
                    ):
                        continue

                    skill = gap.get(
                        "skill",
                        "Skill"
                    )

                    student_score = safe_percentage(
                        gap.get(
                            "student_score",
                            0
                        )
                    )

                    required_score = safe_percentage(
                        gap.get(
                            "required_score",
                            0
                        )
                    )

                    gap_value = safe_percentage(
                        gap.get(
                            "gap",
                            0
                        )
                    )

                    c1, c2, c3 = st.columns(3)

                    with c1:
                        st.write(
                            f"**{skill}**"
                        )

                    with c2:
                        st.write(
                            f"Student: {student_score:.0f}%"
                        )

                    with c3:
                        st.write(
                            f"Required: {required_score:.0f}%"
                        )

                    st.progress(
                        student_score / 100
                    )

                    if gap_value > 0:

                        st.caption(
                            f"Skill gap: {gap_value:.0f} percentage points"
                        )


# =========================================================
# PARENT LEARNING PLAN
# =========================================================

def parent_learning_plan():

    parent = st.session_state.get(
        "parent",
        {}
    )

    student_email = parent.get(
        "student_email"
    )

    parent_hero(
        "📚 Learning Plan",
        "View the personalized learning plan generated from the student's skill assessment."
    )

    resources = load_learning_resources(
        student_email
    )

    if not resources:

        html(
            """
            <div class="status-empty">

                No learning plan is available yet.

                <br><br>

                Complete the student's assessment to generate
                a personalized learning plan.

            </div>
            """
        )

        return

    plan = resources[0]

    target_career = plan.get(
        "target_career",
        "Career Development"
    )

    total_weeks = plan.get(
        "total_weeks",
        "-"
    )

    created_at = plan.get(
        "created_at"
    )

    # -----------------------------------------------------
    # FIND SKILL PLAN RECURSIVELY
    # -----------------------------------------------------

    def find_skill_plan(data):

        if isinstance(data, list):

            valid_items = []

            for item in data:

                if isinstance(
                    item,
                    dict
                ):

                    if (
                        "skill" in item
                        and (
                            "score" in item
                            or "priority" in item
                            or "weeks" in item
                        )
                    ):

                        valid_items.append(
                            item
                        )

            if valid_items:
                return valid_items

            for item in data:

                result = find_skill_plan(
                    item
                )

                if result:
                    return result

        elif isinstance(data, dict):

            possible_fields = [
                "skill_plan",
                "skills",
                "skill_development_plan",
                "learning_plan",
                "plan",
                "skill_development",
                "resources",
            ]

            for field in possible_fields:

                if field in data:

                    result = find_skill_plan(
                        data[field]
                    )

                    if result:
                        return result

            for key, value in data.items():

                if key in [
                    "_id",
                    "student_email",
                    "target_career",
                    "created_at",
                    "total_weeks",
                ]:
                    continue

                result = find_skill_plan(
                    value
                )

                if result:
                    return result

        return []

    skill_plan = find_skill_plan(
        plan
    )

    # -----------------------------------------------------
    # OVERVIEW
    # -----------------------------------------------------

    st.markdown(
        "### 🎯 Learning Plan Overview"
    )

    col1, col2 = st.columns(2)

    with col1:

        with st.container(
            border=True
        ):

            st.markdown(
                "#### 🎯 Target Career"
            )

            html(
                f"""
                <div class="profile-name">
                    {target_career}
                </div>
                """
            )

    with col2:

        with st.container(
            border=True
        ):

            st.markdown(
                "#### ⏱️ Total Duration"
            )

            html(
                f"""
                <div class="profile-name">
                    {total_weeks} weeks
                </div>
                """
            )

    # -----------------------------------------------------
    # SKILL DEVELOPMENT
    # -----------------------------------------------------

    st.markdown(
        "### 🧠 Skill Development Plan"
    )

    if not skill_plan:

        st.info(
            "No skill development plan is available."
        )

        return

    for index, skill_data in enumerate(
        skill_plan
    ):

        if not isinstance(
            skill_data,
            dict
        ):
            continue

        skill = skill_data.get(
            "skill",
            "Skill"
        )

        score = safe_percentage(
            skill_data.get(
                "score",
                0
            )
        )

        priority = skill_data.get(
            "priority",
            "Medium"
        )

        weeks = skill_data.get(
            "weeks",
            "-"
        )

        priority_text = str(
            priority
        ).strip().lower()

        if priority_text == "high":
            priority_icon = "🔴"
        elif priority_text == "medium":
            priority_icon = "🟠"
        else:
            priority_icon = "🟢"

        with st.container(
            border=True
        ):

            html(
                f"""
                <div class="data-title">
                    🧠 {skill}
                </div>

                <div class="data-text">
                    Current skill score: {score:.0f}%
                    &nbsp; • &nbsp;
                    Priority: {priority}
                    &nbsp; • &nbsp;
                    Duration: {weeks} weeks
                </div>
                """
            )

            st.progress(
                score / 100
            )

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(
                    "Current Score",
                    f"{score:.0f}%"
                )

            with c2:

                st.metric(
                    "Priority",
                    f"{priority_icon} {priority}"
                )

            with c3:

                st.metric(
                    "Duration",
                    f"{weeks} weeks"
                )

        if index < len(skill_plan) - 1:
            st.divider()

    if created_at:

        st.caption(
            f"Learning plan generated on: "
            f"{format_date(created_at)}"
        )


# =========================================================
# PARENT PROGRESS
# =========================================================

def parent_progress():

    parent = st.session_state.get(
        "parent",
        {}
    )

    student_email = parent.get(
        "student_email"
    )

    parent_hero(
        "📈 Progress Tracking",
        "Monitor the student's learning and assessment progress."
    )

    history = load_assessment_history(
        student_email
    )

    progress_records = load_progress_records(
        student_email
    )

    st.markdown(
        "### 📊 Assessment Progress"
    )

    if not history:

        st.info(
            "No assessment progress is available yet."
        )

    else:

        percentages = []

        for result in history:

            value = safe_percentage(
                result.get(
                    "overall_score",
                    result.get(
                        "overall_percentage",
                        0
                    )
                )
            )

            percentages.append(
                value
            )

        latest_percentage = percentages[0]
        first_percentage = percentages[-1]

        change = (
            latest_percentage
            - first_percentage
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Assessments Completed",
                len(history)
            )

        with col2:

            st.metric(
                "Latest Score",
                f"{latest_percentage:.0f}%"
            )

        with col3:

            st.metric(
                "Change",
                f"{change:+.0f}%"
            )

        st.markdown(
            "### Assessment Timeline"
        )

        for index, result in enumerate(
            reversed(history)
        ):

            score = safe_percentage(
                result.get(
                    "overall_score",
                    result.get(
                        "overall_percentage",
                        0
                    )
                )
            )

            attempt = result.get(
                "attempt",
                index + 1
            )

            completed = format_date(
                result.get(
                    "completed_at"
                )
            )

            st.write(
                f"**Attempt {attempt}** — "
                f"{score:.0f}% — {completed}"
            )

            st.progress(
                score / 100
            )

    st.markdown(
        "### 📚 Learning Progress"
    )

    if not progress_records:

        st.info(
            "No separate learning progress records are available yet."
        )

    else:

        for record in progress_records:

            skill = first_value(
                record,
                [
                    "skill",
                    "topic",
                    "subject",
                    "category",
                    "name"
                ],
                "Learning Area"
            )

            value = first_value(
                record,
                [
                    "progress",
                    "percentage",
                    "completion",
                    "completion_percentage"
                ],
                0
            )

            progress_value = safe_percentage(
                value
            )

            status = first_value(
                record,
                [
                    "status",
                    "state"
                ],
                "In Progress"
            )

            html(
                f"""
                <div class="data-card">

                    <div class="data-title">
                        {skill}
                    </div>

                    <div class="small-value">
                        {progress_value:.0f}% completed
                    </div>

                    <div class="parent-progress-bar">

                        <div
                            class="parent-progress-fill"
                            style="width:{progress_value}%"
                        ></div>

                    </div>

                    <div class="data-text">
                        Status: {status}
                    </div>

                </div>
                """
            )


# =========================================================
# PARENT DASHBOARD
# =========================================================

def parent_dashboard():

    parent = st.session_state.get(
        "parent",
        {}
    )

    parent_name = parent.get(
        "name",
        "Parent"
    )

    student = get_connected_student()

    first_name = (
        parent_name.split()[0]
        if parent_name
        else "Parent"
    )

    parent_hero(
        f"Welcome, {first_name} 👋",
        "Monitor your student's learning, skills and career development."
    )

    if not student:

        st.warning(
            "The connected student account could not be found."
        )

        return

    col1, col2 = st.columns(
        [1, 2],
        gap="large"
    )

    with col1:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 👨‍🎓 Student"
            )

            html(
                f"""
                <div class="profile-name">
                    {student.get("name", "-")}
                </div>

                <div class="profile-detail">
                    {student.get("email", "-")}
                </div>

                <div class="profile-detail">
                    {student.get("branch", "-")}
                </div>

                <div class="profile-detail">
                    Semester {student.get("semester", "-")}
                </div>
                """
            )

    with col2:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 🔗 Connection"
            )

            html(
                f"""
                <div class="status-success">
                    ✓ Connected Student Account
                </div>

                <br>

                <div class="small-label">
                    Student Email
                </div>

                <div class="small-value">
                    {student.get("email", "-")}
                </div>
                """
            )

    st.markdown(
        "### 📊 Assessment Summary"
    )

    (
        scores,
        marks,
        percentage,
        overall_marks,
        latest
    ) = get_student_score(
        student.get("email")
    )

    if latest:

        history = load_assessment_history(
            student.get("email")
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Overall Score",
                f"{percentage:.0f}%"
            )

        with col2:
            st.metric(
                "Marks",
                f"{int(overall_marks)} / 20"
            )

        with col3:
            st.metric(
                "Attempts",
                len(history)
            )

        with col4:
            st.metric(
                "Latest Attempt",
                latest.get(
                    "attempt",
                    1
                )
            )

    else:

        st.info(
            "The student has not completed an assessment yet."
        )

    st.markdown(
        "### 🧠 Skill Snapshot"
    )

    skills = [
        "Python",
        "SQL",
        "DSA",
        "Machine Learning",
        "Problem Solving"
    ]

    columns = st.columns(5)

    for index, skill in enumerate(skills):

        with columns[index]:

            value = safe_percentage(
                scores.get(
                    skill,
                    0
                )
            )

            st.metric(
                skill,
                f"{value:.0f}%"
            )

    st.markdown(
        "### 🚀 Parent Portal"
    )

    feature_data = [

        (
            "parent_student",
            "👨‍🎓",
            "Student Profile",
            "View academic and personal information."
        ),

        (
            "parent_assessment",
            "📊",
            "Assessment",
            "View marks, percentage and assessment history."
        ),

        (
            "parent_skills",
            "🧠",
            "Skill Analysis",
            "Understand strengths and improvement areas."
        ),

        (
            "parent_career",
            "🎯",
            "Career Guidance",
            "View available career guidance results."
        ),

        (
            "parent_learning",
            "📚",
            "Learning Plan",
            "View learning resources and development areas."
        ),

        (
            "parent_progress",
            "📈",
            "Progress",
            "Track assessment and learning progress."
        ),
    ]

    row1 = st.columns(3)

    for index in range(3):

        page, icon, title, description = feature_data[index]

        with row1[index]:

            with st.container(
                border=True
            ):

                html(
                    f"""
                    <div class="icon">
                        {icon}
                    </div>

                    <div class="card-title">
                        {title}
                    </div>

                    <div class="card-description">
                        {description}
                    </div>
                    """
                )

                if st.button(
                    f"Open {title} →",
                    key=f"parent_feature_{page}",
                    use_container_width=True
                ):

                    go_to(page)

    row2 = st.columns(3)

    for index in range(3, 6):

        page, icon, title, description = feature_data[index]

        with row2[index - 3]:

            with st.container(
                border=True
            ):

                html(
                    f"""
                    <div class="icon">
                        {icon}
                    </div>

                    <div class="card-title">
                        {title}
                    </div>

                    <div class="card-description">
                        {description}
                    </div>
                    """
                )

                if st.button(
                    f"Open {title} →",
                    key=f"parent_feature_{page}",
                    use_container_width=True
                ):

                    go_to(page)


# =========================================================
# LOGIN PAGE
# =========================================================

def login_page():

    left, right = st.columns(
        [1.25, 0.85],
        gap="large"
    )

    with left:

        html(
            """
            <div class="hero">

                <div class="badge">
                    ✨ AI-POWERED CAREER PLATFORM
                </div>

                <div class="hero-title">
                    Discover your<br>
                    <span>career path.</span>
                </div>

                <div class="hero-description">
                    Assess your technical skills, understand your
                    strengths, discover suitable career paths and
                    follow a personalized learning roadmap.
                </div>

                <div class="feature-row">

                    <div class="feature-chip">
                        📝 Skill Assessment
                    </div>

                    <div class="feature-chip">
                        🎯 Career Guidance
                    </div>

                    <div class="feature-chip">
                        📊 Skill Analysis
                    </div>

                    <div class="feature-chip">
                        📚 Learning Plan
                    </div>

                    <div class="feature-chip">
                        👨‍👩‍👦 Parent Monitoring
                    </div>

                </div>

            </div>
            """
        )

    with right:

        with st.container(
            border=True
        ):

            html(
                """
                <div class="login-heading">
                    Welcome back 👋
                </div>

                <div class="login-description">
                    Sign in to continue your career journey.
                </div>
                """
            )

            login_type = st.radio(
                "Login as",
                [
                    "👨‍🎓 Student",
                    "👨‍👩‍👦 Parent"
                ],
                horizontal=True,
                label_visibility="collapsed"
            )

            # =================================================
            # STUDENT
            # =================================================

            if login_type == "👨‍🎓 Student":

                action = st.radio(
                    "Account",
                    [
                        "Login",
                        "Create Account"
                    ],
                    horizontal=True
                )

                # ---------------------------------------------
                # STUDENT LOGIN
                # ---------------------------------------------

                if action == "Login":

                    email = st.text_input(
                        "Email",
                        key="student_login_email"
                    )

                    password = st.text_input(
                        "Password",
                        type="password",
                        key="student_login_password"
                    )

                    if st.button(
                        "Sign In →",
                        type="primary",
                        use_container_width=True
                    ):

                        if (
                            not email
                            or not password
                        ):

                            st.warning(
                                "Please enter your email and password."
                            )

                        elif not is_valid_email(email):

                            st.error(
                                "❌ Invalid email address. "
                                "Please enter a valid email such as example@gmail.com."
                            )

                        else:

                            student = students_collection.find_one(
                                {
                                    "email":
                                        email.lower().strip(),

                                    "password":
                                        hash_password(
                                            password
                                        )
                                }
                            )

                            if student:

                                st.session_state[
                                    "logged_in"
                                ] = True

                                st.session_state[
                                    "user_type"
                                ] = "student"

                                st.session_state[
                                    "student"
                                ] = student

                                st.session_state[
                                    "page"
                                ] = "dashboard"

                                st.rerun()

                            else:

                                st.error(
                                    "Invalid email or password."
                                )

                # ---------------------------------------------
                # STUDENT REGISTRATION
                # ---------------------------------------------

                else:

                    st.markdown(
                        "### Create Student Account"
                    )

                    name = st.text_input(
                        "Full Name",
                        key="register_name"
                    )

                    email = st.text_input(
                        "Email",
                        key="register_email"
                    )

                    password = st.text_input(
                        "Create Password",
                        type="password",
                        key="register_password"
                    )

                    confirm_password = st.text_input(
                        "Confirm Password",
                        type="password",
                        key="register_confirm_password"
                    )

                    branch = st.selectbox(
                        "Branch",
                        [
                            "Computer Science and Engineering",
                            "Information Science",
                            "Electronics and Communication",
                            "Mechanical Engineering",
                            "Civil Engineering",
                            "Electrical Engineering",
                            "Other"
                        ],
                        key="register_branch"
                    )

                    semester = st.selectbox(
                        "Semester",
                        [
                            "1",
                            "2",
                            "3",
                            "4",
                            "5",
                            "6",
                            "7",
                            "8"
                        ],
                        key="register_semester"
                    )

                    phone = st.text_input(
                        "Phone Number",
                        key="register_phone"
                    )

                    if st.button(
                        "Create Account →",
                        type="primary",
                        use_container_width=True
                    ):

                        if (
                            not name
                            or not email
                            or not password
                            or not confirm_password
                        ):

                            st.warning(
                                "Please fill all required fields."
                            )

                        elif not is_valid_email(email):

                            st.error(
                                "❌ Invalid email address. "
                                "Please enter a valid email such as example@gmail.com."
                            )

                        elif password != confirm_password:

                            st.error(
                                "Passwords do not match."
                            )

                        elif len(password) < 6:

                            st.error(
                                "Password must contain at least 6 characters."
                            )

                        else:

                            clean_email = (
                                email.lower().strip()
                            )

                            existing = students_collection.find_one(
                                {
                                    "email":
                                        clean_email
                                }
                            )

                            if existing:

                                st.error(
                                    "An account with this email already exists."
                                )

                            else:

                                students_collection.insert_one(
                                    {
                                        "name":
                                            name.strip(),

                                        "email":
                                            clean_email,

                                        "password":
                                            hash_password(
                                                password
                                            ),

                                        "branch":
                                            branch,

                                        "semester":
                                            semester,

                                        "phone":
                                            phone.strip()
                                    }
                                )

                                st.success(
                                    "Account created successfully. "
                                    "Switch to Login to continue."
                                )

            # =================================================
            # PARENT
            # =================================================

            else:

                action = st.radio(
                    "Parent Account",
                    [
                        "Login",
                        "Create Account"
                    ],
                    horizontal=True,
                    key="parent_account_action"
                )

                # ---------------------------------------------
                # PARENT LOGIN
                # ---------------------------------------------

                if action == "Login":

                    st.markdown(
                        "### Parent Login"
                    )

                    email = st.text_input(
                        "Parent Email",
                        key="parent_login_email"
                    )

                    password = st.text_input(
                        "Password",
                        type="password",
                        key="parent_login_password"
                    )

                    if st.button(
                        "Parent Sign In →",
                        type="primary",
                        use_container_width=True
                    ):

                        if (
                            not email
                            or not password
                        ):

                            st.warning(
                                "Please enter your email and password."
                            )

                        elif not is_valid_email(email):

                            st.error(
                                "❌ Invalid email address. "
                                "Please enter a valid email such as example@gmail.com."
                            )

                        else:

                            parent = parents_collection.find_one(
                                {
                                    "email":
                                        email.lower().strip(),

                                    "password":
                                        hash_password(
                                            password
                                        )
                                }
                            )

                            if parent:

                                st.session_state[
                                    "logged_in"
                                ] = True

                                st.session_state[
                                    "user_type"
                                ] = "parent"

                                st.session_state[
                                    "parent"
                                ] = parent

                                st.session_state[
                                    "page"
                                ] = "parent_dashboard"

                                st.rerun()

                            else:

                                st.error(
                                    "Invalid email or password."
                                )

                # ---------------------------------------------
                # PARENT REGISTRATION
                # ---------------------------------------------

                else:

                    st.markdown(
                        "### Create Parent Account"
                    )

                    parent_name = st.text_input(
                        "Parent Full Name",
                        key="parent_register_name"
                    )

                    parent_email = st.text_input(
                        "Parent Email",
                        key="parent_register_email"
                    )

                    parent_password = st.text_input(
                        "Create Password",
                        type="password",
                        key="parent_register_password"
                    )

                    parent_confirm_password = st.text_input(
                        "Confirm Password",
                        type="password",
                        key="parent_register_confirm_password"
                    )

                    student_email = st.text_input(
                        "Student Email",
                        placeholder="Enter student's registered email",
                        key="parent_student_email"
                    )

                    st.caption(
                        "Enter the same email used by the student during registration."
                    )

                    if st.button(
                        "Create Parent Account →",
                        type="primary",
                        use_container_width=True
                    ):

                        if (
                            not parent_name
                            or not parent_email
                            or not parent_password
                            or not parent_confirm_password
                            or not student_email
                        ):

                            st.warning(
                                "Please fill all required fields."
                            )

                        elif not is_valid_email(parent_email):

                            st.error(
                                "❌ Invalid parent email address. "
                                "Please enter a valid email such as example@gmail.com."
                            )

                        elif not is_valid_email(student_email):

                            st.error(
                                "❌ Invalid student email address. "
                                "Please enter a valid email such as example@gmail.com."
                            )

                        elif (
                            parent_password
                            != parent_confirm_password
                        ):

                            st.error(
                                "Passwords do not match."
                            )

                        elif len(parent_password) < 6:

                            st.error(
                                "Password must contain at least 6 characters."
                            )

                        else:

                            clean_parent_email = (
                                parent_email.lower().strip()
                            )

                            clean_student_email = (
                                student_email.lower().strip()
                            )

                            existing_parent = (
                                parents_collection.find_one(
                                    {
                                        "email":
                                            clean_parent_email
                                    }
                                )
                            )

                            if existing_parent:

                                st.error(
                                    "A parent account with this email already exists."
                                )

                            else:

                                student = (
                                    students_collection.find_one(
                                        {
                                            "email":
                                                clean_student_email
                                        }
                                    )
                                )

                                if not student:

                                    st.error(
                                        "Student account not found. "
                                        "Please check the student's email."
                                    )

                                else:

                                    parents_collection.insert_one(
                                        {
                                            "name":
                                                parent_name.strip(),

                                            "email":
                                                clean_parent_email,

                                            "password":
                                                hash_password(
                                                    parent_password
                                                ),

                                            "student_email":
                                                clean_student_email
                                        }
                                    )

                                    st.success(
                                        "Parent account created successfully. "
                                        "Switch to Login to continue."
                                    )


# =========================================================
# MODULE ROUTER
# =========================================================

def show_module(
    module_name,
    function_names,
    title,
    message
):

    function = load_page_function(
        module_name,
        function_names
    )

    if function:

        function()

    else:

        st.title(
            title
        )

        st.info(
            message
        )


# =========================================================
# MAIN CONTROLLER
# =========================================================

if st.session_state.get(
    "logged_in",
    False
):

    show_sidebar()

    page = st.session_state.get(
        "page",
        "dashboard"
    )

    # =====================================================
    # PARENT ROUTES
    # =====================================================

    if st.session_state.get(
        "user_type"
    ) == "parent":

        if page == "parent_dashboard":

            parent_dashboard()

        elif page == "parent_student":

            parent_student_profile()

        elif page == "parent_assessment":

            parent_assessment_page()

        elif page == "parent_skills":

            parent_skill_analysis()

        elif page == "parent_career":

            parent_career_guidance()

        elif page == "parent_learning":

            parent_learning_plan()

        elif page == "parent_progress":

            parent_progress()

        else:

            go_to(
                "parent_dashboard"
            )

    # =====================================================
    # STUDENT ROUTES
    # =====================================================

    else:

        if page == "dashboard":

            student_dashboard()

        elif page == "assessment_intro":

            assessment_instructions_page()

        elif page == "assessment":

            skill_assessment_page()

        elif page == "career":

            show_module(
                "career_matching",
                [
                    "career_matching_page",
                    "career_guidance_page",
                    "career_page"
                ],
                "🎯 Career Guidance",
                "Career guidance module is not connected."
            )

        elif page == "skills":

            show_module(
                "skill_analysis",
                [
                    "skill_analysis_page",
                    "skills_analysis_page",
                    "skill_page"
                ],
                "📊 Skill Analysis",
                "Skill analysis module is not connected."
            )

        elif page == "learning":

            show_module(
                "learning_plan",
                [
                    "learning_plan_page",
                    "learning_page",
                    "personalized_learning_page"
                ],
                "📚 Learning Plan",
                "Learning plan module is not connected."
            )

        elif page == "progress":

            show_module(
                "progress",
                [
                    "progress_page",
                    "progress_tracking_page",
                    "progress_tracking"
                ],
                "📈 Progress Tracking",
                "Progress module is not connected."
            )

        else:

            go_to(
                "dashboard"
            )

else:

    login_page()