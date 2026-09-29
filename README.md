AI-Based Personalized Academic Course Planner

Hybrid AI using Rule-Based Reasoning and Constraint Satisfaction

A Semester-5 Artificial Intelligence Innovative Assignment implemented in Python + Streamlit.

The system generates valid and personalized academic course plans by combining rule-based reasoning, Constraint Satisfaction Problems (CSP), Backtracking, Minimum Remaining Values (MRV), Forward Checking, preference-based ranking, and explainable output.

1. Project Overview

Academic course planning involves several conditions that must be satisfied at the same time:

Course prerequisites must be satisfied.

Courses must belong to the appropriate semester.

The total credits must remain within the student's limit.

Blocked time slots must not be used.

Two courses must not occupy the same time slot.

The final plan should reflect the student's specialization and time preferences.

This project models the problem as a Hybrid AI system.

The application first uses a custom rule engine to determine course eligibility. The eligible Semester-5 courses are then formulated as a Constraint Satisfaction Problem. Three manually implemented CSP solvers generate feasible plans, after which the plans are ranked using simple student preferences.

The application also provides explanations for eligibility decisions, plan validity, preference scores, and selected no-solution conflicts.

2. AI Techniques Used

Rule-Based Reasoning

Four explicit eligibility rules are used:

Already completed course → Ineligible

Course from a different semester → Ineligible

Missing prerequisite → Ineligible

Requirements satisfied → Eligible

Constraint Satisfaction Problem

For the Semester-5 planning cycle:

Variables: Course IDs

Domains: Available course time slots

Elective domain: Includes NOT_SELECTED

CSP Solvers

Three solvers are implemented manually:

Basic Backtracking

Backtracking + Minimum Remaining Values (MRV)

MRV + Forward Checking

Hard Constraints

Maximum credit limit

Blocked time slots

Timetable conflicts

Preference Ranking

After feasible plans are generated:

Specialization match → +10

Preferred time slot → +5

Preferences are used only for ranking feasible plans; they do not override hard constraints.

Explainability

The application explains:

Why a course is eligible or rejected

Why a plan is valid

Why a plan received its preference score

Some common no-solution conflicts

3. System Workflow

Student Profile
      ↓
JSON Knowledge Base
      ↓
Rule-Based Eligibility Reasoning
      ↓
Eligible Semester-5 Courses
      ↓
CSP Formulation
      ↓
 ┌─────────────────────┬─────────────────────┬─────────────────────────┐
 │ Basic Backtracking  │ Backtracking + MRV  │ MRV + Forward Checking  │
 └─────────────────────┴─────────────────────┴─────────────────────────┘
      ↓
Feasible Academic Plans
      ↓
Preference Evaluation
      ↓
Ranked Plans
      ↓
Explanations
      ↓
Streamlit Interface

4. Student Inputs

The Streamlit application accepts:

Current semester

Completed courses

Maximum credits

Preferred specialization

Preferred time slots

Blocked time slots

These inputs influence eligibility, CSP feasibility, or plan ranking.

5. Knowledge Base

Course information is stored in:

data/courses.json

The demonstration catalogue contains 30 subjects from Semester 1 to Semester 5.

Earlier-semester subjects are mainly used as completed-course and prerequisite knowledge, while Semester 5 is the main planning cycle.

Semester-5 demonstration courses include:

Course ID

Course

Credits

Type

Specialization

AI301

Artificial Intelligence

4

Mandatory

AI

CMAI301

Computational Mathematics for AIML

4

Mandatory

Mathematics

DL301

Deep Learning

4

Mandatory

AI

OST301

Open Source Technology

4

Elective

Software

DCN301

Data Communication & Networking

4

Mandatory

Networks

BDS301

Big Data System

4

Mandatory

Data

Note: The prerequisite relationships in this project are project-defined rules created to demonstrate AI reasoning. They are not claimed to be official university prerequisite regulations.

6. Example CSP Formulation

An eligible course becomes a CSP variable and its available time slots form its domain.

AI301    → [MON-09, WED-11]
CMAI301  → [TUE-10, THU-10]
DL301    → [MON-09, THU-14]
OST301   → [TUE-10, FRI-10, NOT_SELECTED]
DCN301   → [THU-14, FRI-11]
BDS301   → [WED-11, FRI-14]

The solver searches for assignments that satisfy all hard constraints.

7. Solver Comparison

The same CSP instance is solved using three different strategies.

Solver

Main Strategy

Basic Backtracking

Assign variables in normal order and backtrack when a constraint fails

Backtracking + MRV

Select the unassigned variable with the smallest legal domain

MRV + Forward Checking

Use MRV and prune invalid values from future domains

The application records:

Nodes explored

Backtracks

Execution time

