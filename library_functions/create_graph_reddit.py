from typing import List, Any, Union
from pathlib import Path

from tqdm.auto import tqdm

try:
    import library_functions as lf
except ModuleNotFoundError:
    import project.library_functions as lf

import networkx as nx
import numpy as np
import wojciech as w


def create_graph_reddit(
    max_drugs_in_post: Union[int, np.int] = np.inf,
    min_edge_occurrences_to_link: Union[int, np.int] = 1,
    min_content_length_in_characters: Union[int, np.int] = 0,
    conditional_functions_dict: Union[dict, Path] = None,
    include_node_contents: bool = False,
    include_link_contents: bool = False,
    alternative_path: Union[str, Path] = None,
    show_progress_bars: bool = False,
):
    """
    Args:
        max_drugs_in_post (int): a limit of the number of drugs in a post.
                                 Posts containing more drugs will be
                                 disregarded.

        min_edge_occurrences_to_link (int): a limit describing the minimum
                                            number times a link needs to appear
                                            in order to be considered valid.
                                            The links that occur less times will
                                            be disregarded.

        min_content_length_in_characters (int): a limit describing the minimum
                                                length of the content of the
                                                Reddit post. Posts with shorter
                                                content will be disregarded.

        conditional_functions_dict (dict): a dictionary keyed by attribute names
                                           whose values are functions that
                                           represent conditions for those
                                           attributes, e.g.
                                           {'polarity': lambda x: x > 0.1}

        include_node_contents (bool): A boolean determining whether to assign
                                      the content of the posts containing a
                                      drug as a node attribute.

        include_link_contents (bool): A boolean determining whether to assign
                                      the content of the posts containing the
                                      linked drugs as an edge attribute.

        show_progress_bars (): A boolean deciding whether to show progress bars.

    Returns:

    Examples:
        >>> g_reddit = create_graph_reddit(
        >>>        max_drugs_in_post=10,
        >>>        min_edge_occurrences_to_link=3,
        >>>        min_content_length_in_characters=25,
        >>>        conditional_functions_dict={'polarity': lambda x: x > 0.1},
        >>>        alternative_path=None,
        >>>        include_node_contents=False,
        >>>        include_link_contents=False
        >>> )
    """

    # Make sure that conditional_functions_dict is a dict
    if conditional_functions_dict is None:
        conditional_functions_dict = dict()

    # Load the clean Reddit and Wiki data
    drug_database_reddit = lf.load_data_reddit(alternative_path)
    wiki_data = lf.load_data_wiki()
    substance_names = lf.load_substance_names()

    # Initialize graphs
    g_reddit = nx.Graph()
    g_reddit.add_nodes_from(substance_names)

    # Assign node properties. Note thad we use drug names as nodes, and that
    # the drug names are taken from Wikipedia
    for index_drug, drug in enumerate(wiki_data["name"]):
        if drug in g_reddit.nodes:
            g_reddit.nodes[drug]["count"] = 0
            g_reddit.nodes[drug]["polarity"] = []
            g_reddit.nodes[drug]["subjectivity"] = []
            g_reddit.nodes[drug]["contents"] = []
            g_reddit.nodes[drug]["ids"] = []
            g_reddit.nodes[drug]["categories"] = wiki_data["categories"][index_drug]

    # Link drugs that appear in the same post
    for post_id, reddit_post in tqdm(
        list(drug_database_reddit.items()), disable=not show_progress_bars
    ):

        # Disregard the post if the length of its content does not
        # surpass the threshold
        if len(reddit_post["content"]) < min_content_length_in_characters:
            continue

        # Link the drugs and assign link attributes
        link_drugs(
            G=g_reddit,
            list_of_drugs=reddit_post["matches"],
            polarity=reddit_post["polarity"],
            subjectivity=reddit_post["subjectivity"],
            text=reddit_post["title"] + " " + reddit_post["content"],
            max_drugs_in_post=max_drugs_in_post,
            conditional_functions_dict=conditional_functions_dict,
            include_link_contents=include_link_contents,
            include_node_contents=include_node_contents,
            post_id=post_id,
        )

    # Remove the edges that occur fewer times than the threshold
    if min_edge_occurrences_to_link > 1:

        def occurring_to_seldom(edge_attributes):
            return edge_attributes["count"] < min_edge_occurrences_to_link

        edges_to_remove = w.graph.get_edges_by_conditions(g_reddit, occurring_to_seldom)

        g_reddit.remove_edges_from(edges_to_remove)

    # Weight the parameters
    attributes_to_weight = ["polarity", "subjectivity"]

    for edge in tqdm(g_reddit.edges, disable=not show_progress_bars):
        for attribute in attributes_to_weight:
            g_reddit.edges[edge][attribute + "_weighted"] = weigh_attribute(
                attribute, g_reddit.edges[edge]
            )

    return g_reddit


