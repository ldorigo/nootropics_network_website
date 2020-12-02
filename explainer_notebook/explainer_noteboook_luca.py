# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
# get_ipython().run_line_magic("load_ext", "autoreload")

# get_ipython().run_line_magic("autoreload", "2")
# get_ipython().run_line_magic("matplotlib", "inline")
from tqdm import tqdm
from config import Config
import library_functions as lf
import wojciech as w
from ipywidgets import widgets
import json
import community
import plotly.graph_objects as go
import matplotlib.pyplot as plt

import networkx as nx
import matplotlib

# %% [markdown]
#  ## Detecting Communities and visualizing them
# 
#  Let's load in our graphs:

# %%
graph_reddit = lf.create_graph_reddit(
    max_drugs_in_post=6,  # Ignore posts that have too many substances in them, as they are likely noise
    min_edge_occurrences_to_link=2,  # Include all mentions
    include_link_contents=True,
    include_node_contents=True,
    min_content_length_in_characters=25,
)
graph_reddit = w.graph.largest_connected_component(graph_reddit)

# Same for wikipedia, but here we also need to convert to an undirected graph
graph_wiki = w.graph.largest_connected_component(lf.create_graph_wiki().to_undirected())

# %% [markdown]
#  Let's look at our graphs. First, let's compute a layout, as it is an expensive operation and only needs to happe once:

# %%
# Compute positions, both taking edge weights into account and not doing so.
positions_reddit_weighted = lf.get_fa2_layout(
    graph=graph_reddit, edge_weight_attribute="count"
)
positions_reddit_unweighted = lf.get_fa2_layout(graph=graph_reddit)

positions_wiki = lf.get_fa2_layout(graph=graph_wiki)

# %% [markdown]
#  And let's just draw them as-is, with edge thickness corresponding to how often the two substances co-occur:

# %%

# figure_weighted = lf.plotly_draw.draw_graph_plotly(
#     graph=graph_reddit,
#     positions=positions_reddit_weighted,
#     node_size_attribute="degree",  # Size nodes by degree
#     edge_weight_attribute="count",  # Size links by how often they appear, i.e. how often the two substances are mentionned together
# )
# figure_unweighted = lf.plotly_draw.draw_graph_plotly(
#     graph=graph_reddit,
#     positions=positions_reddit_unweighted,
#     node_size_attribute="degree",  # Size nodes by degree
#     edge_weight_attribute="count",  # Size links by how often they appear, i.e. how often the two substances are mentionned together
# )
# widgets.HBox([figure_unweighted, figure_weighted])

# %% [markdown]
#  From these visualizations, it can be hard to see if there is any specific structure to the graph. Let's apply both the louvain and the infomap algorithm to detect communities:

# %%
reddit_graph, reddit_dendrogram = lf.assign_louvain_communities(graph_reddit)
wiki_graph, wiki_dendrogram = lf.assign_louvain_communities(graph_wiki)
lf.get_infomap_communities(reddit_graph, reddit_edge_weight="count")
lf.get_infomap_communities(wiki_graph)


# %%

# figure_weighted_colored_by_louvain_community = lf.plotly_draw.draw_graph_plotly(
#     graph=graph_reddit,
#     positions=positions_reddit_weighted,
#     node_size_attribute="degree",  # Size nodes by degree
#     edge_weight_attribute="count",  # Size links by how often they appear, i.e. how often the two substances are mentionned together
#     node_color_attribute="louvain_community_reddit",
# )

# figure_weighted_colored_by_infomap_community = lf.plotly_draw.draw_graph_plotly(
#     graph=graph_reddit,
#     positions=positions_reddit_weighted,
#     node_size_attribute="degree",  # Size nodes by degree
#     edge_weight_attribute="count",  # Size links by how often they appear, i.e. how often the two substances are mentionned together
#     node_color_attribute="infomap_community",
# )

# figure_unweighted_colored_by_community = lf.plotly_draw.draw_graph_plotly(
#     graph=graph_reddit,
#     positions=positions_reddit_unweighted,
#     node_size_attribute="degree", # Size nodes by degree
#     edge_weight_attribute="count", # Size links by how often they appear, i.e. how often the two substances are mentionned together
#     node_color_attribute="louvain_community_reddit"
# )
# widgets.HBox(
#     [
#         figure_weighted_colored_by_louvain_community,
#         figure_weighted_colored_by_infomap_community,
#     ]
# )

