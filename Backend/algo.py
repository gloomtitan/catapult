from Backend.Models.Student import Student
from Backend.Models.Subject import Subject
import random

LATE = 10
LUNCH_HOURS = [12, 13]

def conflicts_schedule(sess: Subject.Session, sessions: list[Subject.Session]) -> bool:
    for session in sessions:
        if session != sess and sess.start_time == session.start_time and sess.mwf == session.mwf:
            return True
    return False

def has_lunch_break(sessions: list[Subject.Session]) -> bool:
    class_times = [s.start_time for s in sessions]
    return not all(hour in class_times for hour in LUNCH_HOURS)

def handle_time(student: Student, students_list: list[Student]) -> bool:
    changes_made = False
    
    if student.preferences["late"] == 0:
        return False
    
    for stud_sess in student.sessions:
        if stud_sess.start_time >= LATE:
            continue
            
        subject = stud_sess.parent
        
        later_sessions = [s for s in subject.sessions if s.start_time > stud_sess.start_time]
        later_sessions.sort(key=lambda s: s.start_time, reverse=True)
        
        for sess in later_sessions:
            if conflicts_schedule(sess, student.sessions):
                continue
                
            if sess.current_enrollment() < sess.capacity:
                if swap_sessions(student, stud_sess, sess, students_list):
                    changes_made = True
                    break
            else:
                for other in sess.students:
                    if other.preferences["late"] < student.preferences["late"]:
                        if not conflicts_schedule(stud_sess, other.sessions):
                            if swap_students(student, stud_sess, other, sess, students_list):
                                changes_made = True
                                break
                
                if changes_made:
                    break
    
    return changes_made

def handle_gpa(student: Student, students_list: list[Student]) -> bool:
    changes_made = False
    
    if student.preferences["gpa"] == 0:
        return False
    
    for stud_sess in student.sessions:
        subject = stud_sess.parent
        
        better_sessions = [s for s in subject.sessions if s.prof_gpa > stud_sess.prof_gpa]
        better_sessions.sort(key=lambda s: s.prof_gpa, reverse=True)
        
        for sess in better_sessions:
            if conflicts_schedule(sess, student.sessions):
                continue
                
            if sess.current_enrollment() < sess.capacity:
                if swap_sessions(student, stud_sess, sess, students_list):
                    changes_made = True
                    break
            else:
                for other in sess.students:
                    if other.preferences["gpa"] < student.preferences["gpa"]:
                        if not conflicts_schedule(stud_sess, other.sessions):
                            if swap_students(student, stud_sess, other, sess, students_list):
                                changes_made = True
                                break
                
                if changes_made:
                    break
    
    return changes_made

def handle_lunch(student: Student, students_list: list[Student]) -> bool:
    changes_made = False
    
    # Only consider students with a preference for lunch break
    if student.preferences["lunch"] == 0:
        return False
        
    # Check if student already has a lunch break
    if has_lunch_break(student.sessions):
        return False  # Already satisfied
    
    # Find all sessions during lunch hours
    lunch_sessions = [s for s in student.sessions if s.start_time in LUNCH_HOURS]
    
    for lunch_sess in lunch_sessions:
        subject = lunch_sess.parent
        
        # Find non-lunch hour sessions for this subject
        alt_sessions = [s for s in subject.sessions if s.start_time not in LUNCH_HOURS]
        
        for sess in alt_sessions:
            if conflicts_schedule(sess, student.sessions):
                continue  # Skip if conflicts with other classes
            
            # Try to swap to the non-lunch session
            if sess.current_enrollment() < sess.capacity:
                # Simple move
                if swap_sessions(student, lunch_sess, sess, students_list):
                    changes_made = True
                    break
            else:
                # Try to find someone to swap with
                for other in sess.students:
                    # Only consider swapping if other student cares less about lunch
                    if other.preferences["lunch"] < student.preferences["lunch"]:
                        # Check if the other student can move to student's current session
                        if not conflicts_schedule(lunch_sess, other.sessions):
                            # Perform the swap
                            if swap_students(student, lunch_sess, other, sess, students_list):
                                changes_made = True
                                break
                
                if changes_made:
                    break
                    
        if changes_made:
            # Check if we've achieved a lunch break
            if has_lunch_break(student.sessions):
                break  # Success!
    
    return changes_made

def swap_sessions(student: Student, from_sess: Subject.Session, to_sess: Subject.Session, students_list: list[Student]) -> bool:
    initial_happiness = hval(students_list)
    
    student.remove_session(from_sess)
    student.add_session(to_sess)
    
    new_happiness = hval(students_list)
    
    if new_happiness > initial_happiness:
        return True
    else:
        student.remove_session(to_sess)
        student.add_session(from_sess)
        return False

def swap_students(student1: Student, sess1: Subject.Session, student2: Student, sess2: Subject.Session, students_list: list[Student]) -> bool:
    initial_happiness = hval(students_list)
    
    student1.remove_session(sess1)
    student2.remove_session(sess2)
    
    student1.add_session(sess2)
    student2.add_session(sess1)
    
    new_happiness = hval(students_list)
    
    if new_happiness > initial_happiness:
        return True
    else:
        student1.remove_session(sess2)
        student2.remove_session(sess1)
        student1.add_session(sess1)
        student2.add_session(sess2)
        return False

def optimize_schedule(students: list[Student], max_iterations=100, improvement_threshold=0.0001):
    initial_score = hval(students)
    current_score = initial_score
    print(f"Initial happiness score: {initial_score}")
    
    # Keep track of scores
    score_history = [current_score]
    plateau_count = 0
    
    # Sort students by total preference weight (most opinionated first)
    sorted_students = sorted(
        students,
        key=lambda s: s.preference_weight(),
        reverse=True
    )
    
    for iteration in range(1, max_iterations + 1):
        total_changes = 0
        
        # Apply all three handlers in sequence for each student
        for student in sorted_students:
            if handle_time(student, students):
                total_changes += 1
                
            if handle_gpa(student, students):
                total_changes += 1
                
            if handle_lunch(student, students):
                total_changes += 1
        
        # Calculate new happiness score
        new_score = hval(students)
        improvement = (new_score - current_score) / current_score if current_score > 0 else 0
        
        print(f"Iteration {iteration}: happiness = {new_score} (change: {improvement:.4f}, changes: {total_changes})")
        
        if abs(improvement) < improvement_threshold:
            plateau_count += 1
        else:
            plateau_count = 0
            
        if plateau_count >= 5:
            print(f"Optimization plateaued after {iteration} iterations")
            break
            
        # Stop if no changes were made
        if total_changes == 0:
            print("No further improvements possible")
            break
            
        current_score = new_score
        score_history.append(current_score)
        
        if iteration % 5 == 0:
            random.shuffle(sorted_students)
    
    final_score = hval(students)
    print(f"Optimization complete. Final happiness: {final_score}")
    
    if final_score > initial_score:
        improvement_pct = ((final_score - initial_score) / initial_score) * 100
        print(f"Total improvement: {improvement_pct:.2f}%")
    else:
        print("No overall improvement achieved.")
    
    return final_score, students

def hval(students: list[Student]) -> int:
    """
    Original happiness function from the algorithm.
    Happiness = Σ over students Σ over sessions
                pref_value * rank
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

        if p["lunch"]:
            class_times = [s.start_time for s in stu.sessions]
            has_gap = not all(hour in class_times for hour in LUNCH_HOURS)
            if has_gap:
                total += p["lunch"]
                
    return total 
