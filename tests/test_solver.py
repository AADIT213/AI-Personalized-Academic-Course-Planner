import unittest

from src.knowledge_base import KnowledgeBase
from src.models import StudentProfile
from src.inference_engine import InferenceEngine
from src.csp import build_course_csp

from src.solvers import (backtracking_solver, mrv_backtracking_solver, forward_checking_solver)

class TestSolvers(unittest.TestCase):
    def setUp(self):
        kb = KnowledgeBase("data/courses.json")
        self.courses = kb.load_courses()
        
        completed = [course.course_id for course in self.courses.values() if course.semester < 5]

        self.student = StudentProfile(student_id = "24BAM005", semester = 5,
                                      completed_courses = completed, max_credits = 24,
                                      preferred_specialization = "AI", preferred_slots = [
                                          "MON-09", "THU-14"])
        engine = InferenceEngine(self.courses)
        eligibility = (engine.evaluate_all_courses( self.student))
        self.csp = build_course_csp(self.courses, eligibility)

    def test_all_solvers_find_solutions(self):
        basic, _ = backtracking_solver(self.csp, self.courses, self.student)
        mrv, _ = mrv_backtracking_solver(self.csp, self.courses, self.student)
        forward, _ = forward_checking_solver(self.csp, self.courses, self.student)
        
        self.assertGreater(len(basic), 0)
        self.assertEqual(len(basic), len(mrv))
        self.assertEqual(len(mrv), len(forward))

    def test_forward_checking_metrics(self):
        _, metrics = (forward_checking_solver(self.csp, self.courses, self.student))
        self.assertIn("pruning_events", metrics)

if __name__ == "__main__":
    unittest.main()