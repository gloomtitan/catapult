def parse_schedule(raw):
    parts = raw.split("-")
    name = parts[0]
    times = {
        "scla": int(parts[1]),
        "econ": int(parts[2]),
        "eng": int(parts[3]),  # fixed key
        "cs": int(parts[4]),
        "ma": int(parts[5]),
        "chem": int(parts[6]),
    }
    return name, times


def eval_schedule(raw):
    name, times = parse_schedule(raw)

    tue_thu = [times[c] for c in ["scla", "econ", "eng"] if times[c] > 0]
    mwf = [times[c] for c in ["ma", "cs", "chem"] if times[c] > 0]

    scores = {}

    def score_block(classes):
        scores_local = {}
        count = len(classes)

        # Base score per class
        for t in classes:
            score = 0
            if 7 <= t <= 9:
                score -= 2
            if 12 <= t <= 14:
                score += 2
            scores_local[t] = score  # initialize

        # Bundle bonus
        classes_sorted = sorted(classes)
        for i in range(len(classes_sorted) - 1):
            if classes_sorted[i + 1] - classes_sorted[i] == 1:
                scores_local[classes_sorted[i]] += 1
                scores_local[classes_sorted[i + 1]] += 1

        # Penalty for >3 classes
        if count > 3:
            for k in scores_local:
                scores_local[k] -= 1

        return scores_local

    scores.update(score_block(tue_thu))
    scores.update(score_block(mwf))

    total_score = sum(scores.values())
    return total_score, scores


person1 = "#1-1-7-2-11-9-16"
score, class_scores = eval_schedule(person1)
print("Total Score:", score)
print("Class Scores:", class_scores)
