from Backend.Models.Student import Student
from Backend.Models.Subject import Subject
import numpy as np
import random

LATE = 10  # Classes at or after 10 are considered "late"
LUNCH_HOURS = [12, 13]  # Lunch hours for lunch break preference

def conflicts_schedule(sess: Subject.Session, sessions: list[Subject.Session]) -> bool:
    """Check if a session conflicts with any existing sessions."""
    for session in sessions:
        if session != sess and sess.start_time == session.start_time and sess.mwf == session.mwf:
            return True
    return False

def has_lunch_break(sessions: list[Subject.Session]) -> bool:
    """Check if a student has a lunch break (no class at 12 or 1)."""
    class_times = [s.start_time for s in sessions]
    return not all(hour in class_times for hour in LUNCH_HOURS)

def total_happiness_score(students: list[Student]) -> float:
    """Calculate the total happiness score using the original hval method."""
    return hval(students)

def handle_time_improved(student: Student, students_list: list[Student]) -> bool:
    """
    Improved version of the handle_time function.
    Attempts to move a student to a later class if they prefer it.
    Returns True if any change was made, False otherwise.
    """
    changes_made = False
    
    # Only consider students with a preference for late classes
    if student.preferences["late"] == 0:
        return False
    
    for stud_sess in student.sessions:
        if stud_sess.start_time >= LATE:
            continue  # Already in a late class
            
        subject = stud_sess.parent
        
        # Get later sessions for this subject, sorted by start time (latest first)
        later_sessions = [s for s in subject.sessions if s.start_time > stud_sess.start_time]
        later_sessions.sort(key=lambda s: s.start_time, reverse=True)
        
        for sess in later_sessions:
            if conflicts_schedule(sess, student.sessions):
                continue  # Skip if conflicts with other classes
                
            initial_happiness = hval(students_list)
            
            # Try to swap to the later session
            if sess.current_enrollment() < sess.capacity:
                # Simple move
                if simple_swap(student, stud_sess, sess, students_list):
                    changes_made = True
                    break
            else:
                # Try to find someone to swap with
                for other in sess.students:
                    # Only consider swapping if other student cares less about late classes
                    if other.preferences["late"] < student.preferences["late"]:
                        # Check if the other student can move to student's current session
                        if not conflicts_schedule(stud_sess, other.sessions):
                            # Temporarily perform the swap
                            if swap_students(student, stud_sess, other, sess, students_list):
                                changes_made = True
                                break
                
                if changes_made:
                    break
    
    return changes_made

def handle_gpa_improved(student: Student, students_list: list[Student]) -> bool:
    """
    Improved version of the handle_gpa function.
    Attempts to move a student to a higher GPA class if they prefer it.
    Returns True if any change was made, False otherwise.
    """
    changes_made = False
    
    # Only consider students with a preference for high GPA
    if student.preferences["gpa"] == 0:
        return False
    
    for stud_sess in student.sessions:
        subject = stud_sess.parent
        
        # Get higher GPA sessions for this subject
        better_sessions = [s for s in subject.sessions if s.prof_gpa > stud_sess.prof_gpa]
        better_sessions.sort(key=lambda s: s.prof_gpa, reverse=True)
        
        for sess in better_sessions:
            if conflicts_schedule(sess, student.sessions):
                continue  # Skip if conflicts with other classes
                
            # Try to swap to the better GPA session
            if sess.current_enrollment() < sess.capacity:
                # Simple move
                if simple_swap(student, stud_sess, sess, students_list):
                    changes_made = True
                    break
            else:
                # Try to find someone to swap with
                for other in sess.students:
                    # Only consider swapping if other student cares less about GPA
                    if other.preferences["gpa"] < student.preferences["gpa"]:
                        # Check if the other student can move to student's current session
                        if not conflicts_schedule(stud_sess, other.sessions):
                            # Perform the swap
                            if swap_students(student, stud_sess, other, sess, students_list):
                                changes_made = True
                                break
                
                if changes_made:
                    break
    
    return changes_made

def handle_lunch_improved(student: Student, students_list: list[Student]) -> bool:
    """
    Improved function to handle lunch preferences.
    Attempts to give students who want a lunch break the opportunity to have one.
    Returns True if any change was made, False otherwise.
    """
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
                if simple_swap(student, lunch_sess, sess, students_list):
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

def simple_swap(student: Student, from_sess: Subject.Session, to_sess: Subject.Session, students_list: list[Student]) -> bool:
    """
    Attempt a simple swap from one session to another.
    Only makes the change if it increases overall happiness.
    """
    initial_happiness = hval(students_list)
    
    # Try the swap
    student.remove_session(from_sess)
    student.add_session(to_sess)
    
    new_happiness = hval(students_list)
    
    if new_happiness > initial_happiness:
        return True  # Keep the change
    else:
        # Revert the swap
        student.remove_session(to_sess)
        student.add_session(from_sess)
        return False

