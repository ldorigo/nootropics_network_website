import json
from typing import Dict, List, Literal, Set, Tuple
import random

try:
    import library_functions as lf
except ModuleNotFoundError:
    import project.library_functions as lf
try:
    from config import Config
except ModuleNotFoundError:
    from project.config import Config

# pre-compute some stuff for efficiency
reddit_data = lf.load_data_reddit()
post_lengths = [len(data["title"] + data["content"]) for data in reddit_data.values()]
n_of_matches_per_post = [len(data["matches"]) for data in reddit_data.values()]


def get_post_lengths() -> List[int]:
    """Get a list of the lengths of individual posts

    Returns:
        List[int]: The length in characters of each of the reddit posts
    """
    return post_lengths.copy()


def get_n_of_matches_per_post() -> List[int]:
    return n_of_matches_per_post.copy()


def get_top_posts(
    attribute: Literal["length", "mentions"], reverse: bool = False, amount: int = 10
) -> List[Tuple[str, int, str]]:
    tuples = []
    for index, (id, post) in enumerate(reddit_data.items()):

        if attribute == "mentions":
            attr = n_of_matches_per_post[index]
        else:
            attr = post_lengths[index]
        tuples.append(
            (post["title"], attr, f"https://www.reddit.com/r/Nootropics/comments/{id}")
        )

    sorted_tuples = sorted(tuples, key=lambda x: x[1], reverse=reverse)

    return sorted_tuples[:amount]