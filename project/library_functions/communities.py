#%%

from typing import Dict, List, Optional, Tuple, Union

import community
import networkx as nx
from infomap import Infomap
import numpy as np
import plotly.graph_objects as go
from collections import Counter

# %%


def assign_louvain_communities(
    reddit_graph: nx.Graph,
    wiki_graph: nx.Graph = None,
    reddit_edge_weight: str = "count",
    others_threshold: int = 2,
) -> Union[nx.Graph, Tuple[nx.Graph, nx.Graph]]:
    """ "Calculate communities using the louvain algorithm and assign them as property to the graphs node.
    if two graphs are given, also assign one graph's communities to the other's.


    Args:
        reddit_graph (nx.Graph): Reddit Graph
        wiki_graph (nx.Graph, optional): Wikipedia graph. Defaults to None.
        reddit_edge_weight (str, optional): edge attribute to use for weighting. Defaults to "count".
        others_threshold (int, optional): minimum size of the communities. Communities smaller than this are mapped to "other". Defaults to 2.

    Returns:
        Union[nx.Graph, Tuple[nx.Graph, nx.Graph]]: [description]
    """
    reddit_dendrogram = community.generate_dendrogram(
        reddit_graph, weight=reddit_edge_weight
    )
    if wiki_graph:
        wiki_dendrogram = community.generate_dendrogram(wiki_graph)

    # Iterate over reddit nodes to assign communities
    for node in reddit_graph:
        # Iterate over all levels of the dendrogram
        for level in range(len(reddit_dendrogram) - 1):
            actual_level = len(wiki_dendrogram) - 2 - level

            partition = community.partition_at_level(reddit_dendrogram, level)

            node_community = partition[node]
            counts = Counter(partition.values())
            if counts[node_community] < others_threshold:
                node_community = "other"
            reddit_graph.nodes[node][
                f"louvain_community_reddit_L{actual_level}"
            ] = f"L{actual_level}-{node_community}"
        if wiki_graph:
            # Also add the community from the other graph to allow comparing
            # Again, iterate over all levels in the dendrogram
            for level in range(len(wiki_dendrogram) - 1):
                actual_level = len(wiki_dendrogram) - 2 - level

                partition = community.partition_at_level(wiki_dendrogram, level)

                try:
                    node_community = partition[node]
                    counts = Counter(partition.values())
                    if counts[node_community] < others_threshold:
                        node_community = "other"

                    reddit_graph.nodes[node][
                        f"louvain_community_wiki_L{actual_level}"
                    ] = f"L{actual_level}-{node_community}"

                except:
                    reddit_graph.nodes[node][
                        f"louvain_community_wiki_L{level}"
                    ] = f"L{level}-NONE"
    if wiki_graph:
        for node in wiki_graph:
            for level in range(
                len(wiki_dendrogram) - 1,
            ):
                actual_level = len(wiki_dendrogram) - 2 - level

                partition = community.partition_at_level(wiki_dendrogram, level)
                node_community = partition[node]

                counts = Counter(partition.values())
                if counts[node_community] < others_threshold:
                    node_community = "other"

                wiki_graph.nodes[node][
                    f"louvain_community_wiki_L{actual_level}"
                ] = f"L{actual_level}-{node_community}"
            # Also add the community from the other graph to allow comparing

            for level in range(len(reddit_dendrogram) - 1):
                actual_level = len(wiki_dendrogram) - 2 - level

                partition = community.partition_at_level(reddit_dendrogram, level)

                try:
                    node_community = partition[node]

                    counts = Counter(partition.values())
                    if counts[node_community] < others_threshold:
                        node_community = "other"
                    wiki_graph.nodes[node][
                        f"louvain_community_reddit_L{actual_level}"
                    ] = f"L{actual_level}-{node_community}"
                except:
                    wiki_graph.nodes[node][
                        f"louvain_community_reddit_L{level}"
                    ] = f"L{level}-NONE"

    return (
        (reddit_graph, reddit_dendrogram, wiki_graph, wiki_dendrogram)
        if wiki_graph
        else (reddit_graph, reddit_dendrogram)
    )


def get_infomap_communities(graph: nx.Graph, reddit_edge_weight=None):
    im = Infomap("--flow-model undirected -N 10 --prefer-modular-solution")

    ## im only works with numerical ids, so we need to save a mapping

    ids_to_names = {}
    names_to_ids = {}

    for index, node in enumerate(graph.nodes):
        ids_to_names[index] = node
        names_to_ids[node] = index
        im.add_node(index, name=node)

    # iterate over edges and add them to the im tree, optionally adding the weight
    for e1, e2, data in graph.edges(data=True):
        e1_id = names_to_ids[e1]
        e2_id = names_to_ids[e2]
        weight = data[reddit_edge_weight] if reddit_edge_weight else None
        link = (e1_id, e2_id, weight) if weight else (e1_id, e2_id)
        im.add_link(*link)

    im.run()
    for node in im.tree:
        if node.is_leaf:
            graph.nodes[ids_to_names[node.node_id]][
                "infomap_community"
            ] = node.module_id

    return graph


def assign_root_categories(
    graph: nx.Graph,
    wiki_data: Dict[str, List],
    mapping: Dict[str, List[str]],
    name: str,
):
    """Given a graph and wikipedia data, assign a new attribute to the nodes that represent the root category of that node on wikipedia.


    Args:
        graph (nx.Graph): nootropics graph
        wiki_data (Dict[str, List]): wikipedia data as obtained by lf.load_wiki_data
        mapping (Dict[str, List[str]]): Dict of the form {"root_category":["list","of","sub","categories"]}
        name (str): name of the new node attribute to which to assign the mapping.
    """
    inverse_mapping = {}
    for category, subcategories in mapping.items():
        for subcategory in subcategories:
            inverse_mapping[subcategory.lower()] = category.lower()

    names_to_categories = dict(zip(wiki_data["name"], wiki_data["categories"]))
    for node in graph.nodes:
        graph.nodes[node][name] = []

        for category in names_to_categories[node]:
            if category in inverse_mapping:
                graph.nodes[node][name].append(inverse_mapping[category])


# def partition_from_nodes(graph: nx.)
# # %%
# def plot_partition_sizes(partition: Dict[str, int]):
#     partitions_amount = len(set(partition.values()))
#     partition_values = list(partition.values())
#     unique, frequency = np.unique(partition_values, return_counts=True)
