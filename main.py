from __future__ import annotations
import pathlib
from Backend.Models.Subject import Subject
from Backend.Models.Student  import Student
from Backend.algo import optimize_schedule, hval

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

students = Student.load_students("Backend/test-cases.txt", catalog)

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

if __name__ == "__main__":
    debug = False

    if debug:
        dump_students(students)
        dump_subject_sessions(catalog)

        sorted_students = Student.sort_by_preference_weight(
            students,
            output_file="Backend/sorted-students.txt",
            debug=True
        )
    
    initial_happiness_regular = hval(students)
    initial_happiness_normalized = hval(students)
    
    print(f"Initial happiness (hval method): {initial_happiness_regular}")
    print(f"Initial happiness (normalized method): {initial_happiness_normalized:.2f}")
    
    max_iterations = 100
    improvement_threshold = 0.001
    
    optimize_schedule(students, max_iterations, improvement_threshold)
    
    final_happiness_regular = hval(students)
    final_happiness_normalized = hval(students)
    
    print(f"Final happiness (hval method): {final_happiness_regular}")
    print(f"Final happiness (normalized method): {final_happiness_normalized:.2f}")
    print(f"Improvement (hval method): {((final_happiness_regular - initial_happiness_regular) / initial_happiness_regular) * 100:.2f}%")
    
    debug_dumps = True
    if debug_dumps:
        dump_students(students)
        dump_subject_sessions(catalog)
        Student.sort_by_preference_weight(
            students,
            output_file="Backend/sorted-students.txt",
            debug=True
        )

