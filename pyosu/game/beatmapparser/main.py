# Copyright (c) FlamesCoder. Licensed under the MIT Licence.
# See the LICENCE file in the repository root for full licence text.

import os

from pyosu.settings import ROOT_DIR
from pyosu.game.beatmapparser.beatmapparser import BeatmapParser


def parse_level(osu_file_path: str) -> dict:
    parser = BeatmapParser()

    parser.parseFile(os.path.join(ROOT_DIR, f"songs/{osu_file_path}"))

    return parser.build_beatmap()
