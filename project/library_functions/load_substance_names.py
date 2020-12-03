import json

try:
    from library_functions.config import Config
except ModuleNotFoundError:
    from project.library_functions.config import Config


def load_substance_names():
    with open(Config.Path.substance_names) as file:
        substance_names = json.load(file)

    return substance_names
