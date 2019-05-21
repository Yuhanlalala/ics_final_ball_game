score = 0
def total(point):
    global score
    score += point
def get_score():
    return score
def clear_score():
    global score
    score = 0