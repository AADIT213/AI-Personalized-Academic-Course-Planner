import json
from src.models import Course
from src.models import StudentProfile

class KnowledgeBase:
    def __init__(self, course_file, student_file = None):
        self.course_file = course_file
        self.student_file = student_file

        self.courses = {}
        self.students = {}

    def load_courses(self):
        with open(self.course_file, "r") as file:
            course_data = json.load(file)

        for data in course_data:

            course = Course(
                course_id = data["course_id"],
                name = data["name"],
                semester = data["semester"],
                credits = data["credits"],
                category = data["category"],
                prerequisites = data.get("prerequisites", []),
                offered_slots = data.get("offered_slots", []),
                course_type = data.get("course_type", "elective"),
                specialization=data.get("specialization", "")
            )

            self.courses[course.course_id] = course

        return self.courses

    def load_students(self):
        if self.student_file is None:
            raise ValueError("Student file was not provided.")

        with open(self.student_file, "r") as file:
            student_data = json.load(file)

        for data in student_data:

            student = StudentProfile(
                student_id = data["student_id"],
                semester = data["semester"],
                completed_courses = data["completed_courses"],
                max_credits = data["max_credits"],
                preferred_specialization = data.get("preferred_specialization", ""),
                preferred_slots=data.get("preferred_slots", []),
                blocked_slots=data.get("blocked_slots", [])
            )

            self.students[student.student_id] = student

        return self.students