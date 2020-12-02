
# %%
from os import remove
import wikipedia as wp
from mediawiki import MediaWiki
from typing import Dict
import regex as re
from pathlib import Path
import os
from tqdm.auto import tqdm
import json
# %%
mw = MediaWiki()


# %% [markdown]
# Obtain a "category tree" for psychotropics from which we weed out irrelevant stuff:

# %%
# ct= mw.categorytree("Drugs by psychological effects", depth=15)

# # %% [markdown]
# # This takes a long time to compute, so let's save it to json in case we need to recover it:

# # %%
# with open("psychoactive_category_tree_raw.json", "w+") as f:
#     json.dump(ct, f)
# #%% 

# with open("psychoactive_category_tree_raw.json", "r") as f:
#     ct = json.load(f)

# # %%
# root_tree = ct["Drugs by psychological effects"]
# root_subs = root_tree["sub-categories"]
# psychoanaleptics_subs = root_subs["Psychoanaleptics"]["sub-categories"]
# stimulants_tree = psychoanaleptics_subs["Stimulants"]

# # %% [markdown]
# # Do some manual cleaning to remove noise:
# # %% [markdown]
# # ### Stimulants

# # %%
# h_f_stimulants = stimulants_tree["sub-categories"]['Herbal and fungal stimulants']

# tobacco = h_f_stimulants["sub-categories"]["Tobacco"]
# tobacco_sub = tobacco["sub-categories"]
# tobacco_links = tobacco["links"]

# # Other than "snus", subcategories are irrelevant
# to_delete = []
# for i in tobacco_sub.keys():
#     if i not in ["Snus"]:
#         print(f"Deleted {i}")
#         to_delete.append(i)
        
# for td in to_delete:
#     try:
#         del tobacco_sub[td]
#     except:
#         print(f"could not delete {td}")
# # Delete irrelevant pages:

# for i in ["List of tobacco-related topics",
#           "Animals and tobacco smoke", 
#           "Cultivation of tobacco",
#           "Curing of tobacco",   
#           "George Augustine Washington",
#             "Types of tobacco",
#             "Tobacco smoke",
#             "Tobacco products",
#             "Tobacco pouch",
#             "Tobacco politics",
#             "Ten Motives",
#             "Tobacco and art",
#             "Tobacco and other drugs",
#             "Tobacco BY-2 cells",
#             "Tobacco factory",
#          "Prevalence of tobacco use"]:
#     try:
#         print(f"removing {i}")
#         tobacco_links.remove(i)
#     except:
#         print(f"Could not remove {i}")
# h_f_stimulants['links'].remove("Areca nut production in India")
# stimulant_subcategories = stimulants_tree["sub-categories"]
# sm_amines=stimulant_subcategories['Sympathomimetic amines']
# sm_amines['links'].remove("List of methylphenidate analogues")
# stimulants_tree["links"].remove("List of investigational sleep drugs")
# stimulants_tree["links"].remove("List of phenyltropanes")

# # Delete the top-level stimulants category, which is duplicate
# del root_subs["Stimulants"]

# # %% [markdown]
# # ### nootropics

# # %%
# nootropics_tree = psychoanaleptics_subs["Nootropics"]
# nootropics_tree["links"].remove("Nootropic")
# nootropics_tree["links"].remove("Neuroenhancement")
# nootropics_tree["links"].remove("Performance-enhancing substance")
# nootropics_tree["links"].remove("Template:Psychostimulants, agents used for ADHD and nootropics")
# nootropics_subcategories = nootropics_tree["sub-categories"]
# del nootropics_subcategories["Smart drugs in fiction"]

# # %% [markdown]
# # ### Antidepressants

