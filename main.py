"""
main.py  – single entry‑point for timetable‑optimizer demo
----------------------------------------------------------
• Builds the course‑catalog once.
• Loads students from Backend/test-cases.txt.
• When debug=True it writes a human‑readable dump to
  Backend/student-database.txt
"""

from __future__ import annotations
import pathlib
import sys
from Backend.Models.Subject import Subject
from Backend.Models.Student  import Student

# ------------------------------------------------------------------ #
# 1.  Build course catalog  (immutable after creation)
#     Each tuple = (start_time, professor_GPA, capacity)
# ------------------------------------------------------------------ #
catalog = {
    "scla": Subject("scla", [(7,  4.0, 50),
                             (9,  3.7, 50),
                             (10, 2.5, 50),
                             (12, 3.2, 50)]),

    "econ": Subject("econ", [(10, 3.9, 25),
                             (13, 3.2, 100),
                             (14, 2.9, 50),
                             (16, 4.0, 50)]),

    "eng":  Subject("eng",  [(7,  3.6, 50),
                             (8,  3.3, 50),
                             (12, 2.1, 100),
                             (14, 3.9, 25)]),

    "cs":   Subject("cs",   [(9,  3.0, 50),
                             (10, 3.8, 25),
                             (11, 2.4, 100),
                             (15, 3.1, 50)]),

    "ma":   Subject("ma",   [(7,  3.9, 50),
                             (8,  3.4, 100),
                             (10, 3.7, 50),
                             (13, 2.8, 50)]),

    "chem": Subject("chem", [(9,  4.0, 25),
                             (11, 3.8, 50),
                             (12, 3.3, 100),
                             (16, 3.0, 50)]),

    "pol":  Subject("pol",  [(8,  3.9, 25),
                             (9,  3.5, 100),
                             (10, 4.0, 50),
                             (13, 3.3, 50)]),

    "hist": Subject("hist", [(10, 3.5, 25),
                             (13, 3.9, 50),
                             (14, 2.8, 100),
                             (16, 3.0, 50)]),
}

# 2.  Load students
students = Student.load_students("Backend/test-cases.txt", catalog)

# 3.  Optional pretty‑print dump
def dump_students(stu_list, out_path="Backend/student-database.txt") -> None:
    p = pathlib.Path(out_path)
    with p.open("w") as f:
        for stu in stu_list:
            prefs = stu.preferences
            f.write(f"Student {stu.id}\n")
            f.write(
                f"  Preferences: "
                f"late={prefs['late']}  lunch={prefs['lunch']}  gpa={prefs['gpa']}\n"
            )
            f.write("  Sessions:\n")
            for sess in stu.sessions:
                f.write(
                    f"    {sess.parent.name.upper()} @ {sess.start_time:02d}:00  "
                    f"(prof‑GPA {sess.prof_gpa}, cap {sess.capacity}, "
                    f"enrolled {(sess.current_enrollment())})\n"
                )
            f.write("\n")
    print(f"Wrote {len(stu_list)} students → {p}")

# 3)b Dump the list of sessions of each subject along with details and student list. Students are identified by their ID number
def dump_subject_sessions(cat: dict[str, Subject],
                          out_path="Backend/subject_session_details.txt") -> None:
    p = pathlib.Path(out_path)
    with p.open("w") as f:
        for subj in cat.values():
            f.write(f"{subj.name.upper()}\n")
            for sess in subj.sessions:
                ids = [stu.id for stu in sess.students] or ["<empty>"]
                f.write(
                    f"  start={sess.start_time:02d}:00  "
                    f"cap={sess.capacity}  profGPA={sess.prof_gpa}\n"
                    f"    students: {', '.join(ids)}\n"
                )
            f.write("\n")
    print(f"Wrote session details → {p}")

# 4.  Main block
if __name__ == "__main__":
    debug = True          # ← toggle to False to skip file dump

    if debug:
        dump_students(students)  # already present
        dump_subject_sessions(catalog)  # ← add this li

    # Example: call sort_preference_weight if desired
    # from Backend.sort_students import sort_preference_weight
    # sort_preference_weight(debug=True)

