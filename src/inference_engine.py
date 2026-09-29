from src.rules import ELIGIBILITY_RULES

class InferenceEngine:
    def __init__(self, courses):
        self.courses = courses

    def evaluate_course(self, course, student):
        """Apply eligibility rules to one course."""

        for rule in ELIGIBILITY_RULES:
            result = rule(course, student)

            if result is not None:

                return {
                    "course_id": course.course_id,
                    "course_name": course.name,
                    "status": result["status"],
                    "rule_id": result["rule_id"],
                    "reason": result["reason"]
                }

    def evaluate_all_courses(self, student):
        """Apply eligibility reasoning to all courses."""

        results = []

        for course in self.courses.values():
            result = self.evaluate_course(course, student)
            results.append(result)

        return results