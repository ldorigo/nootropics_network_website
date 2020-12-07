# %%

try:
    import library_functions as lf
except ModuleNotFoundError:
    import project.library_functions as lf

try:
    from config import Config
except ModuleNotFoundError:
    from project.config import Config

import wojciech as w

# %% md

## Let's look at some basic stats about our data:
### Reddit:
# %%
reddit_data = lf.load_data_reddit()
# %%
number_of_posts = len(reddit_data)

# %%
length = sum([len(p["title"]) + len(p["content"]) for p in reddit_data.values()])
wordlength = sum([p["n_of_words"] for p in reddit_data.values()])
# %%
average_length = length / number_of_posts
# %%
n_of_matches = sum([len(p["matches"]) for p in reddit_data.values()])
# %%
average_matches = n_of_matches / number_of_posts
# %%
n_of_posts_with_links = sum([1 for p in reddit_data.values() if len(p["matches"]) >= 2])
# %%

### Wiki:

wiki_data = lf.load_data_wiki()
# %%
n_of_pages = len(wiki_data["name"])

# %%
total_length_wiki = sum([len(p) for p in wiki_data["content"]])
average_length_wiki = total_length_wiki / n_of_pages
# %%
wiki_graph = lf.create_graph_wiki()
# %%
wiki_graph_directed = wiki_graph.to_directed()
# %%
outgoing_links = [d for n, d in wiki_graph_directed.out_degree]
# %%
import numpy as np

# %%
average_links = np.mean(outgoing_links)
# %%
