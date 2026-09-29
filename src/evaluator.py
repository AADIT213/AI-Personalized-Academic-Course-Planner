def evaluate_plan(plan, courses, student):
    score = 0
    reasons = []
    
    for course_id, slot in plan.items():
        # Ignore electives that were not selected
        if slot == "NOT_SELECTED":
            continue

        course = courses[course_id]

        # Preference 1:
        # Preferred specialization
        if (student.preferred_specialization and course.specialization 
            == student.preferred_specialization):
            score += 10

            reasons.append(
                f"{course_id}: matches preferred "
                f"specialization "
                f"({student.preferred_specialization})"
            )

        # Preference 2:
        # Preferred time slot

        if slot in student.preferred_slots:
            score += 5

            reasons.append(
                f"{course_id}: uses preferred "
                f"slot {slot}"
            )

    return {"plan": plan, "score": score, "reasons": reasons}

def rank_plans(plans, courses, student):
    evaluated_plans = []

    for plan in plans:
        result = evaluate_plan(plan, courses, student)
        evaluated_plans.append(result)

    # Highest score first
    evaluated_plans.sort(key = lambda item: item["score"], reverse = True)

    return evaluated_plans