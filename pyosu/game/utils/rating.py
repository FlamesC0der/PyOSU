from pyosu.settings import RATING


def get_rating(accuracy: int):
    for threshold, grade in sorted(RATING.items(), reverse=True):
        if accuracy >= threshold:
            return grade
