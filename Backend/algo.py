from Backend.Models.Student import Student
from sort_students import sort_preference_weight
import numpy as np

def handle_late():
    pass

def handle_break():
    pass

def handle_gpa():
    pass

def algo_main(students: np.ndarray):
    for student in students:
        student: Student

if __name__ == "__main__":
    students: np.ndarray = sort_preference_weight()
    algo_main(students)

