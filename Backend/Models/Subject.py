import numpy as np


class Subject:
    """
    A course that can have one or more sessions (sections).
    Each session has its own capacity, enrolled‑student list,
    and a hard‑coded average‑GPA value (set by the professor / section).
    """

    class Session:
        """
        One section of a course.

        Attributes
        ----------
        start_time : int            # time (24 hour format)
        max_size   : int            # capacity
        prof_gpa   : float          # historical avg GPA for this section
        students   : list[str]      # ids of enrolled students
        """
        def __init__(self, start_time: int, max_size: int, prof_gpa: float):
            self.start_time = start_time
            self.max_size   = max_size
            self.prof_gpa   = prof_gpa
            self.students   = []          # empty at creation

        def add_student(self, student_id: str) -> bool:
            """Returns True if added, False if section is full."""
            if len(self.students) < self.max_size:
                self.students.append(student_id)
                return True
            return False

        def seats_left(self) -> int:
            return self.max_size - len(self.students)

        def __repr__(self):
            return (f"{self.start_time} | cap={self.max_size} | "
                    f"profGPA={self.prof_gpa} | enrolled={len(self.students)}")

    # ------------- Subject -------------
    def __init__(self, name: str, section_data):
        """
        Parameters
        ----------
        name         : str
            Course code, e.g. 'cs'
        section_data : iterable[tuple]
            Each tuple = (start_time:int, prof_gpa:float, capacity:int)
            Example: [(930, 3.2, 40), (1430, 3.6, 35)]
        """
        self.name = name
        self.sessions = [Subject.Session(*tup) for tup in section_data]

    def __repr__(self):
        return f"{self.name}: {self.sessions}"