# ad_tree = psychoanaleptics_subs["Antidepressants"]
# to_remove = ["Antidepressants","Template:Antidepressants","List of antidepressants",
#      "List of countries by antidepressant consumption","Antidepressant discontinuation syndrome",
#     "Antidepressants and suicide risk","Antidepressants in Japan",
#     "List of investigational antidepressants","Listening to Prozac",
#     "Neurobiological effects of physical exercise","Pharmacology of antidepressants",
#     "Second-generation antidepressant","Serotonin antagonist and reuptake inhibitor",
#      "Serotonin modulator and stimulator"]
# %%
def remove_from_links(category, to_remove):
    for i in to_remove:
        try:    
            print(f"Removing {i}.")
            category["links"].remove(i)
        except:
            print(f"Unable to remove{i}")

# %% 
# remove_from_links(ad_tree, to_remove)
# ad_tree["sub-categories"]["Norepinephrine-dopamine reuptake inhibitors"]["links"].remove("List of methylphenidate analogues")
# to_remove= ["Antidepressant discontinuation syndrome","Allosteric serotonin reuptake inhibitor",
#             "Development and discovery of SSRI drugs", "Selective serotonin reuptake inhibitor"]
# remove_from_links(ad_tree["sub-categories"]["Selective serotonin reuptake inhibitors"], to_remove)
# to_remove= ["Antidepressant discontinuation syndrome","Serotonin–norepinephrine reuptake inhibitor"]
# remove_from_links(ad_tree["sub-categories"]["Serotonin-norepinephrine reuptake inhibitors"], to_remove)
# psychoanaleptics_subs["Antidementia agents"]["links"].remove("Template:Anti-dementia drugs")
# # Remove the top-level antidepressants category (duplicate)
# del root_subs["Antidepressants"]
# ### Remove psychedelics, euphoriants, deliriants and dissociative drugs, which aren;t nootropics
# del root_subs["Deliriants"]
# del root_subs["Psychedelic drugs"]
# del root_subs["Dissociative drugs"]
# del root_subs["Euphoriants"]
# # Psycholeptics are also likely nonrelevant
# del root_subs["Psycholeptics"]

# # %% [markdown]
# # ### Anxiolitics

# # %%
# anxiolitics = root_subs["Anxiolytics"]
# to_delete = ["List of investigational anxiolytics", "Serotonin antagonist and reuptake inhibitor"]
# remove_from_links(anxiolitics, to_delete)
# barbiturates = anxiolitics["sub-categories"]["Barbiturates"]
# del barbiturates["sub-categories"]["Barbiturates-related deaths"]
# to_delete = ["Mood stabilizer", "List of antidepressants","List of adverse effects of valproate semisodium",
#             "List of investigational antidepressants","Template:Mood stabilizers"]
# remove_from_links(root_subs["Mood stabilizers"], to_delete)

# %% [markdown]
# ### Save the resulting clean tree:

# %%
psychoactive_tree_path = Path.cwd() / "shared_data" / "psychoactive_category_tree_clean.json"
# with open(psychoactive_tree_path, "w+") as f:
#     json.dump(root_tree, f)

# %%

with open(psychoactive_tree_path, "r") as f:
    psychoactive_tree = json.load(f)


# %% [markdown]

## Now let's do the same for categories under "dietary supplements"


# %% 

ct= mw.categorytree("Dietary supplements", depth=15)

# %%
supplements_ct_dir = Path.cwd() / "shared_data" / "dietary_supplements_category_tree_raw.json"

# %%
with open(supplements_ct_dir, "w+") as f:
    json.dump(ct, f)

# %%
with open(supplements_ct_dir, "r") as f:
    ct = json.load(f)

