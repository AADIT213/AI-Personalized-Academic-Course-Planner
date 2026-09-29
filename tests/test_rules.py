import unittest
from src.knowledge_base import KnowledgeBase
from src.models import StudentProfile
from src.inference_engine import InferenceEngine

class TestRules(unittest.TestCase):
    def setUp(self):
        kb = KnowledgeBase("data/courses.json")

        self.courses = kb.load_courses()
        self.completed = [course.course_id for course in self.courses.values() 
                          if course.semester < 5]

    def test_ai_course_is_eligible(self):
        student = StudentProfile(student_id = "24BAM005", semester = 5,
                                 completed_courses = self.completed, max_credits = 24)

        engine = InferenceEngine(self.courses)
        results = engine.evaluate_all_courses(student)
        result = next(item for item in results if item["course_id"] == "AI301")
        self.assertEqual(result["status"], "eligible")

    def test_missing_ml_rejects_deep_learning(self):
        completed = self.completed.copy()
        completed.remove("ML202")
        student = StudentProfile(student_id = "24BAM005", semester = 5,
                                 completed_courses = completed, max_credits = 24)
        engine = InferenceEngine(self.courses)
        results = engine.evaluate_all_courses(student)
        result = next(item for item in results if item["course_id"] == "DL301")

        self.assertEqual(result["status"], "ineligible")
        self.assertIn("ML202", result["reason"])

if __name__ == "__main__":
    unittest.main()