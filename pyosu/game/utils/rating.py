# Copyright (c) FlamesCoder. Licensed under the MIT Licence.
# See the LICENCE file in the repository root for full licence text.

from pyosu.settings import RATING


def get_rating(accuracy: int):
    for threshold, grade in sorted(RATING.items(), reverse=True):
        if accuracy >= threshold:
            return grade