# %%
supplements_tree = ct["Dietary supplements"]
supplements_links = supplements_tree["links"]
to_remove = ["Dietary supplement", "Alternative treatments used for the common cold",
"Clinical trials on glucosamine and chondroitin","Enforcement actions against açaí berry supplement manufacturers",
"Ensure", "Good manufacturing practice", "GU Energy Labs","Herbal Magic", "Herbal medicine",
"Herbal viagra", "Jimmy Joy (company)", "Korea Ginseng Corporation", "Mellin's Food",
"Met-Rx", "Metabolife", "Natural Products Association", "Nutrilite", "Nutriway",
"PowerBar", "Prozis", "Radio Malt", "Medical uses of silver", "Sports drink", "Sports nutrition",
"USANA Health Sciences", "Vitamer", "You Bar", "Template:Dietary supplement" ]
remove_from_links(supplements_tree, to_remove=to_remove)
del supplements_tree["sub-categories"]["Relaxation drinks"]
del supplements_tree["sub-categories"]["Sports nutrition and bodybuilding supplement companies"]
bodybuilding = supplements_tree["sub-categories"]["Bodybuilding supplements"] 
to_remove = ["Bodybuilding supplement", "Pre-workout", "Protein bar", "USANA Health Sciences"]
remove_from_links(bodybuilding, to_remove=to_remove)
del bodybuilding["sub-categories"]["Sports nutrition and bodybuilding supplement companies"]
del supplements_tree["sub-categories"]["Energy drinks"]
del supplements_tree["sub-categories"]["Energy food products"]
del supplements_tree["sub-categories"]["Nutritional supplement companies"]
vitamins = supplements_tree["sub-categories"]["Vitamins"]
del vitamins["sub-categories"]["Hypervitaminosis"]
del vitamins["sub-categories"]["Vitamin deficiencies"]
to_remove = ["Vitamin", "Prenatal vitamins", "Bleach and recycle", "Canada's Food Guide",
"Dietary Reference Intake", "Flintstones Chewable Vitamins", "Megavitamin therapy", "Myers' cocktail", "Multivitamin",
"One A Day", "Reference Daily Intake"]
remove_from_links(vitamins, to_remove)
vitamins["sub-categories"]["Vitamers"]["links"].remove("Vitamer")
vitamins["sub-categories"]["Vitamers"]["links"].remove("Chemistry of ascorbic acid")
bvit = vitamins["sub-categories"]["B vitamins"]
b12 = bvit["sub-categories"]["Vitamin B12"]
del b12["sub-categories"]["Deaths from pernicious anemia"]
to_delete = ["Cobalamin biosynthesis", "Vitamin B12 deficiency", "Vitamin B12 total synthesis"]
remove_from_links(b12, to_delete)
thiamine = bvit["sub-categories"]["Thiamine"]
to_delete = ["Thiamine deficiency","Wernicke encephalopathy", "Vitamin B1 analogue", "Wernicke–Korsakoff syndrome"]
remove_from_links(thiamine, to_delete)
cvit = vitamins["sub-categories"]["Vitamin C"]
del cvit["sub-categories"]["Deaths from scurvy"]
to_delete = ["Chemistry of ascorbic acid","Intravenous ascorbic acid",
"James Lind", "Scurvy", "Albert Szent-Györgyi","Vitamin C and the common cold",
"Vitamin C and the Common Cold (book)", "Vitamin C megadosage", "John Woodall"]
remove_from_links(cvit, to_delete)
dvit = vitamins["sub-categories"]["Vitamin D"]
to_delete = ["Health effects of sunlight exposure", "Osteomalacia", "Rickets", "Vitamin D and respiratory tract infections",
"Tuberculosis management", "Vitamin D and Omega-3 Trial", "Vitamin D deficiency", "Vitamin D receptor",
"Vitamin D toxicity", "Vitamin D-binding protein","X-linked hypophosphatemia" ]
remove_from_links(dvit, to_delete)


# %%
supplements_tree_clean_path = Path.cwd() / "shared_data" / "dietary_supplements_category_tree_clean.json"
with open(supplements_tree_clean_path, "w+") as f:
    json.dump(supplements_tree, f)

#%%

with open(supplements_tree_clean_path, "r") as f:
    supplements_tree = json.load(f)


# %% [markdown]

## Let's create an artificial top-level category to allow us to work on a single tree:

toplevel_category = {
    "depth": -1,
    "sub-categories" : {
        "psychoactive drugs": psychoactive_tree,
        "dietary supplements": supplements_tree,
    },
    "links" : [],
    "parent-categories": []
}

# %%
full_tree_clean_path = Path.cwd() / "shared_data" / "full_category_tree_clean.json"
with open(full_tree_clean_path, "w+") as f:
    json.dump(toplevel_category, f)
# %%

# %%
