import random
import time
from datetime import datetime

import streamlit as st

from database import assessments_collection


# ============================================================
# ASSESSMENT SETTINGS
# ============================================================

TOTAL_QUESTIONS = 20
TOTAL_MARKS = 20
MARKS_PER_QUESTION = 1
TIME_LIMIT_SECONDS = 20 * 60


# ============================================================
# QUESTION BANK
# ============================================================

QUESTIONS = [

    # ========================================================
    # PYTHON
    # ========================================================

    {
        "skill": "Python",
        "question": "Which keyword is used to define a function in Python?",
        "options": [
            "func",
            "define",
            "def",
            "function"
        ],
        "answer": "def"
    },

    {
        "skill": "Python",
        "question": "Which data type is immutable in Python?",
        "options": [
            "List",
            "Dictionary",
            "Set",
            "Tuple"
        ],
        "answer": "Tuple"
    },

    {
        "skill": "Python",
        "question": "Which symbol is used to write a single-line comment in Python?",
        "options": [
            "//",
            "#",
            "/*",
            "--"
        ],
        "answer": "#"
    },

    {
        "skill": "Python",
        "question": "Which function is used to find the length of a list in Python?",
        "options": [
            "size()",
            "length()",
            "count()",
            "len()"
        ],
        "answer": "len()"
    },


    # ========================================================
    # SQL
    # ========================================================

    {
        "skill": "SQL",
        "question": "Which SQL command is used to retrieve data from a table?",
        "options": [
            "GET",
            "FETCH",
            "SELECT",
            "READ"
        ],
        "answer": "SELECT"
    },

    {
        "skill": "SQL",
        "question": "Which SQL clause is used to filter records?",
        "options": [
            "ORDER BY",
            "WHERE",
            "GROUP BY",
            "FILTER"
        ],
        "answer": "WHERE"
    },

    {
        "skill": "SQL",
        "question": "Which command is used to add a new row to a table?",
        "options": [
            "ADD",
            "INSERT",
            "UPDATE",
            "CREATE"
        ],
        "answer": "INSERT"
    },

    {
        "skill": "SQL",
        "question": "Which keyword is used to remove duplicate records from query results?",
        "options": [
            "UNIQUE",
            "DISTINCT",
            "REMOVE",
            "DIFFERENT"
        ],
        "answer": "DISTINCT"
    },


    # ========================================================
    # DSA
    # ========================================================

    {
        "skill": "DSA",
        "question": "Which data structure follows the LIFO principle?",
        "options": [
            "Queue",
            "Stack",
            "Array",
            "Linked List"
        ],
        "answer": "Stack"
    },

    {
        "skill": "DSA",
        "question": "Which data structure follows the FIFO principle?",
        "options": [
            "Stack",
            "Tree",
            "Queue",
            "Graph"
        ],
        "answer": "Queue"
    },

    {
        "skill": "DSA",
        "question": "What is the average time complexity of binary search on a sorted array?",
        "options": [
            "O(n)",
            "O(log n)",
            "O(n²)",
            "O(1)"
        ],
        "answer": "O(log n)"
    },

    {
        "skill": "DSA",
        "question": "Which traversal visits the root node between the left and right subtrees?",
        "options": [
            "Preorder",
            "Postorder",
            "Inorder",
            "Level order"
        ],
        "answer": "Inorder"
    },


    # ========================================================
    # MACHINE LEARNING
    # ========================================================

    {
        "skill": "Machine Learning",
        "question": "Which type of learning uses labelled training data?",
        "options": [
            "Unsupervised learning",
            "Supervised learning",
            "Reinforcement learning",
            "Random learning"
        ],
        "answer": "Supervised learning"
    },

    {
        "skill": "Machine Learning",
        "question": "Which algorithm is commonly used for classification?",
        "options": [
            "Linear Regression",
            "Logistic Regression",
            "K-Means only",
            "PCA"
        ],
        "answer": "Logistic Regression"
    },

    {
        "skill": "Machine Learning",
        "question": "What is overfitting?",
        "options": [
            "Model performs poorly on training data",
            "Model performs well on training data but poorly on unseen data",
            "Model has no parameters",
            "Model always predicts the same value"
        ],
        "answer": "Model performs well on training data but poorly on unseen data"
    },

    {
        "skill": "Machine Learning",
        "question": "Which metric is commonly used for classification performance?",
        "options": [
            "Accuracy",
            "Mean squared error only",
            "Variance",
            "Standard deviation"
        ],
        "answer": "Accuracy"
    },


    # ========================================================
    # PROBLEM SOLVING
    # ========================================================

    {
        "skill": "Problem Solving",
        "question": "What should you generally do first when solving a programming problem?",
        "options": [
            "Start coding immediately",
            "Understand and analyse the problem",
            "Delete the input",
            "Choose random variables"
        ],
        "answer": "Understand and analyse the problem"
    },

    {
        "skill": "Problem Solving",
        "question": "Which approach breaks a problem into smaller subproblems?",
        "options": [
            "Decomposition",
            "Compilation",
            "Encryption",
            "Formatting"
        ],
        "answer": "Decomposition"
    },

    {
        "skill": "Problem Solving",
        "question": "What is an algorithm?",
        "options": [
            "A programming language",
            "A step-by-step procedure for solving a problem",
            "A database",
            "A computer"
        ],
        "answer": "A step-by-step procedure for solving a problem"
    },

    {
        "skill": "Problem Solving",
        "question": "Why is testing important in problem solving?",
        "options": [
            "To make code longer",
            "To identify errors and verify correctness",
            "To remove all comments",
            "To increase file size"
        ],
        "answer": "To identify errors and verify correctness"
    }
]


