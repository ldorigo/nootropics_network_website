from typing import Dict
import random

try:
    import library_functions as lf
except ModuleNotFoundError:
    import project.library_functions as lf

wiki_data = lf.load_data_wiki()
synonyms_to_names = lf.load_synonym_mappings()


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