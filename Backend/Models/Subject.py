class Subject:
    def __init__(self, name, session, gpa):
        self.name = name
        self.session = np.array(session)
        self.gpa = np.array(gpa)