# ============================================================
# SESSION STATE
# ============================================================

def initialize_assessment_state():

    defaults = {
        "assessment_started": False,
        "assessment_submitted": False,

        "assessment_start_time": None,
        "assessment_end_time": None,

        "assessment_questions": [],
        "assessment_answers": {},

        "assessment_scores": {},
        "assessment_marks": {},

        "overall_score": 0,
        "overall_marks": 0,

        "assessment_attempt": 0,

        "assessment_auto_submitted": False,
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


initialize_assessment_state()


# ============================================================
# START A NEW TEST
# ============================================================

def start_new_assessment():

    # Make a fresh copy of the question bank.
    questions = QUESTIONS.copy()

    # Randomize question order.
    random.shuffle(questions)

    # Clear all previous answers.
    st.session_state["assessment_answers"] = {}

    # Clear previous results.
    st.session_state["assessment_scores"] = {}
    st.session_state["assessment_marks"] = {}

    st.session_state["overall_score"] = 0
    st.session_state["overall_marks"] = 0

    # Increase attempt number.
    st.session_state["assessment_attempt"] = (
        st.session_state.get(
            "assessment_attempt",
            0
        ) + 1
    )

    # Start timer.
    start_time = time.time()

    st.session_state["assessment_start_time"] = start_time

    st.session_state["assessment_end_time"] = (
        start_time + TIME_LIMIT_SECONDS
    )

    # Store new questions.
    st.session_state["assessment_questions"] = questions

    # Set assessment state.
    st.session_state["assessment_started"] = True
    st.session_state["assessment_submitted"] = False
    st.session_state["assessment_auto_submitted"] = False

    # Navigate to assessment.
    st.session_state["page"] = "assessment"

    st.rerun()


# ============================================================
# INSTRUCTIONS PAGE
# ============================================================

def assessment_instructions_page():

    st.title("📝 Skill Assessment")

    st.write(
        "Before starting the assessment, please read the instructions carefully."
    )

    st.markdown("")


    # --------------------------------------------------------
    # INSTRUCTIONS
    # --------------------------------------------------------

    with st.container(border=True):

        st.subheader("📋 Test Instructions")

        instructions = [

            "The assessment contains 20 questions.",

            "Each question carries 1 mark.",

            "The maximum score is 20 marks.",

            "The total duration of the assessment is 20 minutes.",

            "The timer starts only after you click Start Test.",

            "Questions cover Python, SQL, DSA, Machine Learning and Problem Solving.",

            "No answer will be selected automatically.",

            "If the timer reaches zero, the assessment will be submitted automatically.",

            "You can submit the assessment before the time limit.",

            "A retest will generate a different randomized question order.",

        ]

        for number, instruction in enumerate(
            instructions,
            start=1
        ):

            st.markdown(
                f"""
                <div style="
                    padding:13px 16px;
                    margin:8px 0;
                    border-radius:12px;
                    background:#f8fafc;
                    border:1px solid #e2e8f0;
                    color:#334155;
                    font-size:15px;
                    line-height:1.5;
                ">
                    <strong>{number}.</strong>
                    &nbsp;&nbsp;
                    {instruction}
                </div>
                """,
                unsafe_allow_html=True
            )


    st.markdown("")


    # --------------------------------------------------------
    # SUMMARY CARDS
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Questions",
            "20"
        )

    with c2:

        st.metric(
            "Total Marks",
            "20"
        )

    with c3:

        st.metric(
            "Duration",
            "20 min"
        )

    with c4:

        st.metric(
            "Marks / Question",
            "1"
        )


    st.markdown("")


    st.warning(
        "⚠️ Once you click Start Test, the 20-minute timer will begin."
    )


    # --------------------------------------------------------
    # START BUTTON
    # --------------------------------------------------------

    left, center, right = st.columns(
        [1, 2, 1]
    )

    with center:

        if st.button(
            "🚀 Start Test",
            type="primary",
            use_container_width=True
        ):

            start_new_assessment()


