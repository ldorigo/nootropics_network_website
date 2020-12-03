import json
from typing import Dict, List, Literal, Set, Tuple
import random

try:
    import library_functions as lf
except ModuleNotFoundError:
    import project.library_functions as lf
try:
    from library_functions.config import Config
except ModuleNotFoundError:
    from project.library_functions.config import Config

# pre-fetch/compute some stuff to make computations faster

wiki_data = lf.load_data_wiki()
with open(Config.Path.wiki_mechanism_categories, "r") as f:
    mechanism_categories_mapping = json.load(f)

with open(Config.Path.wiki_mechanism_categories, "r") as f:
    effects_categories_mapping = json.load(f)


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


def get_wiki_page_names(with_synonyms: bool = False) -> Set[str]:
    """Get a list with the names of all the substance pages on wikipedia

    Args:
        with_synonyms (bool): include synonyms in the list
    Returns:
        List[str]: List containing all substance names on wikipedia , eventually with synonyms
    """

    names = set(wiki_data["name"])
    if with_synonyms:
        names = names.union(synonyms_to_names.keys())
    return names


def get_wiki_synonyms_mapping() -> Dict[str, str]:
    """Return a dict mapping synonyms to the name of the wiki pages

    Returns:
        Dict[str, str]: Dict mapping synonyms (and names) to names
    """
    with open(Config.Path.synonym_mapping, "r") as f:
        return json.load(f)


synonyms_to_names = get_wiki_synonyms_mapping()
all_names_and_synonyms = get_wiki_page_names(with_synonyms=True)


def get_page_lengths() -> List[int]:
    """Get a list of all the page lengths, in characters

    Returns:
        List[int]: List of the number of characters in each wiki page
    """
    wiki_data["length"] = [len(p) for p in wiki_data["content"]]
    return wiki_data["length"]


def get_number_of_links() -> List[int]:
    """Get a list of the number of links of each page (only counting links to other substances)

    Returns:
        List[int]: List of the number of links that each page has towards other pages
    """
    valid_links_numbers = []
    wiki_data["valid_links"] = []
    for links in wiki_data["links"]:
        valid_links = [link for link in links if link.lower() in all_names_and_synonyms]
        valid_links_numbers.append(len(valid_links))
        wiki_data["valid_links"].append(valid_links)

    return valid_links_numbers


def get_number_of_categories() -> List[int]:
    """Get a list of the number of categories that each page is part of

    Returns:
        List[int]: List of the number of categories that each page belongs to
    """

    return [len(cats) for cats in wiki_data["categories"]]


def get_number_of_synonyms() -> List[int]:
    """Get a list of the number of synonyms (redirects) of each page

    Returns:
        List[int]: List of the number of redirects that each page has
    """

    return [len(syns) for syns in wiki_data["synonyms"]]


def get_name_by(indices: List[int]) -> List[str]:
    """Return the names corresponding to the indices passed as argument

    Args:
        indices (List[int]): List of indices of the pages for which to get names

    Returns:
        List[str]: List of names corresponding to the given indices
    """
    return [wiki_data["name"][i] for i in indices]


def get_top(property: str, amount: int = 10, reverse=False) -> List[Tuple[str, int]]:
    tuples = zip(
        wiki_data["name"],
        [p if type(p) == int else len(p) for p in wiki_data[property]],
    )
    sorted_tuples = sorted(
        tuples, key=lambda x: x[1] if type(x[1]) == int else len(x[1]), reverse=reverse
    )
    return sorted_tuples[:amount]


def get_wiki_data() -> Dict:
    """Get a copy of the wiki_data dict

    Returns:
        Dict: shallow copy of the wiki_data dict
    """
    return wiki_data.copy()


def get_root_category_mapping(which: Literal["effects", "mechanisms"]) -> Dict:
    if which == "effects":
        return effects_categories_mapping.copy()
    elif which == "mechanisms":
        return mechanism_categories_mapping
    else:
        raise RuntimeError("Can only be one of 'effects','mechanisms'")