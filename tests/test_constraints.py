import unittest

from src.knowledge_base import KnowledgeBase
from src.models import StudentProfile
from src.constraints import is_valid_assignment

class TestConstraints(unittest.TestCase):
    def setUp(self):
        kb = KnowledgeBase("data/courses.json")
        
        self.courses = kb.load_courses()
        self.completed = [course.course_id for course in self.courses.values()
                          if course.semester < 5] 

    def test_blocked_slot(self):
        student = StudentProfile(student_id = "24BAM005", semester = 5, 
                                 completed_courses = self.completed, max_credits = 24, 
                                 blocked_slots = ["MON-09"])
        valid = is_valid_assignment("AI301", "MON-09", {}, self.courses, student)
        self.assertFalse(valid)
        
    def test_time_conflict(self):
        student = StudentProfile(student_id = "24BAM005", semester = 5, 
                                 completed_courses = self.completed, max_credits = 24)
        assignment = {"AI301": "MON-09"}
        valid = is_valid_assignment("DL301", "MON-09", assignment, self.courses, student)
        self.assertFalse(valid)

    def test_credit_limit(self):
        student = StudentProfile(student_id = "24BAM005", semester = 5, 
                                 completed_courses = self.completed, max_credits = 4)
        assignment = {"AI301": "WED-11"}
        valid = is_valid_assignment("CMAI301", "TUE-10", assignment, self.courses, student)
        self.assertFalse(valid)

if __name__ == "__main__":
    unittest.main()