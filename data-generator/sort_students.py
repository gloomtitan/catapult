"""
Reads test-cases.txt, sorts students by descending preference weight,
and writes the result to data-generator/sorted-students.txt
"""
from Backend.Models.Student import Student

def sort_preference_weight(
    input_file: str = "test-cases.txt",
    output_file: str = "sorted-students.txt"
):
    students = Student.load_students(input_file)

    # sort by descending weight
    sorted_students = sorted(
        students,
        key=lambda s: s.preference_weight(),
        reverse=True
    )

    with open(output_file, "w") as f:
        for stu in sorted_students:
            f.write(f"{stu.id} {stu.preference_weight():.2f}\n")

    print(f"Wrote {len(sorted_students)} students → {output_file}")
    return sorted_students


if __name__ == "__main__":
    sort_preference_weight()
