from typing import List

from tqdm.auto import tqdm

try:
    import library_functions as lf
except ModuleNotFoundError:
    import project.library_functions as lf
import networkx as nx
import numpy as np
import wojciech as w


def create_graph_reddit(
    max_drugs_in_post=np.inf,
    min_edge_occurrences_to_link=1,
    min_content_length_in_characters=0,
    conditional_functions_dict=None,
    alternative_path=None,
    include_node_contents=False,
    include_link_contents=False,
):

    if conditional_functions_dict is None:
        conditional_functions_dict = dict()

    # Load the clean Reddit and Wiki data
    drug_database_reddit = lf.load_data_reddit(alternative_path)
    wiki_data = lf.load_data_wiki()
    substance_names = lf.load_substance_names()

    # Initialize graphs
    g_reddit = nx.Graph()
    g_reddit.add_nodes_from(substance_names)

    # Initialize mention counts and assign categories from Wikipedia
    # to nodes (drugs)
    for index_drug, drug in enumerate(wiki_data["name"]):
        if drug in g_reddit.nodes:
            g_reddit.nodes[drug]["count"] = 0
            g_reddit.nodes[drug]["polarity"] = []
            g_reddit.nodes[drug]["subjectivity"] = []
            g_reddit.nodes[drug]["contents"] = []
            g_reddit.nodes[drug]["categories"] = wiki_data["categories"][index_drug]

    # Link drugs
    for reddit_post in tqdm(list(drug_database_reddit.values())):
        if len(reddit_post["content"]) < min_content_length_in_characters:
            continue

        link_drugs(
            g_reddit,
            reddit_post["matches"],
            reddit_post["polarity"],
            reddit_post["subjectivity"],
            reddit_post["title"] + " " + reddit_post["content"],
            max_drugs_in_post,
            conditional_functions_dict,
            include_link_contents=include_link_contents,
            include_node_contents=include_node_contents,
        )

    # Remove the edges that occur fewer times than the threshold
    if min_edge_occurrences_to_link > 1:

        def occurring_to_seldom(edge_attributes):
            return edge_attributes["count"] < min_edge_occurrences_to_link

        edges_to_remove = w.graph.get_edges_by_conditions(g_reddit, occurring_to_seldom)

        g_reddit.remove_edges_from(edges_to_remove)

    # Weight the parameters
    attributes_to_weight = ["polarity", "subjectivity"]

    for edge in tqdm(g_reddit.edges):
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
    text: str,
    max_drugs_in_post: int,
    conditional_functions_dict,
    include_node_contents: bool = False,
    include_link_contents: bool = False,
):

    # Discard posts where the number of mentioned substances exceeds the limit
    if (len(list_of_drugs) <= 1) or (len(list_of_drugs) > max_drugs_in_post):
        return

    if "polarity" in conditional_functions_dict.keys():
        condition = conditional_functions_dict["polarity"]
        if not condition(polarity):
            return

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
            if include_node_contents:
                G.nodes[drug]["contents"].append(text)

    # Assign the edge attributes.
    for index in range(len(list_of_drugs)):
        drug = list_of_drugs[index]
        other_drugs = list_of_drugs[(index + 1) :]

        for other_drug in other_drugs:
            if (drug in G.nodes) & (other_drug in G.nodes):
                edge = (drug, other_drug)
                if G.has_edge(*edge):
                    G.edges[edge]["count"] += 1
                    G.edges[edge]["number_of_drugs_in_post"].append(len(list_of_drugs))
                    G.edges[edge]["polarity"].append(polarity)
                    G.edges[edge]["subjectivity"].append(subjectivity)
                    if include_link_contents:
                        G.edges[edge]["contents"].append(text)
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
