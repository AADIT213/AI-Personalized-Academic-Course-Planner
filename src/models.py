from dataclasses import dataclass, field
from typing import List

@dataclass
class Course:
    course_id: str
    name: str
    semester: int
    credits: int
    category: str
    prerequisites: List[str] = field(default_factory=list)
    offered_slots: List[str] = field(default_factory=list)
    course_type: str = "elective"
    specialization: str = ""

@dataclass
class StudentProfile:
    student_id: str
    semester: int
    completed_courses: List[str]
    max_credits: int

    preferred_specialization: str = ""
    preferred_slots: List[str] = field(default_factory=list)
    blocked_slots: List[str] = field(default_factory=list)