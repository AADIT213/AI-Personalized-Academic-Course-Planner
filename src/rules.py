def rule_already_completed(course, student):
    if course.course_id in student.completed_courses:

        return {"rule_id": "R1", "status": "ineligible", "reason": (
                f"{course.course_id} has " f"already been completed.")}
    return None

def rule_wrong_semester(course, student):
    if course.semester != student.semester:
        
        return {"rule_id": "R2", "status": "ineligible", "reason": (
                f"Course belongs to Semester " f"{course.semester}, not Semester " 
                f"{student.semester}.")}
    return None

def rule_missing_prerequisite(course, student):
    missing_prerequisites = []

    for prerequisite in course.prerequisites:
        
        if prerequisite not in (student.completed_courses):
            missing_prerequisites.append(prerequisite)

    if missing_prerequisites:

        return {"rule_id": "R3", "status": "ineligible", "reason": (
            "Missing prerequisite(s): " + ", ".join(missing_prerequisites))}
    return None


def rule_prerequisites_satisfied(course, student):
    return {"rule_id": "R4", "status": "eligible", "reason": (
            "Semester and prerequisite requirements are satisfied.")}

ELIGIBILITY_RULES = [rule_already_completed, rule_wrong_semester,
                     rule_missing_prerequisite, rule_prerequisites_satisfied]