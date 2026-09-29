def is_valid_assignment(course_id, slot, assignment, courses, student):
    course = courses[course_id]

    # Elective not selected
    if slot == "NOT_SELECTED":
        return True

    # Rule 1:
    # Student cannot use a blocked slot
    if slot in student.blocked_slots:
        return False

    # Rule 2:
    # Two selected courses cannot use the same slot
    for other_course, other_slot in assignment.items():
        if other_slot == "NOT_SELECTED":
            continue
        
        if slot == other_slot:
            return False

    # Rule 3:
    # Credit limit must not be exceeded
    total_credits = course.credits

    for assigned_course, assigned_slot in assignment.items():
        
        if assigned_slot != "NOT_SELECTED":
            total_credits += (courses[assigned_course].credits)

    if total_credits > student.max_credits:
        return False

    return True