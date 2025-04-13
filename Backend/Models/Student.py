import numpy as np
from .Subject import Subject      # relative import inside Backend.Models


class Student:
    """
    id            : string  (e.g. '#1')
    preferences   : dict    {'late': int, 'lunch': int, 'gpa': float}
    subject_list  : list[Subject]
    """
    SUBJECT_NAMES = ["scla", "econ", "eng", "cs", "ma", "chem", "pol", "hist"]

    def __init__(self, student_id, preferences, subject_list):
        self.id            = student_id
        self.preferences   = preferences
        self.subject_list  = subject_list

    # ---------- preference weight ----------
    def preference_weight(self) -> float:
        p = self.preferences
        return p["late"]**2 + p["lunch"]**2 + p["gpa"]**2

    # ---------- factory from one line ----------
    @staticmethod
    def from_line(line: str):
        """
        Format:
        #id-scla-econ-eng-cs-ma-chem-pol-hist|late|lunch|gpa
        """
        line = line.strip()
        if not line:
            return None

        data_part, late, lunch, gpa = line.split('|')
        parts = data_part.split('-')

        student_id   = parts[0]
        class_times  = list(map(int, parts[1:]))

        subject_list = [
            Subject(name, [time], [0.0])          # default GPA per session
            for name, time in zip(Student.SUBJECT_NAMES, class_times)
        ]

        preferences = {
            "late" : int(late),
            "lunch": int(lunch),
            "gpa"  : float(gpa)
        }

        return Student(student_id, preferences, subject_list)

    # ---------- bulk loader ----------
    @staticmethod
    def load_students(file_path: str = "data-generator/test-cases.txt"):
        """
        Reads the first line as the count, then that many student lines.
        Returns a NumPy object array of Student instances.
        """
        students = []
        with open(file_path, "r") as f:
            lines = f.readlines()
            count = int(lines[0].strip())

            for line in lines[1:count + 1]:
                stu = Student.from_line(line)
                if stu:
                    students.append(stu)

        return np.array(students, dtype=object)

    # ---------- nice print ----------
    def __repr__(self):
        return f"{self.id} | Pref‑wgt={self.preference_weight():.2f}"
