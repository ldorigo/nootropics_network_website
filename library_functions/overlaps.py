from os import name
from typing import Collection, Dict
import networkx as nx
from typing import Collection, Dict, List


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