# ============================================================
# GET REMAINING TIME
# ============================================================

def get_remaining_seconds():

    end_time = st.session_state.get(
        "assessment_end_time"
    )

    if not end_time:
        return 0

    remaining = int(
        end_time - time.time()
    )

    return max(
        0,
        remaining
    )


# ============================================================
# FIXED TIMER
# ============================================================

def display_timer():

    remaining = get_remaining_seconds()

    minutes = remaining // 60
    seconds = remaining % 60


    # Change appearance during final minute.

    if remaining <= 60:

        border_color = "#dc2626"
        background_color = "#fff1f2"
        text_color = "#b91c1c"

    else:

        border_color = "#4f46e5"
        background_color = "#eef2ff"
        text_color = "#4338ca"


    # IMPORTANT:
    #
    # position: fixed
    #
    # means the timer is attached to the browser viewport
    # and does NOT move when the user scrolls.
    #
    # st.html() is used instead of st.markdown() so that
    # the HTML/CSS is rendered instead of appearing as text.

    st.html(
        f"""
        <style>

        /* ==================================================
           SKILLPATH AI FIXED TIMER
           ================================================== */

        #skillpath-fixed-timer {{

            position: fixed !important;

            top: 18px !important;

            right: 28px !important;

            z-index: 999999999 !important;

            width: 235px !important;

            min-height: 78px !important;

            box-sizing: border-box !important;

            padding: 12px 18px !important;

            border-radius: 16px !important;

            border: 2px solid
                {border_color} !important;

            background:
                {background_color} !important;

            box-shadow:
                0 8px 25px
                rgba(15, 23, 42, 0.18) !important;

            display: flex !important;

            flex-direction: column !important;

            align-items: center !important;

            justify-content: center !important;

            text-align: center !important;

            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif !important;

        }}


        #skillpath-fixed-timer
        .timer-title {{

            color:
                {text_color} !important;

            font-size:
                12px !important;

            font-weight:
                800 !important;

            letter-spacing:
                0.5px !important;

            margin:
                0 0 5px 0 !important;

            padding:
                0 !important;

        }}


        #skillpath-fixed-timer
        .timer-value {{

            color:
                {text_color} !important;

            font-size:
                30px !important;

            line-height:
                1 !important;

            font-weight:
                900 !important;

            font-variant-numeric:
                tabular-nums !important;

            letter-spacing:
                1px !important;

            margin:
                0 !important;

            padding:
                0 !important;

        }}


        /* ==================================================
           MOBILE
           ================================================== */

        @media (max-width: 700px) {{

            #skillpath-fixed-timer {{

                top:
                    10px !important;

                right:
                    10px !important;

                width:
                    175px !important;

                min-height:
                    65px !important;

                padding:
                    9px 12px !important;

            }}


            #skillpath-fixed-timer
            .timer-title {{

                font-size:
                    10px !important;

            }}


            #skillpath-fixed-timer
            .timer-value {{

                font-size:
                    25px !important;

            }}

        }}

        </style>


        <div id="skillpath-fixed-timer">

            <div class="timer-title">
                ⏱️ TIME REMAINING
            </div>

            <div class="timer-value">
                {minutes:02d}:{seconds:02d}
            </div>

        </div>
        """
    )

    return remaining


# ============================================================
# CALCULATE RESULTS
# ============================================================

