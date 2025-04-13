import numpy as np

from Backend.Models.Student import Student

class Subject:
    """
    Represents a single course section.
    session  : numpy array of start‑times (ints, e.g. [9])
    gpa      : numpy array of GPAs for those sessions (floats)
    """
    def __init__(self, name: str, session, gpa):
        self.name    = name
        self.session = np.array(session, dtype=int)
        self.gpa     = np.array(gpa,     dtype=float)

    def __repr__(self):
        return f"{self.name}@{self.session.tolist()} | GPA {self.gpa.tolist()}"
