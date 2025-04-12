class Student:
    def __init__(self, id, preferences, subject_list):
        self.id = id
        self.preferences = preferences
        self.subject_list = subject_list

    @staticmethod
    def load_students(file_path='test-cases.txt'):
