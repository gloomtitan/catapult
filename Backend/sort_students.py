"""
Reads test-cases.txt, sorts students by descending preference weight,
and (optionally) writes the result to Backend/sorted-students.txt
"""

import sys, pathlib
import numpy as np

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))   # add project root

from Backend.Models.Student import Student


def sort_preference_weight(
    input_file: str = "Backend/test-cases.txt",
    output_file: str = "Backend/sorted-students.txt",
    debug: bool = False
):
    students = Student.load_students(input_file)

    sorted_students = sorted(
        students, key=lambda s: s.preference_weight(), reverse=True
    )

    if debug:
        with open(output_file, "w") as f:
            for stu in sorted_students:
                p = stu.preferences
                f.write(f"{stu.id}  total={stu.preference_weight():.2f}\n")
                # f.write(f"    late={p['late']}  lunch={p['lunch']}  gpa={p['gpa']}\n")

        print(f"Wrote {len(sorted_students)} students → {output_file}")

    return np.array(sorted_students)


if __name__ == "__main__":
    sort_preference_weight(debug=True)   # set True if you want the file output
