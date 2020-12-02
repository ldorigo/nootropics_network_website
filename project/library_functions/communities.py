#%%

from typing import Dict, List, Optional, Tuple, Union
import community
import networkx as nx
from infomap import Infomap

# %%


def assign_louvain_communities(
    reddit_graph, wiki_graph=None, reddit_edge_weight="count"
) -> Union[nx.Graph, Tuple[nx.Graph, nx.Graph]]:
    """Calculate communities using the louvain algorithm and assign them as property to the graphs node.
    if two graphs are given, also assign one graph's communities to the other's.

    Args:
        reddit_graph ([type]): [description]
        wiki_graph ([type], optional): [description]. Defaults to None.

    Returns:
        Union[nx.Graph, Tuple[nx.Graph, nx.Graph]]: [description]
    """
    reddit_dendrogram = community.generate_dendrogram(
        reddit_graph, weight=reddit_edge_weight
    )
    if wiki_graph:
        wiki_dendrogram = community.generate_dendrogram(wiki_graph)
    for node in reddit_graph:
        reddit_graph.nodes[node][f"louvain_community_reddit"] = {}
        for level in range(len(reddit_dendrogram) - 1):
            partition = community.partition_at_level(reddit_dendrogram, level)
            reddit_graph.nodes[node][f"louvain_community_reddit"][level] = partition[
                node
            ]
        if wiki_graph:
            # Also add the community from the other graph to allow comparing
            reddit_graph.nodes[node][f"louvain_community_wiki"] = {}
            try:
                for level in range(len(wiki_dendrogram) - 1):
                    partition = community.partition_at_level(wiki_dendrogram, level)
                    reddit_graph.nodes[node][f"louvain_community_wiki"][
                        level
                    ] = partition[node]
            except:
                reddit_graph.nodes[node]["louvain_community_wiki"] = -1
    if wiki_graph:  # %%
        for node in wiki_graph:
            wiki_graph.nodes[node][f"louvain_community_wiki"] = {}
            for level in range(len(wiki_dendrogram) - 1):
                partition = community.partition_at_level(wiki_dendrogram, level)
                wiki_graph.nodes[node][f"louvain_community_wiki"][level] = partition[
                    node
                ]
            # Also add the community from the other graph to allow comparing

            wiki_graph.nodes[node][f"louvain_community_reddit"] = {}
            try:
                for level in range(len(reddit_dendrogram) - 1):
                    partition = community.partition_at_level(reddit_dendrogram, level)
                    wiki_graph.nodes[node][f"louvain_community_reddit"][
                        level
                    ] = partition[node]
            except:
                wiki_graph.nodes[node]["louvain_community_reddit"] = -1

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
        mapping (Dict[str, List[str]]): Dict of the form "root_category":["list","of","sub","categories"]
        name (str): name of the new node attribute to which to assign the mapping.
    """
    inverse_mapping = {}
    for category, subcategories in mapping.items():
        for subcategory in subcategories:
            inverse_mapping[subcategory] = category

    names_to_categories = dict(zip(wiki_data["name"], wiki_data["categories"]))
    for node in graph.nodes:
        graph.nodes[node][name] = []

        for category in names_to_categories[node]:
            if category in inverse_mapping:
                graph.nodes[node][name].append(inverse_mapping[category])


# %%
