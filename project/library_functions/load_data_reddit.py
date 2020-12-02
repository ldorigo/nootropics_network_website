import json

try:
    from config import Config
except ModuleNotFoundError:
    from project.config import Config


def load_data_reddit(alternative_path=None):
    if alternative_path:
        filepath = alternative_path
    else:
        filepath = Config.Path.reddit_data_with_NER_and_sentiment
    with open(filepath) as file:
        drug_database_reddit = json.load(file)

    return drug_database_reddit
