# name-scla-econ-eng-cs-ma-chem
# person1-7-2-11-9-16


class Student:
    def __init__(self, raw_data):
        name, times = parse_schedule(raw_data)
        self.name = name
        self.times = times

def parse_schedule(raw):
    parts = raw.split('-')
    name = parts[0]
    times = {
        "scla" : int(parts[1]),
        "econ" : int(parts[2]),
        "engr" : int(parts[3]),
        "cs" : int(parts[4]),
        "ma" : int(parts[5]),
        "chem" : int(parts[6])
    }
    return name, times

def eval_schedule(raw): # Gives us the score for a person's timetable
    student = Student(raw)    
    
    scores = {}
    total_score = 0
    
    def score_block(classes, day_group):
        scores_local = {}
        count = len(classes)
        for t in classes:
            score = 0
            if 7 <= t <= 9:
                pass    
    return 0