def calculate_results(
    questions,
    answers
):

    skill_marks = {}

    skill_totals = {}

    total_marks = 0


    for question in questions:

        skill = question["skill"]

        skill_totals[skill] = (
            skill_totals.get(
                skill,
                0
            ) + 1
        )

        skill_marks.setdefault(
            skill,
            0
        )


        selected_answer = answers.get(
            question["question"]
        )


        if selected_answer == question["answer"]:

            skill_marks[skill] += 1

            total_marks += 1


    skill_scores = {}


    for skill in skill_totals:

        marks = skill_marks.get(
            skill,
            0
        )

        total = skill_totals[skill]

        skill_scores[skill] = (
            marks / total
        ) * 100


    overall_percentage = (
        total_marks /
        TOTAL_MARKS
    ) * 100


    return (
        skill_marks,
        skill_scores,
        total_marks,
        overall_percentage
    )


# ============================================================
# SAVE RESULT TO MONGODB
# ============================================================

def save_result(
    skill_marks,
    skill_scores,
    total_marks,
    overall_percentage
):

    student = st.session_state.get(
        "student",
        {}
    )


    result_document = {

        "student_email":
            student.get(
                "email"
            ),

        "student_name":
            student.get(
                "name"
            ),

        "scores":
            skill_scores,

        "skill_marks":
            skill_marks,

        "overall_score":
            overall_percentage,

        "overall_marks":
            total_marks,

        "obtained_marks":
            total_marks,

        "attempt":
            st.session_state.get(
                "assessment_attempt",
                1
            ),

        "completed_at":
            datetime.now()
    }


    try:

        assessments_collection.insert_one(
            result_document
        )

    except Exception as error:

        st.error(
            f"Unable to save assessment result: {error}"
        )


# ============================================================
# SUBMIT ASSESSMENT
# ============================================================

def submit_assessment(
    auto_submitted=False
):

    questions = st.session_state.get(
        "assessment_questions",
        []
    )

    answers = st.session_state.get(
        "assessment_answers",
        {}
    )


    (
        skill_marks,
        skill_scores,
        total_marks,
        overall_percentage
    ) = calculate_results(
        questions,
        answers
    )


    # Store results.

    st.session_state[
        "assessment_marks"
    ] = skill_marks

    st.session_state[
        "assessment_scores"
    ] = skill_scores

    st.session_state[
        "overall_marks"
    ] = total_marks

    st.session_state[
        "overall_score"
    ] = overall_percentage

    st.session_state[
        "assessment_auto_submitted"
    ] = auto_submitted

    st.session_state[
        "assessment_submitted"
    ] = True

    st.session_state[
        "assessment_started"
    ] = False


    # Save to MongoDB.

    save_result(
        skill_marks,
        skill_scores,
        total_marks,
        overall_percentage
    )


    st.rerun()


# ============================================================
# RESULTS PAGE
# ============================================================

def show_results():

    st.title(
        "🎉 Assessment Results"
    )


    marks = st.session_state.get(
        "overall_marks",
        0
    )

    percentage = st.session_state.get(
        "overall_score",
        0
    )


    # --------------------------------------------------------
    # SUBMISSION MESSAGE
    # --------------------------------------------------------

    if st.session_state.get(
        "assessment_auto_submitted",
        False
    ):

        st.warning(
            "⏰ Time is over. Your assessment was submitted automatically."
        )

    else:

        st.success(
            "✅ Assessment submitted successfully!"
        )


    # --------------------------------------------------------
    # OVERALL RESULT
    # --------------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Marks Obtained",
            f"{int(marks)} / 20"
        )


    with col2:

        st.metric(
            "Percentage",
            f"{float(percentage):.0f}%"
        )


    st.markdown("---")


    # --------------------------------------------------------
    # SKILL-WISE RESULT
    # --------------------------------------------------------

    st.subheader(
        "📊 Skill-wise Performance"
    )


    skill_marks = st.session_state.get(
        "assessment_marks",
        {}
    )


    skill_scores = st.session_state.get(
        "assessment_scores",
        {}
    )


    skills = [
        "Python",
        "SQL",
        "DSA",
        "Machine Learning",
        "Problem Solving"
    ]


    columns = st.columns(5)


    for index, skill in enumerate(
        skills
    ):

        with columns[index]:

            skill_mark = int(
                skill_marks.get(
                    skill,
                    0
                )
            )

            skill_percentage = float(
                skill_scores.get(
                    skill,
                    0
                )
            )


            st.metric(
                skill,
                f"{skill_percentage:.0f}%"
            )


            st.caption(
                f"{skill_mark} / 4 marks"
            )


    st.markdown("---")


    # --------------------------------------------------------
    # BUTTONS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "🔄 Retest",
            type="primary",
            use_container_width=True
        ):

            start_new_assessment()


    with col2:

        if st.button(
            "🏠 Back to Dashboard",
            use_container_width=True
        ):

            st.session_state[
                "assessment_submitted"
            ] = False

            st.session_state[
                "assessment_started"
            ] = False

            st.session_state[
                "page"
            ] = "dashboard"

            st.rerun()


