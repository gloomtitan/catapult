from __future__ import annotations
from typing import List
from Backend.Models.Subject import Subject


class Student:
    COURSE_ORDER = ["scla", "econ", "eng", "cs",
                    "ma", "chem", "pol", "hist"]

    def __init__(self,
                 student_id: str,
                 preferences: dict,
                 sessions: List[Subject.Session]):
        self.id          = student_id
        self.preferences = preferences
        self.sessions    = sessions

        # register this Student object with every Session
        for sess in self.sessions:
            sess.add_student(self)

    # ------------- preference weight -------------
    def preference_weight(self) -> float:
        p = self.preferences
        return p["late"]**2 + p["lunch"]**2 + p["gpa"]**2

    # ------------- factory from one line -------------
    @staticmethod
    def from_line(line: str, catalog: dict[str, Subject]):
        data_part, late, lunch, gpa = line.strip().split('|')
        parts = data_part.split('-')

        student_id  = parts[0]
        class_times = list(map(int, parts[1:]))

        sessions = []
        for course, time in zip(Student.COURSE_ORDER, class_times):
            if time == 0:
                continue
            subj = catalog[course]
            sess = subj.get_session(time)
            if sess is None:
                raise ValueError(f"{course} has no session at {time}")
            sessions.append(sess)

        prefs = {"late": int(late), "lunch": int(lunch), "gpa": int(gpa)}
        return Student(student_id, prefs, sessions)

    @staticmethod
    def load_students(path: str, catalog: dict[str, Subject]):
        students = []
        with open(path) as f:
            lines = f.readlines()
            n = int(lines[0].strip())
            for line in lines[1:n+1]:
                students.append(Student.from_line(line, catalog))
        return students

    def add_session(self, sess: Subject.Session) -> bool:
        """
        Enrol this student in the given Session.
        Returns True if successful, False if the session is full
        or already present.
        """
        if sess in self.sessions:
            return False  # already enrolled
        if sess.add_student(self):  # uses Session helper
            self.sessions.append(sess)
            return True
        return False  # session full

    def remove_session(self, sess: Subject.Session) -> bool:
        """
        Drop this student from the given Session.
        Returns True on success, False if the session was not found.
        """
        if sess not in self.sessions:
            return False
        self.sessions.remove(sess)
        sess.remove_student(self)  # uses Session helper
        return True

    @staticmethod
    def sort_by_preference_weight(students,
                                  output_file: str = "Backend/sorted-students.txt",
                                  debug: bool = False):
        """
        Sort a list / NumPy array of Student objects in descending order
        of preference_weight.  Optionally writes the ranking to a file.
        """
        import numpy as np

        sorted_stu = sorted(
            students,
            key=lambda s: s.preference_weight(),
            reverse=True
        )

        if debug:
            with open(output_file, "w") as f:
                for stu in sorted_stu:
                    f.write(f"{stu.id}  total={stu.preference_weight():.2f}\n")
            print(f"Wrote {len(sorted_stu)} students → {output_file}")

        return np.array(sorted_stu, dtype=object)


    def __repr__(self):
        codes = [f"{s.parent.name}-{s.start_time}" for s in self.sessions]
        return f"{self.id}: {codes} | prefW={self.preference_weight():.1f}"
