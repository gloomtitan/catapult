from Backend.Models.Student import Student
from Backend.Models.Subject import Subject
import numpy as np

LATE = 10

def conflicts_schedule(sess: Subject.Session, sessions: list[Subject.Session]) -> bool:
    exit_code = False
    for session in sessions:
        if sess.start_time == session.start_time and sess.mwf == session.mwf:
            exit_code = True
            break
    return exit_code

# called if the student wants to switch to a later start time
def handle_time(student: Student):
    for stud_sess in student.sessions:
        stud_sess: Subject.Session
        if stud_sess.start_time >= LATE:
            continue
        if stud_sess.start_time == 0:
            continue
        subject = stud_sess.parent

        ranked_late = sorted(
            subject.sessions,
            key=lambda s: s.start_time,
            reverse=True
        )
        for sess in ranked_late:
            sess: Subject.Session
            if sess.start_time < LATE or conflicts_schedule(sess, student.sessions):
                continue

            if sess.current_enrollment() < sess.capacity:
                student.remove_session(sess)
                sess.add_student(student)
                break

            reversed_list = reversed(list(Student.sort_by_preference_weight(sess.students)))
            flag_break = False
            for other in reversed_list:
                other: Student
                other_late: int = other.preferences["late"]
                stud_late: int = student.preferences["late"]
                if (other_late < stud_late or (other_late == stud_late and int(other.id[1:]) > int(student.id[1:]))):
                    sess.remove_student(other)
                    other.remove_session(sess)
                    sess.add_student(student)
                    student.add_session(sess)
                    # to original session
                    stud_sess.remove_student(student)
                    student.remove_session(stud_sess)
                    stud_sess.add_student(other)
                    other.add_session(stud_sess)
                    flag_break = True
                    break
            if flag_break:
                break
    pass

# called if the student wants to switch to a better avg gpa section
def handle_gpa(student: Student):
    for stud_sess in student.sessions:
        stud_sess: Subject.Session

        if stud_sess.start_time == 0:
            continue

        subject: Subject = stud_sess.parent
        ranked_late = sorted(
            subject.sessions,
            key=lambda s: s.prof_gpa,
            reverse=True
        )
        for sess in ranked_late:
            sess: Subject.Session

            if sess.prof_gpa <= stud_sess.prof_gpa or conflicts_schedule(sess, student.sessions):
                continue
            
            if sess.current_enrollment() < sess.capacity:
                student.remove_session(sess)
                sess.add_student(student)
                break

            reversed_list = reversed(list(Student.sort_by_preference_weight(sess.students)))
            flag_break = False
            for other in reversed_list:
                other: Student
                other_gpa: int = other.preferences["gpa"]
                stud_gpa: int = student.preferences["gpa"]
                if (other_gpa < stud_gpa or (other_gpa == stud_gpa and int(other.id[1:]) > int(student.id[1:]))):
                    sess.remove_student(other)
                    other.remove_session(sess)
                    sess.add_student(student)
                    student.add_session(sess)
                    # to original session
                    stud_sess.remove_student(student)
                    student.remove_session(stud_sess)
                    stud_sess.add_student(other)
                    other.add_session(stud_sess)
                    flag_break = True
                    break
            if flag_break:
                break
    pass


def hval(students: list[Student]) -> int:
    """
    Happiness = Σ over students Σ over sessions
                pref_value * rank
    rank is the 1‑based position (ascending) of that session
    within its course when sorted by the criterion that matches
    the preference (time for 'late', prof_gpa for 'gpa').
    """
    total = 0
    for stu in students:
        p = stu.preferences
        for sess in stu.sessions:
            subj = sess.parent

            if p["late"]:
                ordered = sorted(subj.sessions, key=lambda s: s.start_time)
                rank = ordered.index(sess) + 1
                total += p["late"] * rank

            if p["gpa"]:
                ordered = sorted(subj.sessions, key=lambda s: s.prof_gpa)
                rank = ordered.index(sess) + 1
                total += p["gpa"] * rank

        # lunch‑gap happiness (1 if gap, else 0)
        if p["lunch"]:
            has_gap = any(s.start_time not in (12, 13) for s in stu.sessions)
            if has_gap:
                total += 0.1 * p["lunch"]
        return total
