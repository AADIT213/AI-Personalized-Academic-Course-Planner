# 🎓 AI-Based Personalized Academic Course Planner

### 🤖 Hybrid AI using Rule-Based Reasoning and Constraint Satisfaction

> **A Semester-5 Artificial Intelligence Innovative Assignment** implemented in **Python + Streamlit**

## 🚀 Live Demo

[![Open Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-personalized-academic-course-planner.streamlit.app)
---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [AI Techniques Used](#-ai-techniques-used)
- [System Workflow](#-system-workflow)
- [Student Inputs](#-student-inputs)
- [Knowledge Base](#-knowledge-base)
- [CSP Formulation Example](#-csp-formulation-example)
- [Solver Comparison](#-solver-comparison)
- [Project Structure](#-project-structure)
- [Module Description](#-module-description)
- [Installation](#-installation)
- [Running the Application](#-running-the-application)
- [Running the Tests](#-running-the-tests)
- [Demonstration Scenarios](#-demonstration-scenarios)
- [Testing and Validation](#-testing-and-validation)
- [Design Principles](#-design-principles)
- [Key Learning Outcomes](#-key-learning-outcomes)
- [Future Scope](#-future-scope)
- [Academic Note](#-academic-note)
- [Authors](#-authors)

---

## 🚀 Project Overview

Academic course planning involves several conditions that must be satisfied simultaneously:

- ✅ Course prerequisites must be satisfied
- ✅ Courses must belong to the appropriate semester
- ✅ Total credits must remain within the student's limit
- ✅ Blocked time slots must not be used
- ✅ Two courses must not occupy the same time slot
- ✅ The final plan should reflect the student's specialization and time preferences

### 🧠 Hybrid AI Approach

This project models the problem as a **Hybrid AI system**:

1. **Rule Engine** → Determines course eligibility using custom rules
2. **CSP Formulation** → Eligible Semester-5 courses become a Constraint Satisfaction Problem
3. **Three CSP Solvers** → Generate feasible plans using different strategies
4. **Preference Ranking** → Ranks plans based on student preferences
5. **Explainability** → Provides clear explanations for all decisions

---

## 🧩 AI Techniques Used

### 📜 Rule-Based Reasoning

Four explicit eligibility rules are implemented:

| Rule | Condition | Outcome |
|------|-----------|---------|
| **Rule 1** | Already completed course | ❌ Ineligible |
| **Rule 2** | Course from different semester | ❌ Ineligible |
| **Rule 3** | Missing prerequisite | ❌ Ineligible |
| **Rule 4** | All requirements satisfied | ✅ Eligible |

### 🎯 Constraint Satisfaction Problem (CSP)

For the Semester-5 planning cycle:

- **Variables**: Course IDs
- **Domains**: Available course time slots
- **Elective Domain**: Includes `NOT_SELECTED` option

### 🔍 CSP Solvers

Three solvers are implemented **manually**:

1. **Basic Backtracking** → Standard backtracking search
2. **Backtracking + MRV** → Minimum Remaining Values heuristic
3. **MRV + Forward Checking** → MRV with constraint propagation

### ⚙️ Hard Constraints

- 📊 Maximum credit limit
- 🚫 Blocked time slots
- ⏰ Timetable conflicts (no overlapping courses)

### 🏆 Preference Ranking

After feasible plans are generated:

| Preference | Score |
|------------|-------|
| Specialization match | +10 |
| Preferred time slot | +5 |

> ⚠️ Preferences are used **only for ranking** feasible plans; they do **not** override hard constraints.

### 💡 Explainability

The application explains:

- ❓ Why a course is eligible or rejected
- ❓ Why a plan is valid
- ❓ Why a plan received its preference score
- ❓ Common no-solution conflicts

---

## 🔄 System Workflow

```
👤 Student Profile
        ↓
📦 JSON Knowledge Base
        ↓
📜 Rule-Based Eligibility Reasoning
        ↓
✅ Eligible Semester-5 Courses
        ↓
🎯 CSP Formulation
        ↓
   ┌─────────────────────┬─────────────────────┬─────────────────────────┐
   │ Basic Backtracking  │ Backtracking + MRV  │ MRV + Forward Checking  │
   └─────────────────────┴─────────────────────┴─────────────────────────┘
        ↓
📋 Feasible Academic Plans
        ↓
🏆 Preference Evaluation
        ↓
📊 Ranked Plans
        ↓
💡 Explanations
        ↓
🖥️ Streamlit Interface
```

---

## 📝 Student Inputs

The Streamlit application accepts:

| Input | Purpose |
|-------|---------|
| 📚 Current semester | Determines planning cycle |
| ✅ Completed courses | Affects prerequisite satisfaction |
| 📊 Maximum credits | Hard constraint for CSP |
| 🎯 Preferred specialization | Preference ranking (+10) |
| ⏰ Preferred time slots | Preference ranking (+5) |
| 🚫 Blocked time slots | Hard constraint (unavailable) |

---

## 📚 Knowledge Base

Course information is stored in: `data/courses.json`

### Course Catalogue

The demonstration catalogue contains **30 subjects** from Semester 1 to Semester 5.

### Semester-5 Demonstration Courses

| Course ID | Course | Credits | Type | Specialization |
|-----------|--------|---------|------|----------------|
| AI301 | Artificial Intelligence | 4 | Mandatory | AI |
| CMAI301 | Computational Mathematics for AIML | 4 | Mandatory | Mathematics |
| DL301 | Deep Learning | 4 | Mandatory | AI |
| OST301 | Open Source Technology | 4 | Elective | Software |
| DCN301 | Data Communication & Networking | 4 | Mandatory | Networks |
| BDS301 | Big Data System | 4 | Mandatory | Data |

> ⚠️ **Note**: The prerequisite relationships in this project are **project-defined rules** created to demonstrate AI reasoning. They are **not** claimed to be official university prerequisite regulations.

---

## 🎲 Example CSP Formulation

An eligible course becomes a CSP variable and its available time slots form its domain:

```
AI301    → [MON-09, WED-11]
CMAI301  → [TUE-10, THU-10]
DL301    → [MON-09, THU-14]
OST301   → [TUE-10, FRI-10, NOT_SELECTED]
DCN301   → [THU-14, FRI-11]
BDS301   → [WED-11, FRI-14]
```

The solver searches for assignments that satisfy **all hard constraints**.

---

## 📊 Solver Comparison

The same CSP instance is solved using three different strategies:

| Solver | Main Strategy |
|--------|---------------|
| **Basic Backtracking** | Assign variables in normal order and backtrack when a constraint fails |
| **Backtracking + MRV** | Select the unassigned variable with the smallest legal domain |
| **MRV + Forward Checking** | Use MRV and prune invalid values from future domains |

### Performance Metrics

The application records:

- 🔢 Nodes explored
- 🔄 Backtracks
- ⏱️ Execution time
- ✅ Solutions found
- ✂️ Forward Checking pruning events

### Reference Run Results

For the normal demonstration profile, one verified execution produced:

| Solver | Nodes Explored | Backtracks | Pruning | Solutions |
|--------|----------------|------------|---------|-----------|
| **Basic Backtracking** | 102 | 0 | N/A | 25 |
| **Backtracking + MRV** | 56 | 0 | N/A | 25 |
| **MRV + Forward Checking** | 48 | 0 | 7 | 25 |

> ⚠️ **Note**: Execution time is intentionally not fixed in this table because it depends on the machine and individual run.

---

## 📁 Project Structure

```
ai-course-planner/
│
├── app.py                    # Streamlit UI & workflow
├── requirements.txt          # Dependencies
├── README.md                 # Project documentation
│
├── data/
│   ├── courses.json          # Course catalogue
│   ├── sample_students.json  # Sample student profiles
│   └── sample_scenarios.json # Test scenarios
│
├── src/
│   ├── __init__.py
│   ├── models.py             # Data structures
│   ├── knowledge_base.py     # JSON data loader
│   ├── rules.py              # Eligibility rules
│   ├── inference_engine.py   # Rule application
│   ├── csp.py                # CSP formulation
│   ├── constraints.py        # Constraint checking
│   ├── solvers.py            # CSP search strategies
│   ├── evaluator.py          # Preference scoring
│   └── explanations.py       # Human-readable explanations
│
├── tests/
│   ├── __init__.py
│   ├── test_rules.py
│   ├── test_constraints.py
│   ├── test_solver.py
│   └── test_scenarios.py
│
└── outputs/
    └── screenshots/          # Documentation images
```

---

## 📦 Module Description

| File | Purpose |
|------|---------|
| `app.py` | Streamlit user interface and complete application workflow |
| `models.py` | Course and StudentProfile data structures |
| `knowledge_base.py` | Loads course and student data from JSON |
| `rules.py` | Defines course eligibility rules |
| `inference_engine.py` | Applies rules to determine eligibility |
| `csp.py` | Builds CSP variables and domains |
| `constraints.py` | Checks credit, blocked-slot and timetable constraints |
| `solvers.py` | Implements the three CSP search strategies |
| `evaluator.py` | Calculates preference scores and ranks plans |
| `explanations.py` | Produces human-readable explanations |

---

## 🛠️ Installation

### Requirements

- 🐍 Python 3.x
- 📦 pip

### Dependencies

The application uses:

- `streamlit`

### Install Command

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

1. Open a terminal in the project root
2. Run the following command:

```bash
streamlit run app.py
```

3. Streamlit will display a local URL in the terminal
4. Open that URL in your browser

---

## 🧪 Running the Tests

The project includes a **unittest suite** covering rules, constraints, solver consistency, and scenarios.

### Run Command

```bash
python -m unittest discover -s tests -v
```

### Expected Output

```
Ran 8 tests
OK
```

> ✅ The tests are separate from the main application and validate the implementation.

---

## 🎭 Demonstration Scenarios

The project contains predefined scenarios in: `data/sample_scenarios.json`

### Scenario 1 — Normal Feasible Case ✅

A normal Semester-5 student profile produces feasible academic plans.

### Scenario 2 — Missing Prerequisite ❌

Removing `ML202` from completed courses causes `DL301` to become **ineligible** because its prerequisite is missing.

### Scenario 3 — Credit Limit Conflict ⚠️

A maximum credit limit of **16** is insufficient for mandatory Semester-5 courses, producing **no feasible plan**.

### Scenario 4 — Blocked Mandatory Course 🚫

Blocking both available slots of `AI301` makes the mandatory course **impossible to schedule**.

### Scenario 5 — Preference Variation 🏆

Changing preferred specialization and time slot changes the **preference ranking** of feasible plans.

---

## ✅ Testing and Validation

The project currently contains **8 unit tests** covering:

- ✅ Course eligibility
- ✅ Missing prerequisites
- ✅ Blocked time slots
- ✅ Timetable conflicts
- ✅ Credit limits
- ✅ Solver consistency
- ✅ Forward Checking pruning
- ✅ Predefined scenarios

**The complete test suite passes successfully.**

---

## 🎨 Design Principles

The implementation intentionally remains **simple and modular** for a Semester-5 Artificial Intelligence project.

### What This Project Does NOT Use

- ❌ Machine-learning models
- ❌ External AI APIs
- ❌ Databases
- ❌ Prolog
- ❌ Complex optimization frameworks
- ❌ External CSP libraries

### Why?

The major AI techniques are implemented **directly in Python** so that the logic remains **transparent and easy to explain** during evaluation or viva.

---

## 🎯 Key Learning Outcomes

This project demonstrates practical understanding of:

- 🧠 Knowledge representation
- 📜 Rule-based inference
- 🎯 Constraint Satisfaction Problems (CSP)
- 🔁 Backtracking search
- 🎲 Heuristic search using MRV
- 🔍 Constraint propagation using Forward Checking
- 🏆 Preference-based reasoning
- 💡 Explainable AI (XAI) concepts
- 🐍 Modular Python development
- 🖥️ Streamlit-based AI application development
- 🧪 Unit testing and validation

---

## 🔮 Future Scope

Possible extensions include:

- 📚 More semesters and larger course catalogues
- ⚙️ Additional academic constraints
- 👨‍🏫 Faculty or room availability
- 🎯 More sophisticated preference models
- 📅 Multi-semester planning
- 📊 Visualization of CSP search
- 🌐 Deployment as a web application

> ⚠️ These extensions are **outside the current project scope**.

---

## 📖 Academic Note

> This project is developed as an **Artificial Intelligence Innovative Assignment** for **Semester 5**.

The system is intended as an **educational demonstration** of:

- Hybrid AI
- Rule-based reasoning
- CSP-based academic planning

The course prerequisite relationships and planning constraints are **project-defined demonstration data** unless explicitly stated otherwise.

---

## 👨‍💻 Authors

| Name |
|------|
| **Aadit Shah** |
| **Ayush Tiwari** |

---

<div align="center">

### 🌟 Made with ❤️ using Python + Streamlit

**AI-Based Personalized Academic Course Planner** | Semester 5 AI Project

</div>
