import os
import pprint

from pyosu.settings import ROOT_DIR
from pyosu.game.beatmapparser.main import BeatmapParser

parser = BeatmapParser()

# parser.parseFile(os.path.join(ROOT_DIR, "songs/369354 Equilibrium - Waldschrein/Equilibrium - Waldschrein (Maakkeli) [Mein Land].osu"))
parser.parseFile(os.path.join(ROOT_DIR, "songs/FlamesCoder - Acheron/FlamesCoder - Acheron (flame121) [Easy].osu"))
res = parser.build_beatmap()
pprint.pprint(res)
