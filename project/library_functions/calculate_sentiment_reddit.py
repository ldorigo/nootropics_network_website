import json

try:
    from config import Config
except ModuleNotFoundError:
    from project.config import Config
from textblob import TextBlob
from tqdm import tqdm


def calculate_sentiment_reddit(alternative_path=None, alternative_path_out=None):
    filepath_in = (
        alternative_path if alternative_path else Config.Path.reddit_data_with_NER
    )
    filepath_out = (
        alternative_path_out
        if alternative_path_out
        else Config.Path.reddit_data_with_NER_and_sentiment
    )
    with open(filepath_in) as file:
        drug_database_reddit = json.load(file)

    for post_id, post in tqdm(drug_database_reddit.items()):
        try:
            analysis = TextBlob(post["content"] + post["title"])
        except KeyError:
            analysis = TextBlob(post["body"] + post["title"])  # for comments
        post["polarity"] = analysis.polarity
        post["subjectivity"] = analysis.subjectivity

    with open(filepath_out, "w+") as file:
        json.dump(drug_database_reddit, file)
