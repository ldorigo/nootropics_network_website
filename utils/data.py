from project.library_functions import (
    assign_root_categories,
    create_graph_reddit,
    create_graph_wiki,
    get_fa2_layout,
    get_root_category_mapping,
    get_wiki_data,
    assign_louvain_communities,
    get_wiki_page_names,
    get_wiki_synonyms_mapping,
    load_data_reddit,
)
from project.library_functions.config import Config
import networkx as nx
import wojciech as w

reddit_data = load_data_reddit()

print("Loading graphs...")
graph_reddit = create_graph_reddit(
    max_drugs_in_post=8,
    min_content_length_in_characters=30,
    min_edge_occurrences_to_link=2,
    include_node_contents=True,
)

graph_wiki_directed = create_graph_wiki()
graph_wiki = nx.readwrite.gpickle.read_gpickle(Config.Path.wiki_gcc)
graph_reddit_gcc = w.graph.largest_connected_component(graph_reddit)


## layouts
print("Loading/computing layouts...")

layout_reddit = get_fa2_layout(
    graph_reddit_gcc,
    edge_weight_attribute="count",
    saved="reddit_filtered_weighted_gcc.json",
)
layout_wiki = get_fa2_layout(graph_wiki, saved="wiki_simple_noargs_gcc.json")


## Assign "root categories" on wikipedia
print("Assigning root categories...")
assign_root_categories(
    graph_wiki,
    wiki_data=get_wiki_data(),
    mapping=get_root_category_mapping(which="effects"),
    name="effect_category",
)

assign_root_categories(
    graph_wiki,
    wiki_data=get_wiki_data(),
    mapping=get_root_category_mapping(which="mechanisms"),
    name="mechanism_category",
)
assign_root_categories(
    graph_reddit_gcc,
    wiki_data=get_wiki_data(),
    mapping=get_root_category_mapping(which="effects"),
    name="effect_category",
)
assign_root_categories(
    graph_reddit_gcc,
    wiki_data=get_wiki_data(),
    mapping=get_root_category_mapping(which="mechanisms"),
    name="mechanism_category",
)

## Assign louvain communities on both networks at default resolution
print("Assigning Louvain categories")
_, reddit_dendrogram, _, wiki_dendrogram = assign_louvain_communities(
    graph_reddit_gcc, graph_wiki, reddit_edge_weight="count", others_threshold=8
)

_, reddit_dendrogram_finegrained = assign_louvain_communities(
    graph_reddit_gcc,
    reddit_edge_weight="count",
    others_threshold=4,
    louvain_resolution_reddit=0.6,
)

all_names_and_synonyms = get_wiki_page_names(with_synonyms=True)
synonym_mapping = get_wiki_synonyms_mapping()

names_and_synonyms_in_reddit = {
    i for i in all_names_and_synonyms if synonym_mapping[i] in graph_reddit_gcc.nodes()
}