def swap_students(student1: Student, sess1: Subject.Session, student2: Student, sess2: Subject.Session, students_list: list[Student]) -> bool:
    """
    Swap two students between two sessions.
    Only makes the change if it increases overall happiness.
    """
    initial_happiness = hval(students_list)
    
    # Remove students from current sessions
    student1.remove_session(sess1)
    student2.remove_session(sess2)
    
    # Add to new sessions
    student1.add_session(sess2)
    student2.add_session(sess1)
    
    new_happiness = hval(students_list)
    
    if new_happiness > initial_happiness:
        return True  # Keep the change
    else:
        # Revert the swap
        student1.remove_session(sess2)
        student2.remove_session(sess1)
        student1.add_session(sess1)
        student2.add_session(sess2)
        return False

def optimize_schedule(students: list[Student], max_iterations=100, improvement_threshold=0.0001):
    """
    Main optimization function that attempts to improve the overall happiness score
    through incremental improvements and avoiding local optima.
    """
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
            if handle_time_improved(student, students):
                total_changes += 1
                
            if handle_gpa_improved(student, students):
                total_changes += 1
                
            if handle_lunch_improved(student, students):
                total_changes += 1
        
        # Calculate new happiness score
        new_score = hval(students)
        improvement = (new_score - current_score) / current_score if current_score > 0 else 0
        
        print(f"Iteration {iteration}: happiness = {new_score} (change: {improvement:.4f}, changes: {total_changes})")
        
        # Check for significant improvement
        if abs(improvement) < improvement_threshold:
            plateau_count += 1
            # Try random reshuffling to escape local optimum
            if plateau_count >= 3:
                print("Optimization plateaued, attempting random reshuffling...")
                if try_random_improvements(students, 10):  # Try 10 random improvements
                    plateau_count = 0  # Reset if successful
                else:
                    plateau_count += 1  # Increment if unsuccessful
        else:
            plateau_count = 0  # Reset plateau counter if improving
            
        # Stop if we've plateaued too many times
        if plateau_count >= 5:
            print(f"Optimization plateaued after {iteration} iterations")
            break
            
        # Stop if no changes were made
        if total_changes == 0:
            print("No further improvements possible")
            break
            
        current_score = new_score
        score_history.append(current_score)
        
        # Randomize student order periodically to avoid bias
        if iteration % 5 == 0:
            random.shuffle(sorted_students)
    
    final_score = hval(students)
    print(f"Optimization complete. Final happiness: {final_score}")
    
    # Only report positive improvement percentage
    if final_score > initial_score:
        improvement_pct = ((final_score - initial_score) / initial_score) * 100
        print(f"Total improvement: {improvement_pct:.2f}%")
    else:
        print("No overall improvement achieved.")
    
    return final_score

def try_random_improvements(students: list[Student], num_attempts: int) -> bool:
    """
    Try random swaps between sessions to escape local optima.
    Returns True if any improvement was made.
    """
    made_improvement = False
    
    for _ in range(num_attempts):
        # Pick a random student
        student = random.choice(students)
        
        if not student.sessions:
            continue
            
        # Pick a random session
        current_sess = random.choice(student.sessions)
        subject = current_sess.parent
        
        # Find an alternative session
        alt_sessions = [s for s in subject.sessions if s != current_sess]
        
        if not alt_sessions:
            continue
            
        alt_sess = random.choice(alt_sessions)
        
        # Try to swap if there's no conflict
        if not conflicts_schedule(alt_sess, [s for s in student.sessions if s != current_sess]):
            initial_happiness = hval(students)
            
            if alt_sess.current_enrollment() < alt_sess.capacity:
                # Simple swap
                student.remove_session(current_sess)
                student.add_session(alt_sess)
                
                new_happiness = hval(students)
                
                if new_happiness > initial_happiness:
                    made_improvement = True
                    break
                else:
                    # Revert
                    student.remove_session(alt_sess)
                    student.add_session(current_sess)
            else:
                # Try to find a student to swap with
                potential_swaps = []
                
                for other in alt_sess.students:
                    if not conflicts_schedule(current_sess, [s for s in other.sessions if s != alt_sess]):
                        potential_swaps.append(other)
                        
                if potential_swaps:
                    other = random.choice(potential_swaps)
                    
                    # Perform swap
                    student.remove_session(current_sess)
                    other.remove_session(alt_sess)
                    student.add_session(alt_sess)
                    other.add_session(current_sess)
                    
                    new_happiness = hval(students)
                    
                    if new_happiness > initial_happiness:
                        made_improvement = True
                        break
                    else:
                        # Revert
                        student.remove_session(alt_sess)
                        other.remove_session(current_sess)
                        student.add_session(current_sess)
                        other.add_session(alt_sess)
    
    return made_improvement

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

            # Late preference - higher start time => higher rank (better)
            if p["late"]:
                ordered = sorted(subj.sessions, key=lambda s: s.start_time)
                rank = ordered.index(sess) + 1
                total += p["late"] * rank

            # GPA preference - higher GPA => higher rank (better)
            if p["gpa"]:
                ordered = sorted(subj.sessions, key=lambda s: s.prof_gpa)
                rank = ordered.index(sess) + 1
                total += p["gpa"] * rank

        # Lunch break happiness (if they have a lunch gap)
        if p["lunch"]:
            class_times = [s.start_time for s in stu.sessions]
            has_gap = not all(hour in class_times for hour in LUNCH_HOURS)
            if has_gap:
                total += p["lunch"]
                
    return total 