# %%
import sys

sys.path.append("/home/ldorigo/MEGA/DTU/Q2/social_graphs/mediawiki/")


from os import remove
import wikipedia as wp
from mediawiki import MediaWiki, MediaWikiPage
from typing import Dict
import regex as re
from pathlib import Path
import os
from tqdm.auto import tqdm
import json
from bs4 import BeautifulSoup, Tag

#%% Load in the full category tree:

full_tree_clean_path = Path.cwd() / "shared_data" / "full_category_tree_clean.json"
with open(full_tree_clean_path, "r") as f:
    root_tree = json.load(f)


# %%
# The API returns outgoing links that include those in template boxes at the end of pages, which adds enormous amount of
# Links that are not really relevant. We thus need to extract the links by hand, which is extremely slow.
def get_inline_links(page: MediaWiki.page):
    api_links = page.links
    # print(f"Parsing links for page: {page.title}")
    relevant_sections = [
        section
        for section in page.sections
        if section not in ["See also", "References", "Bibliography", "External links"]
    ]
    # Also parse the initial section (0)
    relevant_sections.append(0)
    actual_links = {}
    for section in tqdm(relevant_sections):
        # print(f"Parsing links of section {section}")
        tentative_links = page.parse_section_links(section)
        if not tentative_links:
            continue
        # print(tentative_links)
        # Remove all references and external links
        no_references = []
        for name, url in tentative_links:
            if not re.search("\[[0-9]*\]", name) and not re.search("^FILE", name):
                if re.search("en\.wikipedia\.org", url):
                    no_references.append((name, url))
        for name, url in no_references:
            link_title = re.search("/([^/]+)(/?)$", url)
            if link_title:
                actual_title = link_title[1].replace("_", " ")

                if actual_title not in api_links:
                    # print(f"Warning: inline link {actual_title} not found in api links")
                    continue
                actual_links[actual_title] = (
                    actual_links.setdefault(actual_title, 0) + 1
                )
    return actual_links


def process_page(name: str, current_dir: Path, redirects: Dict) -> Dict:
    filepath = current_dir.joinpath(name.replace("/", "_") + ".json")

    # To enable resuming: if the article was already downloaded, just read it from file
    if filepath.exists():
        with open(filepath.as_posix(), "r") as f:
            return json.load(f)

    page = mw.page(name)
    results = {}
    ## Add all redirects to the flat list
    for r in page.redirects:
        redirects[r] = name
    ## Save all outgoing links
    results["links"] = get_inline_links(page)
    ## Save secondary categories of the page
    results["categories"] = page.categories
    ## Also save a reference to the redirects within the page itself
    results["redirects"] = page.redirects
    ## Finally, save the contents and the url for quick reference:
    results["url"] = page.url
    results["content"] = page.content

    ## Save to a json file
    with open(filepath, "w+") as f:
        json.dump(results, f)
    return results


def process_tree(
    root_name: str, root_node: Dict, current_dir: Path, redirects: Dict
) -> Dict:
    results = {}
    for link in tqdm(root_node["links"]):
        results[link] = {}
        results[link]["category"] = root_name
        results[link]["data"] = process_page(link, current_dir, redirects)
    for sub_category in tqdm(root_node["sub-categories"]):
        new_dir = current_dir.joinpath(sub_category)
        if not new_dir.exists():
            os.mkdir(new_dir)
        cat_results = process_tree(
            root_name=sub_category,
            root_node=root_node["sub-categories"][sub_category],
            current_dir=new_dir,
            redirects=redirects,
        )
        results.update(cat_results)
    return results


# Flat dict of redirects for later reference
redirects = {}


data_path = Path.cwd().joinpath("private_data/full_wiki_data")
if not data_path.exists():
    os.mkdir(data_path)

mw = MediaWiki()
content_tree = process_tree(
    root_name="custom_root",
    root_node=root_tree,
    current_dir=data_path,
    redirects=redirects,
)

# %%

# Clean some pages that were overlooked

del content_tree["Antidepressant"]
del content_tree["Reversible inhibitor of monoamine oxidase A"]
del content_tree["Stimulant"]
del content_tree["Anxiolytic"]
del content_tree["Histone deacetylase inhibitor"]
del content_tree["Norepinephrine–dopamine disinhibitor"]
del content_tree["Norepinephrine–dopamine reuptake inhibitor"]
del content_tree["Monoamine oxidase inhibitor"]
del content_tree["Heterocyclic antidepressant"]
del content_tree["Tricyclic antidepressant"]
del content_tree["Barbiturate"]
del content_tree["Aphrodisiac"]
# del content_tree["Tricyclic antidepressant"]


# %%
full_wiki_data_path = Path.cwd() / "shared_data" / "full_wiki_data.json"
with open(full_wiki_data_path, "w+") as f:
    json.dump(content_tree, f, indent=2)

# %%
