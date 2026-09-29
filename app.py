import streamlit as st

from src.models import StudentProfile
from src.knowledge_base import KnowledgeBase
from src.inference_engine import InferenceEngine
from src.csp import build_course_csp
from src.solvers import (backtracking_solver, mrv_backtracking_solver, forward_checking_solver)
from src.evaluator import rank_plans
from src.explanations import (explain_plan, explain_ranked_plan, explain_no_solution)

# PAGE SETTINGS
st.set_page_config(page_title="AI Academic Course Planner", layout = "wide")
st.title("AI-Based Personalized Academic Course Planner")
st.write("Hybrid AI using Rule-Based Reasoning and Constraint Satisfaction")
st.caption("Semester-wise personalized course planning with explainable CSP search")

# LOAD COURSE KNOWLEDGE BASE
kb = KnowledgeBase("data/courses.json")
courses = kb.load_courses()
course_ids = list(courses.keys())

# Collect all available time slots
all_slots = []

for course in courses.values():
    for slot in course.offered_slots:
        if slot not in all_slots:
            all_slots.append(slot)

# Collect specializations
specializations = []
for course in courses.values():
    if (course.specialization and course.specialization not in specializations):
        specializations.append(course.specialization)

# STUDENT INPUT
st.sidebar.header("Student Profile")
student_id = st.sidebar.text_input("Student ID", "24BAM005")
semester = st.sidebar.number_input("Current Semester", min_value = 1,
                                   max_value = 8, value = 5)

default_completed = []

for course in courses.values():
    
    if course.semester < semester:
        default_completed.append(course.course_id)

completed_courses = st.sidebar.multiselect("Completed Courses", course_ids,
                                           default = default_completed,
                                           format_func = lambda course_id: (
                                               f"{course_id} - "
                                               f"{courses[course_id].name}"))

max_credits = st.sidebar.slider("Maximum Credits", min_value = 4, max_value = 28,
                                value = 24, step = 4)

preferred_specialization = (st.sidebar.selectbox("Preferred Specialization",
                                                 ["None"] + specializations))

default_preferred_slots = ["MON-09", "THU-14"]
default_preferred_slots = [slot for slot in default_preferred_slots
                           if slot in all_slots]

preferred_slots = st.sidebar.multiselect("Preferred Time Slots",
                                         all_slots, default = default_preferred_slots)

blocked_slots = st.sidebar.multiselect("Blocked Time Slots", all_slots)
generate_button = st.sidebar.button("Generate Academic Plan")

# GENERATE PLAN
if generate_button:
    # Create student profile
    if preferred_specialization == "None":
        preferred_specialization = ""

    student = StudentProfile(
        student_id = student_id,
        semester = semester,
        completed_courses = completed_courses,
        max_credits = max_credits,
        preferred_specialization = (preferred_specialization),
        preferred_slots = preferred_slots,
        blocked_slots = blocked_slots
    )

    # RULE-BASED ELIGIBILITY
    engine = InferenceEngine(courses)
    eligibility_results = (engine.evaluate_all_courses(student))

    st.header("1. Eligibility Analysis")

    eligibility_table = []
    for result in eligibility_results:
        course = courses[result["course_id"]]

        if course.semester == student.semester:
            eligibility_table.append(
            {"Course": result["course_id"], "Course Name": result["course_name"],
             "Status": result["status"], "Reason": result["reason"]})

    st.table(eligibility_table)

    # BUILD CSP

    csp = build_course_csp(courses, eligibility_results)
    st.header("2. CSP Formulation")

    for variable in csp.variables:
        st.write(variable, "→", csp.domains[variable])

    # RUN ALL THREE SOLVERS
    basic_solutions, basic_metrics = (backtracking_solver(csp, courses, student))
    mrv_solutions, mrv_metrics = (mrv_backtracking_solver(csp, courses, student))
    fc_solutions, fc_metrics = (forward_checking_solver(csp, courses, student))

    # SOLVER COMPARISON
    st.header("3. Solver Comparison")
    
    solver_table = [
        {
            "Solver": "Basic Backtracking",
            "Nodes": basic_metrics[
                "nodes_explored"
            ],
            "Backtracks": basic_metrics[
                "backtracks"
            ],
            "Pruning": "N/A",
            "Solutions": basic_metrics[
                "solutions_found"
            ],
            "Time (seconds)": round(
                basic_metrics[
                    "execution_time"
                ],
                6
            )
        },
        {
            "Solver": "Backtracking + MRV",
            "Nodes": mrv_metrics[
                "nodes_explored"
            ],
            "Backtracks": mrv_metrics[
                "backtracks"
            ],
            "Pruning": "N/A",
            "Solutions": mrv_metrics[
                "solutions_found"
            ],
            "Time (seconds)": round(
                mrv_metrics[
                    "execution_time"
                ],
                6
            )
        },
        {
            "Solver": (
                "MRV + Forward Checking"
            ),
            "Nodes": fc_metrics[
                "nodes_explored"
            ],
            "Backtracks": fc_metrics[
                "backtracks"
            ],
            "Pruning": fc_metrics[
                "pruning_events"
            ],
            "Solutions": fc_metrics[
                "solutions_found"
            ],
            "Time (seconds)": round(
                fc_metrics[
                    "execution_time"
                ],
                6
            )
        }
    ]

    st.table(solver_table)

    # CORRECTNESS CHECK
    if (len(basic_solutions) == len(mrv_solutions) == len(fc_solutions)):
        st.success("All three solvers found the same number of solutions.")
    else:
        st.warning("Solver results are different.")

    # RANK PLANS
    ranked_plans = rank_plans(fc_solutions, courses, student)

    st.header("4. Personalized Academic Plans")

    # NO SOLUTION
    if not ranked_plans:
        st.error("No feasible academic plan found.")

        conflict_reasons = (explain_no_solution(csp, courses, student))
        st.subheader("Conflict Explanation")

        for reason in conflict_reasons:
            st.write("•", reason)

    # SHOW TOP PLANS
    else:
        # Show only top 5
        top_plans = ranked_plans[:5]

        for rank, result in enumerate(top_plans, start = 1):
            with st.expander(f"Plan {rank} " f"- Preference Score: " f"{result['score']}"):
                total_credits = 0
                
                for course_id, slot in (result["plan"].items()):
                    if slot == "NOT_SELECTED":
                        st.write(course_id, "→ Not Selected")
                    else:
                        st.write(course_id, "→", slot)
                        total_credits += (courses[course_id].credits)

                st.write("Total Credits:", total_credits)
                st.subheader("Why is this plan valid?")

                plan_explanations = (explain_plan(result["plan"], courses, student))

                for explanation in (plan_explanations):
                    st.write("•", explanation)

                st.subheader("Why this preference score?")

                ranking_explanations = (explain_ranked_plan(result))

                for explanation in (ranking_explanations):
                    st.write("•", explanation)