# %% [markdown]
#  Interesting! blablabla say some stuff about what the communities correspond to.
#  Seems like the infomap algorithm isn't that good here, likely due to the fact that the network is highly connected.
# %% [markdown]
#  Let's look at the overlap between the communities found by louvain and the categories defined on wikipedia, to see if the algorithm picked up interesting information.

# %%
communities_reddit = lf.inverse_communities_from_partition(
    community.partition_at_level(reddit_dendrogram, 1)
)
communities_wiki = lf.inverse_communities_from_partition(
    community.partition_at_level(wiki_dendrogram, 1)
)


# %%
with open(Config.Path.all_categories_to_names_mapping, "r") as f:
    categories_mapping = json.load(f)


# %%
overlaps = {}
for community in communities_reddit:
    overlaps[community] = {}
    for category in categories_mapping:
        overlaps[community][category] = lf.overlap(
            communities_reddit[community], categories_mapping[category]
        )


# %%
overlaps_ranked = {}
for overlap in overlaps:
    overlaps_ranked[overlap] = sorted(
        overlaps[overlap].items(),
        key=lambda x: x[1]["overlap_proportion"],
        reverse=True,
    )


# %%
for overlap in overlaps_ranked:
    print(
        f"Community {overlap}: \n\nNumber of elements in community: {len(communities_reddit[overlap])}."
    )
    print(f"Example members: {', '.join(communities_reddit[overlap][0:10])}.\n")
    print("Categories with largest overlap:")
    for category, overlap_data in overlaps_ranked[overlap][0:5]:
        print(
            f"Category '{category}' ({len(categories_mapping[category])} members):         \n\t{overlap_data['overlap_proportion']*100:.1f}% overlap,        \n\t{overlap_data['proportion_in_category']*100:.1f}% of this community contained in this category,        \n\t{overlap_data['proportion_in_community']*100:.2f}% of the category contained in this community"
        )

# %% [markdown]
#  .... diccussion....
# 
# 
#  The categories above are the raw categories extracted from wikipedia: there is 1800+ of them in our dataset, and they are very granular. Let's also try to do the same operation, but resolving categories to two "root categories":
# 
#  - https://en.wikipedia.org/wiki/Category:Psychoactive_drugs_by_mechanism_of_action
#  - https://en.wikipedia.org/wiki/Category:Drugs_by_psychological_effects
# 
#  To do so, we semi-manually mapped all categories that are sub categories of one of those two categories to the corresponding top-level category: this way, for example, "Masticatories" is mapped to "Herbal and Fungal Stimulants" which is mapped to "Stimulants".

# %%
with open(Config.Path.wiki_mechanism_categories, "r") as f:
    mechanism_categories = json.load(f)

wiki_data = lf.load_data_wiki()


# %%
lf.assign_root_categories(
    reddit_graph,
    wiki_data=wiki_data,
    mapping=mechanism_categories,
    name="wiki_category_mechanisms",
)


# %%
overlaps = {}
for community in communities_reddit:
    overlaps[community] = {}
    for category in mechanism_categories:
        overlaps[community][category] = lf.overlap(
            communities_reddit[community], categories_mapping[category]
        )


# %%
lf.assign_lemmas(graph_reddit)


# %%
lf.assign_lemmas(graph_wiki)


# %%
graph_wiki.nodes(data=True)


# %%
lf.assign_tfs(graph_reddit)
lf.assign_tfs(graph_wiki)


# %%
lf.assign_idfs(graph_reddit)
lf.assign_idfs(graph_wiki)


# %%
lf.assign_tf_idfs(graph_reddit)
lf.assign_tf_idfs(graph_wiki)


# %%

# nx.readwrite.gpickle.write_gpickle(graph_reddit, Config.Path.reddit_with_text)
graph_reddit = nx.readwrite.gpickle.read_gpickle(Config.Path.reddit_with_text)


# %%



# %%
for node in tqdm(graph_reddit.nodes):
    wc = lf.wordcloud_from_node(graph_reddit, node)
    wc.to_file(Config.Path.shared_data_folder / "wordclouds" / "reddit" / f"{node.replace('/','_')}.png")


# %%
for node in tqdm(graph_wiki.nodes):
    wc = lf.wordcloud_from_node(graph_wiki, node)
    wc.to_file(Config.Path.shared_data_folder / "wordclouds" / "wiki" / f"{node.replace('/','_')}.png")


# %%



# %%



# %%



# %%



# %%



# %%