def link_drugs(
    G: nx.Graph,
    list_of_drugs: List[str],
    polarity: float,
    subjectivity: float,
    post_id: str,
    text: str,
    max_drugs_in_post: int,
    conditional_functions_dict,
    include_node_contents: bool = False,
    include_link_contents: bool = False,
):

    # Discard posts where the number of mentioned substances exceeds the limit
    if (len(list_of_drugs) < 1) or (len(list_of_drugs) > max_drugs_in_post):
        return

    # Discard posts that do NOT meet the polarity criteria
    if "polarity" in conditional_functions_dict.keys():
        condition = conditional_functions_dict["polarity"]
        if not condition(polarity):
            return
    # Discard posts that do NOT meet the subjectivity criteria
    if "subjectivity" in conditional_functions_dict.keys():
        condition = conditional_functions_dict["subjectivity"]
        if not condition(subjectivity):
            return

    # Assign the node attributes.
    for drug in list_of_drugs:
        if drug in G.nodes:
            G.nodes[drug]["count"] += 1
            G.nodes[drug]["polarity"].append(polarity)
            G.nodes[drug]["subjectivity"].append(subjectivity)
            G.nodes[drug]["ids"].append(post_id)
            if include_node_contents:
                G.nodes[drug]["contents"].append(text)

    # Stop here if there is only one drug
    if len(list_of_drugs) == 1:
        return

    # Assign the edge attributes.
    for index in range(len(list_of_drugs)):
        drug = list_of_drugs[index]
        other_drugs = list_of_drugs[(index + 1) :]

        for other_drug in other_drugs:
            if (drug in G.nodes) & (other_drug in G.nodes):
                edge = (drug, other_drug)

                # If edge already exists, append the properties to their
                # respective list
                if G.has_edge(*edge):
                    G.edges[edge]["count"] += 1
                    G.edges[edge]["number_of_drugs_in_post"].append(len(list_of_drugs))
                    G.edges[edge]["polarity"].append(polarity)
                    G.edges[edge]["subjectivity"].append(subjectivity)
                    if include_link_contents:
                        G.edges[edge]["contents"].append(text)

                # If the edge does not exist, initialize all the attributes
                else:
                    G.add_edge(
                        *edge,
                        count=1,
                        number_of_drugs_in_post=[len(list_of_drugs)],
                        polarity=[polarity],
                        subjectivity=[subjectivity],
                        contents=[text] if include_link_contents else None
                    )


def weigh_attribute(attribute_to_weigh, all_edge_attributes):
    value_attribute = np.array(all_edge_attributes[attribute_to_weigh])
    number_of_drugs_in_post = np.array(all_edge_attributes["number_of_drugs_in_post"])
    weights = 1 / (number_of_drugs_in_post - 1)

    number_of_posts_containing_link = all_edge_attributes["count"]
    value_weighted = np.sum(weights * value_attribute) / np.sum(weights)

    return value_weighted
