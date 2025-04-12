class Student:
    def __init__(self, id, preferences, subject_list):
        self.id = id
        self.preferences = preferences
        self.subject_list = subject_list

    @staticmethod
    def from_line(line):
        line = line.strip()
        if not line:
            return None

        data_part, late, lunch, gpa = line.split('|')
        subject_parts = data_part.split('-')

        student_id = parts[0]
        class_times = list(map(int, parts[1:]))

        subject_names = ["scla", "econ", "eng", "cs", "ma", "chem", "pol", "hist"]
        subject_list = []

        for name, time in zip(subject_names, class_times):
            subject_list.append(Subject(name, [time], [0.0]))

        preferences = {
            "late": (int(late)),
            "lunch": (int(lunch)),
            "gpa": float(gpa)
        }

        return Student(student_id, preferences, subject_list)

    @staticmethod
    def load_students(file_path='test-cases.txt'):
        students = []
        with open(file_path, 'r') as f:
            lines = f.readlines()
            count = int(lines[0].strip())

            for line in lines[1:count + 1]:
                student = Student.from_line(line)
                if student:
                    students.append(student)

        return np.array(students, dtype=object)

# numpy array of students