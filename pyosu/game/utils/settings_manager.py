import json
import pathlib


def get_settings():
    with open("pyosu/settings.json", "r") as f:
        return json.load(f)

# todo create settings manager
