#%%
import json
import os
from pathlib import Path
from typing import Generator
from psaw import PushshiftAPI

try:
    from config import Config
except ModuleNotFoundError:
    from project.config import Config

# %%
api = PushshiftAPI()
# %%
reddit_path = Config.Path.private_data_folder / "reddit_data"
os.mkdir(reddit_path)
# %%
reddit_comments_path = reddit_path.joinpath("comments")
reddit_submissions_path = reddit_path.joinpath("submissions")

os.mkdir(reddit_comments_path)
os.mkdir(reddit_submissions_path)
# %%


def save_submissions(submission):
    relevant_dict = {
        "title": submission.title,
        "author": submission.author,
        "timestamp": submission.created,
        "id": submission.id,
    }
    try:
        relevant_dict["content"] = submission.selftext
    except:
        relevant_dict["content"] = ""
    with open(
        reddit_submissions_path.joinpath(relevant_dict["id"] + ".json"), "w+"
    ) as f:
        json.dump(relevant_dict, f)


def save_comment(comment):
    relevant_dict = {
        "author": comment.author,
        "body": comment.body,
        "timestamp": comment.created,
        "id": "c__" + comment.id,
    }
    with open(reddit_comments_path.joinpath(relevant_dict["id"] + ".json"), "w+") as f:
        json.dump(relevant_dict, f)


# %%
all_submissions = api.search_submissions(
    subreddit="nootropics",
    filter=["title", "author", "created_utc", "id", "selftext", "url"],
)
# %%
def download_all_submissions(sub_generator: Generator):
    for i, sub in enumerate(sub_generator):

        if i % 100 == 0:
            print(f"Downloading submissions {i} - {i+100}.")

        save_submissions(sub)


def download_all_comments(com_generator: Generator):
    for i, comment in enumerate(com_generator):

        if i % 100 == 0:
            print(f"Downloading comments {i} - {i+100}.")

        save_comment(comment)


# %%
all_comments = api.search_comments(
    subreddit="nootropics",
    filter=["author", "created_utc", "id", "body", "url"],
)
# %%

# %%
download_all_comments(all_comments)
# %%
