def explain_eligibility(eligibility_results):
    explanations = []

    for result in eligibility_results:
        text = (
            f"{result['course_id']} - "
            f"{result['course_name']}: "
            f"{result['reason']}"
        )

        explanations.append(text)

    return explanations


def explain_plan(plan, courses, student):
    explanations = []
    total_credits = 0
    used_slots = []

    for course_id, slot in plan.items():
        if slot == "NOT_SELECTED":
            continue

        course = courses[course_id]
        total_credits += course.credits
        used_slots.append(slot)

    # Credit explanation
    explanations.append(
        f"Total credits = {total_credits}, "
        f"which is within the maximum limit "
        f"of {student.max_credits}."
    )

    # Blocked slot explanation
    blocked_used = False

    for slot in used_slots:
        if slot in student.blocked_slots:
            blocked_used = True

    if not blocked_used:
        explanations.append("No selected course uses a blocked time slot.")

    # Time conflict explanation

    if len(used_slots) == len(set(used_slots)):
        explanations.append("No two selected courses have the same time slot.")

    # Selected courses explanation
    selected_courses = []

    for course_id, slot in plan.items():
        
        if slot != "NOT_SELECTED":
            selected_courses.append(course_id)

    explanations.append("Selected courses: " + ", ".join(selected_courses))

    return explanations


def explain_ranked_plan(ranked_result):
    explanations = []
    score = ranked_result["score"]

    explanations.append(f"Preference score = {score}.")

    if ranked_result["reasons"]:
        for reason in ranked_result["reasons"]:
            explanations.append(reason)
    else:
        explanations.append("No special student preferences were matched.")

    return explanations


def explain_no_solution(csp, courses, student):
    reasons = []

    # Check whether any mandatory course
    # has all its available slots blocked
    for course_id in csp.variables:
        course = courses[course_id]

        if course.course_type != "mandatory":
            continue

        available_slots = course.offered_slots
        usable_slots = []

        for slot in available_slots:
            if slot not in student.blocked_slots:
                usable_slots.append(slot)

        if len(usable_slots) == 0:
            reasons.append(
                f"{course_id} is mandatory, but all "
                f"its available slots are blocked."
            )

    # Check whether the minimum mandatory
    # credit requirement already exceeds
    # the student's maximum credit limit
    mandatory_credits = 0

    for course_id in csp.variables:
        course = courses[course_id]
        
        if course.course_type == "mandatory":
            mandatory_credits += course.credits

    if mandatory_credits > student.max_credits:

        reasons.append(
            f"Mandatory courses require "
            f"{mandatory_credits} credits, but the "
            f"maximum allowed is {student.max_credits}."
        )

    if not reasons:
        reasons.append("No feasible combination satisfies all current hard constraints.")

    return reasons