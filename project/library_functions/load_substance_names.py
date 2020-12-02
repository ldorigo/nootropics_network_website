import json

from config import Config


def load_substance_names():
    with open(Config.Path.substance_names) as file:
        substance_names = json.load(file)

    return substance_names
