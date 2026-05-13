def evaluate_score(score):

    if score >= 0.90:
        marks = 10
        evaluation = "Excellent Answer Match"

    elif score >= 0.75:
        marks = 8
        evaluation = "Good Answer Match"

    elif score >= 0.55:
        marks = 6
        evaluation = "Partial Answer Match"

    else:
        marks = 3
        evaluation = "Poor Answer Match"

    return marks, evaluation