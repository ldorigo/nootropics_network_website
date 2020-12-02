import json
from typing import Dict, List
import random

try:
    import library_functions as lf
except ModuleNotFoundError:
    import project.library_functions as lf
try:
    from config import Config
except ModuleNotFoundError:
    from project.config import Config


def get_page_from_name(name: str) -> Dict:
    """Given a substance name (eventually one of its synonyms),
    return the corresponding wikipedia entry

    Args:
        name (str): name or synonym for the substance

    Returns:
        Dict: Dict containing name, redirects, links, contents, categories, and url
    """
    name = synonyms_to_names[name]
    wiki_data_index = wiki_data["name"].index(name)
    return {
        "name": wiki_data["name"][wiki_data_index],
        "url": wiki_data["url"][wiki_data_index],
        "categories": wiki_data["categories"][wiki_data_index],
        "content": wiki_data["content"][wiki_data_index],
        "links": wiki_data["links"][wiki_data_index],
        "synonyms": wiki_data["synonyms"][wiki_data_index],
    }


def get_random_page() -> Dict:
    """Return a random Wikipedia page

    Returns:
        Dict: Dict containing name, redirects, links, contents, categories, and url
    """
    name = random.choice(wiki_data["names"])
    return get_page_from_name(name)


def get_wiki_page_names(with_synonyms: bool = False) -> List[str]:
    """Get a list with the names of all the substance pages on wikipedia

    Args:
        with_synonyms (bool): include synonyms in the list
    Returns:
        List[str]: List containing all substance names on wikipedia , eventually with synonyms
    """

    names = wiki_data["name"]
    if with_synonyms:
        names += list(synonyms_to_names.keys())
        names = list(set(names))
    return names


def get_page_lengths() -> List[int]:
    """Get a list of all the page lengths, in characters

    Returns:
        List[int]: List of the number of characters in each wiki page
    """
    return [len(p) for p in wiki_data["content"]]


def get_wiki_synonyms_mapping() -> Dict[str, str]:
    """Return a dict mapping synonyms to the name of the wiki pages

    Returns:
        Dict[str, str]: Dict mapping synonyms (and names) to names
    """
    with open(Config.Path.synonym_mapping, "r") as f:
        return json.load(f)


wiki_data = lf.load_data_wiki()
synonyms_to_names = get_wiki_synonyms_mapping()
