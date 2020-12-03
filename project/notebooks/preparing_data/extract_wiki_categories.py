# %%
from typing import Set

try:
    from library_functions.config import Config
except ModuleNotFoundError:
    from project.library_functions.config import Config
import json
from library_functions import load_data_wiki
import sys

sys.path.append("..")
from mediawiki.mediawiki import MediaWiki

# %%
wiki_data = load_data_wiki()
# %%


with open(Config.Path.psychoactive_category_tree_clean, "r") as f:
    ct = json.load(f)


psychological_effect_root = [
    "Anxiogenics",
    "Anxiolytics",
    "Aphrodisiacs",
    "Depressogenics",
    "Entactogens and empathogens",
    "Mood stabilizers",
    "Oneirogens",
    "Psychoanaleptics",
    "Psycholeptics" "Antidepressants‎",
    "Stimulants",
]
# %%
psychological_effect_map = {
    "Antidepressants": [
        "Reversible inhibitors of MAO-A",
        "Azapirones",
        "Bicyclic antidepressants",
        "Monoamine oxidase inhibitors",
        "Noradrenergic and specific serotonergic antidepressants",
        "Norepinephrine-dopamine reuptake inhibitors",
        "Selective serotonin reuptake inhibitors",
        "Serotonin-norepinephrine reuptake inhibitors",
        "Tetracyclic antidepressants",
        "Tricyclic antidepressants",
    ],
    "Stimulants": [
        "Herbal and fungal stimulants",
        "RTI compounds",
        "Sympathomimetic amines",
        "Pyrrolidinophenones‎",
        "Masticatories‎",
        "Tobacco",
    ],
}
# %%
mw = MediaWiki()


#%%
ct = ct["Psychoactive drugs by mechanism of action"]

# %%
def build_category_mapping(category):
    def extract_categories(tree, current: Set[str]) -> Set[str]:
        if tree:
            for subcategory in tree["sub-categories"]:
                if subcategory not in current:
                    current.union(
                        extract_categories(tree["sub-categories"][subcategory], current)
                    )
                    current.add(subcategory)
        return current

    ct = mw.categorytree(category, depth=15)
    ct = ct[category]

    results = {
        key: extract_categories(ct["sub-categories"][key], set())
        for key in ct["sub-categories"].keys()
    }
    return results


# %%
categories_mechanism = build_category_mapping(
    "Psychoactive drugs by mechanism of action"
)
# Convert sets to lists to be able to save as json
for i in categories_mechanism:
    categories_mechanism[i] = list(categories_mechanism[i])

with open(Config.Path.wiki_mechanism_categories, "w+") as f:
    json.dump(categories_mechanism, f)
# %%
categories_effects = build_category_mapping("Drugs by psychological effects")

# Convert sets to lists to be able to save as json
for i in categories_effects:
    categories_effects[i] = list(categories_effects[i])

with open(Config.Path.wiki_effect_categories, "w+") as f:
    json.dump(categories_effects, f)
# %%

# Make a simple mapping between categories and substances
all_categories = set()

for category in wiki_data["categories"]:
    all_categories = all_categories.union(set(category))
print(f"Amount of categories: {len(all_categories)}")

category_inverse_mapping = {category: [] for category in all_categories}

for name, categories in zip(wiki_data["name"], wiki_data["categories"]):
    for category in categories:
        category_inverse_mapping[category].append(name)

with open(Config.Path.all_categories_to_names_mapping, "w+") as f:
    json.dump(category_inverse_mapping, f)
# %%