Solutions found

Forward Checking pruning events

Reference Run

For the normal demonstration profile, one verified execution produced:

Solver

Nodes Explored

Backtracks

Pruning

Solutions

Basic Backtracking

102

0

N/A

25

Backtracking + MRV

56

0

N/A

25

MRV + Forward Checking

48

0

7

25

Execution time is intentionally not fixed in this table because it depends on the machine and individual run.

8. Project Structure

ai-course-planner/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── courses.json
│   ├── sample_students.json
│   └── sample_scenarios.json
│
├── src/
│   ├── __init__.py
│   ├── models.py
│   ├── knowledge_base.py
│   ├── rules.py
│   ├── inference_engine.py
│   ├── csp.py
│   ├── constraints.py
│   ├── solvers.py
│   ├── evaluator.py
│   └── explanations.py
│
├── tests/
│   ├── __init__.py
│   ├── test_rules.py
│   ├── test_constraints.py
│   ├── test_solver.py
│   └── test_scenarios.py
│
└── outputs/
    └── screenshots/

9. Module Description

File

Purpose

app.py

Streamlit user interface and complete application workflow

models.py

Course and StudentProfile data structures

knowledge_base.py

Loads course and student data from JSON

rules.py

Defines course eligibility rules

inference_engine.py

Applies rules to determine eligibility

csp.py

Builds CSP variables and domains

constraints.py

Checks credit, blocked-slot and timetable constraints

solvers.py

Implements the three CSP search strategies

evaluator.py

Calculates preference scores and ranks plans

explanations.py

Produces human-readable explanations

10. Installation

Requirements

Python 3.x

pip

The application uses:

streamlit

Install dependencies using:

pip install -r requirements.txt

11. Running the Application

Open a terminal in the project root:

streamlit run app.py

Streamlit will display a local URL in the terminal. Open that URL in a browser.

12. Running the Tests

The project includes a small unittest suite covering rules, constraints, solver consistency and scenarios.

Run:

python -m unittest discover -s tests -v

Expected result:

Ran 8 tests
OK

The tests are separate from the main application and are included to validate the implementation.

13. Demonstration Scenarios

The project contains predefined scenarios in:

data/sample_scenarios.json

Scenario 1 — Normal Feasible Case

A normal Semester-5 student profile produces feasible academic plans.

Scenario 2 — Missing Prerequisite

Removing ML202 from the completed courses causes DL301 to become ineligible because its prerequisite is missing.

Scenario 3 — Credit Limit Conflict

A maximum credit limit of 16 is insufficient for the mandatory Semester-5 courses, producing no feasible plan.

Scenario 4 — Blocked Mandatory Course

Blocking both available slots of AI301 makes the mandatory course impossible to schedule.

Scenario 5 — Preference Variation

Changing the preferred specialization and time slot changes the preference ranking of feasible plans.

14. Screenshots

Application screenshots used for the project documentation are stored under:

outputs/screenshots/

Recommended evidence includes:

Main Streamlit interface

Eligibility analysis

CSP formulation

Solver comparison

Personalized academic plans

Plan explanation

Missing-prerequisite scenario

No-solution scenario

Unit test execution

15. Testing and Validation

The project currently contains 8 unit tests covering:

Course eligibility

Missing prerequisites

Blocked time slots

Timetable conflicts

Credit limits

Solver consistency

Forward Checking pruning

Predefined scenarios

The complete test suite passes successfully.

16. Design Principles

The implementation intentionally remains simple and modular for a Semester-5 Artificial Intelligence project.

The project does not use:

Machine-learning models

External AI APIs

Databases

Prolog

Complex optimization frameworks

External CSP libraries

The major AI techniques are implemented directly in Python so that the logic remains transparent and easy to explain during evaluation or viva.

17. Key Learning Outcomes

This project demonstrates practical understanding of:

Knowledge representation

Rule-based inference

Constraint Satisfaction Problems

Backtracking search

Heuristic search using MRV

Constraint propagation using Forward Checking

Preference-based reasoning

Explainable AI concepts

Modular Python development

Streamlit-based AI application development

Unit testing and validation

18. Future Scope

Possible extensions include:

More semesters and larger course catalogues

Additional academic constraints

Faculty or room availability

More sophisticated preference models

Multi-semester planning

Visualization of CSP search

Deployment as a web application

These extensions are outside the current project scope.

19. Academic Note

This project is developed as an Artificial Intelligence Innovative Assignment for Semester 5.

The system is intended as an educational demonstration of Hybrid AI, rule-based reasoning and CSP-based academic planning. The course prerequisite relationships and planning constraints are project-defined demonstration data unless explicitly stated otherwise.

Author(s)

Aadit Shah
Ayush Tiwari