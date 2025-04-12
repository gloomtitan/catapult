# name-scla-econ-eng-cs-ma-chem
# person1-7-2-11-9-4

def parse_schedule(raw):
    parts = raw.split('-')
    
    times = {
        name = parts[0],
        scla = parts[1],
        econ = parts[2],
        econ = parts[3],
        engr = parts[4],
        cs = parts[5],
        ma = parts[6],
        chem = parts[7]
    }
    return name, times

def eval_schedule(): # Gives us the score for a person's timetable
    
    name, times = parse_scedule(raw):
    
    tue_thu = [times[c] for c in ["scla", "econ", "eng"] if times[c] > 0]
    mwf = [times[c] for c in ["ma", "cs", "chem"] if times[c] > 0]
    
    scores = {}
    total_score = 0
    
    def score_block(classes, day_group):
        scores_local = {}