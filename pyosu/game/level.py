import os
import re

import pygame

from pyosu.game.beatmapparser.main import parse_level
from pyosu.game.utils.image_loader import load_image
from pyosu.settings import ROOT_DIR

info_pattern = re.compile(r"^(.+) \((.+)\) \[(.+)]$")


def get_levels() -> list[dict]:
    levels = []
    for level in os.listdir(os.path.join(ROOT_DIR, "songs")):
        if os.path.isdir(os.path.join(ROOT_DIR, f"songs/{level}")):

            new_level = {
                "level_name": level,
                "levels": [],
                "bg": pygame.Surface((1, 1)),
            }

            for file in os.listdir(os.path.join(ROOT_DIR, f"songs/{level}")):
                if os.path.isfile(os.path.join(ROOT_DIR, f"songs/{level}/{file}")):
                    name, extension = file.rsplit(".")
                    if extension == "osu":  # osu files
                        match = info_pattern.match(name)
                        name, author, difficulty = [match.group(g) for g in range(1, 3 + 1)]
                        new_level["levels"].append(
                            {
                                "name": name,
                                "author": author,
                                "difficulty": difficulty,
                                "data": parse_level(f"{level}/{file}")
                            }
                        )
                    elif extension in ["png", "PNG", "jpg", "jpeg"]:  # images
                        new_level["bg"] = load_image(os.path.join(ROOT_DIR, f"songs/{level}/{file}"))
            levels.append(new_level)
    return levels