# ============================================================
# MAIN ASSESSMENT PAGE
# ============================================================

def skill_assessment_page():

    # --------------------------------------------------------
    # SHOW RESULTS IF SUBMITTED
    # --------------------------------------------------------

    if st.session_state.get(
        "assessment_submitted",
        False
    ):

        show_results()

        return


    # --------------------------------------------------------
    # SAFETY CHECK
    # --------------------------------------------------------

    if not st.session_state.get(
        "assessment_started",
        False
    ):

        st.session_state[
            "page"
        ] = "assessment_intro"

        st.rerun()

        return


    # --------------------------------------------------------
    # GET QUESTIONS
    # --------------------------------------------------------

    questions = st.session_state.get(
        "assessment_questions",
        []
    )


    if not questions:

        st.session_state[
            "page"
        ] = "assessment_intro"

        st.rerun()

        return


    # --------------------------------------------------------
    # PAGE HEADER
    # --------------------------------------------------------

    st.title(
        "📝 Skill Assessment"
    )


    st.caption(
        "20 questions • 20 marks • 20 minutes • 1 mark per question"
    )


    # --------------------------------------------------------
    # FIXED TIMER
    # --------------------------------------------------------

    remaining = display_timer()


    # --------------------------------------------------------
    # PROGRESS
    # --------------------------------------------------------

    answers = st.session_state.get(
        "assessment_answers",
        {}
    )


    answered_count = len(
        answers
    )


    st.progress(
        answered_count /
        TOTAL_QUESTIONS
    )


    st.caption(
        f"{answered_count} / {TOTAL_QUESTIONS} questions answered"
    )


    # --------------------------------------------------------
    # QUESTIONS
    # --------------------------------------------------------

    for index, question in enumerate(
        questions
    ):

        st.subheader(
            f"{index + 1}. {question['question']}"
        )


        st.caption(
            f"{question['skill']} • 1 mark"
        )


        # The attempt number is part of the key.
        #
        # Therefore a retest receives completely fresh
        # radio-button state.

        question_key = (
            f"assessment_"
            f"{st.session_state['assessment_attempt']}_"
            f"{index}"
        )


        options = [
            "Select an answer"
        ] + question["options"]


        selected_answer = st.radio(
            "Answer",

            options,

            index=0,

            key=question_key,

            label_visibility="collapsed"
        )


        # Never save the placeholder.

        if selected_answer != "Select an answer":

            answers[
                question["question"]
            ] = selected_answer

        else:

            answers.pop(
                question["question"],
                None
            )


        st.divider()


    # Save answers.

    st.session_state[
        "assessment_answers"
    ] = answers


    # --------------------------------------------------------
    # UNANSWERED COUNT
    # --------------------------------------------------------

    unanswered = (
        TOTAL_QUESTIONS -
        len(answers)
    )


    if unanswered > 0:

        st.warning(
            f"{unanswered} question(s) are unanswered."
        )


    # --------------------------------------------------------
    # SUBMIT BUTTON
    # --------------------------------------------------------

    if st.button(
        "✅ Submit Assessment",
        type="primary",
        use_container_width=True
    ):

        submit_assessment(
            auto_submitted=False
        )

        return


    # --------------------------------------------------------
    # TIME EXPIRED
    # --------------------------------------------------------

    if remaining <= 0:

        submit_assessment(
            auto_submitted=True
        )

        return


    # --------------------------------------------------------
    # TIMER REFRESH
    # --------------------------------------------------------

    try:

        from streamlit_autorefresh import (
            st_autorefresh
        )


        st_autorefresh(
            interval=1000,

            key=(
                "assessment_timer_"
                f"{st.session_state['assessment_attempt']}"
            )
        )


    except ImportError:

        st.error(
            "The timer refresh package is not installed."
        )

        st.code(
            "pip install streamlit-autorefresh"
        )