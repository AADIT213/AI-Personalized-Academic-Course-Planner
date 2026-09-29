import time
from src.constraints import is_valid_assignment

# V1 - BASIC BACKTRACKING

def backtracking_solver(csp, courses, student):
    solutions = []

    metrics = {
        "nodes_explored": 0,
        "backtracks": 0,
        "solutions_found": 0,
        "execution_time": 0
    }

    start_time = time.perf_counter()

    def backtrack(assignment):
        # Complete solution found
        if len(assignment) == len(csp.variables):

            solutions.append(assignment.copy())
            metrics["solutions_found"] += 1

            return

        # Select first unassigned variable
        for variable in csp.variables:

            if variable not in assignment:
                current_variable = variable

                break

        solution_found_from_here = False

        # Try all values
        for value in csp.domains[current_variable]:
            metrics["nodes_explored"] += 1

            if is_valid_assignment(current_variable, value, assignment, courses, student):
                assignment[current_variable] = value
                solutions_before = len(solutions)
                backtrack(assignment)

                if len(solutions) > solutions_before:
                    solution_found_from_here = True

                del assignment[current_variable]

        if not solution_found_from_here:
            metrics["backtracks"] += 1

    backtrack({})

    end_time = time.perf_counter()

    metrics["execution_time"] = (end_time - start_time)

    return solutions, metrics


# MRV VARIABLE SELECTION
def select_mrv_variable(csp, assignment, courses, student):

    best_variable = None
    smallest_legal_domain = float("inf")

    for variable in csp.variables:
        # Ignore already assigned variables
        if variable in assignment:
            continue

        legal_values = 0

        # Count currently valid values
        for value in csp.domains[variable]:

            if is_valid_assignment(variable, value, assignment, courses, student):
                legal_values += 1

        # Keep variable with minimum legal values
        if legal_values < smallest_legal_domain:

            smallest_legal_domain = legal_values
            best_variable = variable

    return best_variable

# V2 - BACKTRACKING + MRV
def mrv_backtracking_solver(csp, courses, student):
    solutions = []

    metrics = {
        "nodes_explored": 0,
        "backtracks": 0,
        "solutions_found": 0,
        "execution_time": 0
    }

    start_time = time.perf_counter()

    def backtrack(assignment):

        # Complete solution found
        if len(assignment) == len(csp.variables):
            solutions.append(assignment.copy())
            metrics["solutions_found"] += 1

            return

        # MRV chooses the most constrained variable
        current_variable = select_mrv_variable(csp, assignment, courses, student)
        solution_found_from_here = False

        # Try all values
        for value in csp.domains[current_variable]:
            metrics["nodes_explored"] += 1

            if is_valid_assignment(current_variable, value, assignment, courses, student):
                assignment[current_variable] = value
                solutions_before = len(solutions)
                backtrack(assignment)

                if len(solutions) > solutions_before:
                    solution_found_from_here = True

                del assignment[current_variable]

        if not solution_found_from_here:
            metrics["backtracks"] += 1

    backtrack({})

    end_time = time.perf_counter()

    metrics["execution_time"] = (end_time - start_time)

    return solutions, metrics

# =========================================================
# FORWARD CHECKING
# =========================================================

def forward_check(
    csp,
    assignment,
    current_domains,
    courses,
    student
):

    # Create a copy of current domains
    new_domains = {}

    for variable in current_domains:
        new_domains[variable] = (current_domains[variable].copy())

    pruning_count = 0

    # Check future unassigned variables
    for variable in csp.variables:

        if variable in assignment:
            continue

        valid_values = []

        for value in new_domains[variable]:

            if is_valid_assignment(
                variable,
                value,
                assignment,
                courses,
                student
            ):

                valid_values.append(value)

            else:

                pruning_count += 1

        new_domains[variable] = valid_values

        # If any future variable has no value,
        # this branch cannot produce a solution.
        if len(valid_values) == 0:

            return None, pruning_count

    return new_domains, pruning_count

# MRV USING CURRENT DOMAINS
def select_mrv_from_domains(csp, assignment, current_domains):
    best_variable = None
    smallest_domain = float("inf")

    for variable in csp.variables:

        if variable in assignment:
            continue

        domain_size = len(current_domains[variable])

        if domain_size < smallest_domain:
            smallest_domain = domain_size
            best_variable = variable

    return best_variable

# V3 - MRV + FORWARD CHECKING
def forward_checking_solver(csp, courses, student):
    solutions = []

    metrics = {
        "nodes_explored": 0,
        "backtracks": 0,
        "solutions_found": 0,
        "pruning_events": 0,
        "execution_time": 0
    }

    start_time = time.perf_counter()

    # Initial domain copy
    initial_domains = {}

    for variable in csp.variables:
        initial_domains[variable] = (csp.domains[variable].copy())

    def backtrack(assignment, current_domains):
        # Complete solution found
        if len(assignment) == len(csp.variables):

            solutions.append(assignment.copy())
            metrics["solutions_found"] += 1

            return

        # Select variable using MRV
        current_variable = (select_mrv_from_domains(csp, assignment, current_domains))
        solution_found_from_here = False

        # Try available values
        for value in current_domains[current_variable]:
            metrics["nodes_explored"] += 1

            if is_valid_assignment(current_variable, value, assignment, courses, student):
                assignment[current_variable] = value

                solutions_before = len(solutions)

                # Perform forward checking
                new_domains, pruned = (
                    forward_check(csp, assignment, current_domains, courses, student)
                    )

                metrics["pruning_events"] += pruned

                # Continue only if future
                # domains are still possible
                if new_domains is not None:
                    backtrack(assignment, new_domains)
                    
                if (len(solutions) > solutions_before):
                    solution_found_from_here = True

                del assignment[current_variable]

        if not solution_found_from_here:
            metrics["backtracks"] += 1

    backtrack({}, initial_domains)

    end_time = time.perf_counter()

    metrics["execution_time"] = (end_time - start_time)

    return solutions, metrics