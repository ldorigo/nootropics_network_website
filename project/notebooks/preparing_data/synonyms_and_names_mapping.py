# %%
try:
    from library_functions.config import Config
except ModuleNotFoundError:
    from project.library_functions.config import Config
from library_functions import load_data_wiki, save_synonym_mapping

# %%


wiki_data = load_data_wiki.load_data_wiki()
# %%
save_synonym_mapping.save_synonym_mapping(wiki_data)
save_synonym_mapping.save_substance_names(wiki_data)
save_synonym_mapping.save_contents(wiki_data)
save_synonym_mapping.save_urls(wiki_data)
# %%
