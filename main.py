
def calculate_next_review_time(last_review: int, this_review: int, correct: bool):
    """Simple, naive algorithm"""
    if not correct:
        return 0
    else:
        return (this_review - last_review) * 1.1
