class CSP:
    def __init__(self):
        self.variables = []
        self.domains = {}

    def add_variable(self, variable, domain):
        self.variables.append(variable)
        self.domains[variable] = domain

def build_course_csp(courses,eligibility_results):
    csp = CSP()

    for result in eligibility_results:
        if result["status"] != "eligible":
            continue

        course_id = result["course_id"]
        course = courses[course_id]
        domain = course.offered_slots.copy()

        # Elective course can also be skipped
        if course.course_type == "elective":
            domain.append("NOT_SELECTED")

        csp.add_variable(course_id, domain)

    return csp