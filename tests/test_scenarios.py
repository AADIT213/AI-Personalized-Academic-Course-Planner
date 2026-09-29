import json
import unittest

from src.knowledge_base import KnowledgeBase
from src.models import StudentProfile
from src.inference_engine import InferenceEngine
from src.csp import build_course_csp
from src.solvers import forward_checking_solver

class TestScenarios(unittest.TestCase):
    def setUp(self):
        kb = KnowledgeBase("data/courses.json")

        self.courses = kb.load_courses()
        with open("data/sample_scenarios.json", "r") as file:
            self.scenarios = json.load(file)

    def test_all_scenarios(self):
        for scenario in self.scenarios:
            with self.subTest(scenario=scenario["scenario_id"]):

                completed = [course.course_id
                    for course in (self.courses.values())
                    if (course.semester < scenario["semester"])]

                for course_id in scenario["remove_completed_courses"]:
                    if course_id in completed:
                        completed.remove(course_id)

                student = StudentProfile(student_id = "24BAM005",
                                         semester = scenario["semester"],
                    completed_courses = completed, max_credits = scenario["max_credits"],
                    preferred_specialization = (scenario["preferred_specialization"]),
                    preferred_slots = scenario["preferred_slots"],
                    blocked_slots = scenario["blocked_slots"])

                engine = InferenceEngine(self.courses)
                eligibility = (engine.evaluate_all_courses(student))
                csp = build_course_csp(self.courses, eligibility)
                solutions, _ = (forward_checking_solver(csp, self.courses, student))

                if scenario["expected_solution"]:
                    self.assertGreater(len(solutions), 0)
                else:
                    self.assertEqual(len(solutions), 0)
                    
                if ("expected_ineligible_course" in scenario):
                    course_id = scenario["expected_ineligible_course"]

                    result = next(item for item in eligibility
                                  if item["course_id"] == course_id)
                    
                    self.assertEqual(result["status"], "ineligible")

if __name__ == "__main__":
    unittest.main()