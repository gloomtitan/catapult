from __future__ import annotations
from typing import List, Tuple, TYPE_CHECKING

# if TYPE_CHECKING:                       # avoids runtime circular import
  #  from Backend.Models.Student import Student


class Subject:
    class Session:
        def __init__(self,
                     parent: "Subject",
                     start_time: int,
                     prof_gpa: float,
                     capacity: int):
            self.parent     = parent
            self.start_time = start_time
            self.prof_gpa   = prof_gpa
            self.capacity   = capacity
            self.students: List["Student"] = []   # now Student objects

        # ---------- enrol helpers ----------
        def add_student(self, student: "Student") -> bool:
            if len(self.students) < self.capacity:
                self.students.append(student)
                return True
            return False

        def remove_student(self, student: "Student"):
            if student in self.students:
                self.students.remove(student)

        def __repr__(self):
            return (f"{self.parent.name}-{self.start_time} | "
                    f"cap={self.capacity} | profGPA={self.prof_gpa} | "
                    f"enrolled={len(self.students)}")

    # ---------- Subject ----------
    def __init__(self, name: str,
                 section_data: List[Tuple[int, float, int]]):
        self.name = name
        self.sessions = [
            Subject.Session(self, t, gpa, cap) for t, gpa, cap in section_data
        ]

    def get_session(self, start_time: int) -> "Subject.Session | None":
        for s in self.sessions:
            if s.start_time == start_time:
                return s
        return None

    def __repr__(self):
        return f"{self.name}: {self.sessions}"
