from os import name
from typing import Collection, Dict, List

import networkx as nx
import numpy as np
import wojciech as w
import plotly.figure_factory as ff
import pickle

try:
    import library_functions as lf
except ModuleNotFoundError:
    import project.library_functions as lf
try:
    from library_functions.config import Config
except ModuleNotFoundError:
    from project.library_functions.config import Config


def inverse_communities_from_partition(
    partition: Dict[str, int]
) -> Dict[int, List[str]]:
    """Given a partition mapping from nodes to their community, return a mapping from communities to the nodes in that community.

    Args:
        partition (Dict[str, int]): [description]

    Returns:
        Dict[int, List[str]]: [description]
    """
    communities = {i: [] for i in range(max(partition.values()) + 1)}

    for node in partition:
        communities[partition[node]].append(node)
    return communities


def inverse_categories(categories: Dict):
    inverse = {}
    for cat in categories:
        for c in categories[cat]:
            inverse[c] = cat
    return inverse


def overlap(
    community_names: Collection[str], category_names: Collection[str]
) -> Dict[str, float]:
    """Given a collection of nodes belonging to a community and a collection of
    nodes in a category, compute several metrics about the overlap of those two collections.

    Args:
        community_names (Collection[str]): Collection of nodes that belong to a given community (f.ex., from the louvain algorithm)
        category_names (Collection[str]): Collection of nodes in a category (on wikipedia)

    Returns:
        Dict[str, float]: Dict containing 3 metrics: "proportion_in_community","proportion_in_category", "overlap_proportion".
    """
    nodeset = set(community_names)
    nameset = set(category_names)

    all = nodeset.union(nameset)
    intersection = nodeset.intersection(nameset)

    # Proportion of the community that is part of this category
    proportion_of_nodes_in_category = len(intersection) / len(nodeset)
    # Proportion of the the category that is represented in the community
    proportion_category_in_nodes = len(intersection) / len(nameset)

    # Overall overlap metric: proportion of nodes that are in both sets
    # divided by total amount of different names
    overall_overlap = len(intersection) / len(all)
    return {
        "proportion_in_community": proportion_category_in_nodes,
        "proportion_in_category": proportion_of_nodes_in_category,
        "overlap_proportion": overall_overlap,
    }


def overlap_matrix(
    attribute_A: str, attribute_B: str, graph: nx.Graph, savename: str = None
):
    """Given two attributes that are used to hold the category of nodes within a graph,
    return a matrix that contains the overlaps of each category represented by attribute_A
    and each category represented by attribute_B

    Args:
        attribute_A (str): name of the node attribute containing the first category
        attribute_B (str):  name of the node attribute containing the second category
        graph (nx.Graph): 2D numpy array containing the overlaps

    Returns:
        [type]: np.Array
    """
    try:
        all_A_attributes = list(
            set([data for _, data in graph.nodes(data=attribute_A)])
        )
        all_B_attributes = list(
            set([data for _, data in graph.nodes(data=attribute_B)])
        )
    except TypeError:
        # The above fails if the attributes contain lists
        temp = [data for _, data in graph.nodes(data=attribute_A)]
        all_A_attributes = sorted(list(set(lf.flatten(temp))))
        temp = [data for _, data in graph.nodes(data=attribute_B)]
        all_B_attributes = sorted(list(set(lf.flatten(temp))))

    result = np.zeros((len(all_A_attributes), len(all_B_attributes)))

    for i, a in enumerate(all_A_attributes):
        nodes_a = w.graph.get_nodes_by_conditions(
            graph, lambda x: x[attribute_A] == a or a in x[attribute_A]
        )
        for j, b in enumerate(all_B_attributes):
            nodes_b = w.graph.get_nodes_by_conditions(
                graph, lambda x: x[attribute_B] == b or b in x[attribute_B]
            )
            groups_overlap = overlap(nodes_a, nodes_b)["overlap_proportion"]
            result[i, j] = groups_overlap

    if savename:
        np.save(Config.Path.shared_data_folder / savename, result)
    return result, all_A_attributes, all_B_attributes


def draw_overlaps_plotly(
    attribute_A: str,
    attribute_B: str,
    graph: nx.Graph,
    save: str = None,
    saved: str = None,
):
    """Get a 2D-histogram showing how much the categories of two categorization systems of the nodes in a graph overlap each other.

    Args:
        attribute_A (str): name of the node attribute containing the first category
        attribute_B (str): name of the node attribute containing the second category
        graph (nx.Graph): networkx graph whose nodes have the two attributes above
        saved (str, optional): Name file containing a pre-computed figure. Defaults to None.
        save (str, optional): Name file to which to save the figure. Defaults to None.

    Returns:
        [type]: plotly figure containing the 2D histogram
    """
    if saved:
        with open(Config.Path.shared_data_folder / saved, "rb") as f:
            return pickle.load(f)

    overlaps, A, B = overlap_matrix(
        attribute_A=attribute_A, attribute_B=attribute_B, graph=graph
    )
    heatmap_text = np.around(overlaps, decimals=2)
    fig = ff.create_annotated_heatmap(
        z=overlaps,
        text=overlaps,
        x=[b.title() for b in B],
        y=[f"Com. {i+1}" for i in range(len(A))],
        annotation_text=heatmap_text,
        colorscale="Greys",
        hoverinfo="z",
    )
    for i in range(len(fig.layout.annotations)):
        fig.layout.annotations[i].font.size = 8

    if save:
        with open(Config.Path.shared_data_folder / save, "wb+") as f:
            pickle.dump(fig, f)

    return fig
