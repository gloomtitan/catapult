from Backend.Models.Student import Student
from Backend.Models.Subject import Subject
from sort_students import sort_preference_weight
import numpy as np

LATE = 10

# called if the student wants to switch to a later start time
def handle_time(student: Student):
    for stud_sess in student.sessions:
        stud_sess: Subject.Session
        if stud_sess.start_time >= LATE:
            continue

        subject = stud_sess.parent

        for sess in subject.sessions:
            sess: Subject.Session
            if sess.start_time < LATE:
                continue

            if sess.current_enrollment() < sess.capacity:
                sess.add_student(student)
                student.remove_session(sess)
                break

            reversed_list = reversed(Student.sort_by_preference_weight(sess.students))
            flag_break = False
            for other in reversed_list:
                other: Student
                other_late: int = other.preferences["late"]
                stud_late: int = student.preferences["late"]
                if (other_late < stud_late or (other_late == stud_late and int(other.id[1:]) < int(student.id[1:]))):
                    sess.add_student(student)
                    sess.remove_student(other)
                    student.add_session(sess)
                    other.remove_session(sess)
                    flag_break = True
                    break
            if flag_break:
                break
    pass

# called if the student wants to switch to a better avg gpa section
def handle_gpa(student: Student):
    for stud_sess in student.sessions:
        stud_sess: Subject.Session
        subject: Subject = stud_sess.parent
        
    pass

def algo_main(students: np.ndarray):
    for student in students:
        student: Student

if __name__ == "__main__":
    students: np.ndarray = sort_preference_weight()
    algo_main(students)

