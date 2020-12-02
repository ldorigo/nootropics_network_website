#%%

from typing import Dict, List, Optional, Tuple, Union
import community
import networkx as nx
from infomap import Infomap
import numpy as np
import plotly.graph_objects as go
import spacy
from tqdm.auto import tqdm
import wojciech as w
from wordcloud import WordCloud, STOPWORDS
import matplotlib

nlp = spacy.load("en_core_web_sm")


#%%
def assign_lemmas(graph: nx.Graph):
    assert (
        "contents" in list(graph.nodes(data=True))[0][1]
    ), "The graph does not contain node contents."
    for node, data in tqdm(graph.nodes(data=True)):
        doc = nlp.make_doc(" ".join(data["contents"]))
        lemmas = [i.lemma_.lower() for i in doc if not i.is_punct]
        graph.nodes[node]["lemmas"] = lemmas
        # graph.nodes[node]["doc"] = doc


# %%
def assign_tfs(graph: nx.Graph, type: str = "frequency"):
    for node, data in tqdm(graph.nodes(data=True)):
        graph.nodes[node]["tfs"] = w.nlp.term_frequency(
            terms=None, document=data["lemmas"], type="frequency"
        )


def assign_idfs(graph: nx.Graph, type: str = "regular"):

    all_lemmas = [data["lemmas"] for node_, data in graph.nodes(data=True)]

    for node, data in tqdm(graph.nodes(data=True)):
        # other_lemmas_list = []
        # for lemmas_list in other_lemmas:
        #     other_lemmas_list += lemmas_list
        graph.nodes[node]["idfs"] = w.nlp.inverse_document_frequency(
            terms=None, documents=all_lemmas, term_document=data["lemmas"], type=type
        )


def assign_tf_idfs(graph: nx.Graph):
    assert (
        "tfs" in list(graph.nodes(data=True))[0][1]
        and "idfs" in list(graph.nodes(data=True))[0][1]
    ), "The graph does not contain tfs and idfs, please call those functions first."

    for node, data in tqdm(graph.nodes(data=True)):
        tfidfs = {}
        for lemma in data["lemmas"]:
            tfidfs[lemma] = data["tfs"][lemma] * data["idfs"][lemma]
        graph.nodes[node]["tf-idfs"] = tfidfs


def wordcloud_from_node(graph: nx.Graph, node: str):
    wc = WordCloud(
        background_color="white", width=1800, height=1000, collocations=False
    ).generate_from_frequencies(graph.nodes[node]["tf-idfs"])
    return wc


def wordcloud_from_nodes(graph: nx.Graph, nodes: List[str]):
    """Generate a wordcloud from a community (set of nodes).
    Because the amount of combinations is enormous, this is generated on the fly and thus much slower than for single nodes.

    Args:
        graph (nx.Graph): Graph containing the nodes and the lemmas associated with each node.
        nodes (List[str]): List of node labels for which to compute the wordcloud

    Returns:
        [type]: matplotlib image with the resulting wordcloud
    """
    nodes_lemmas = []
    for node in tqdm(nodes):
        nodes_lemmas += graph.nodes[node]["lemmas"]

    other_nodes_lemmas = []
    for node, data in tqdm(graph.nodes(data=True)):
        if node not in nodes:
            other_nodes_lemmas += data["lemmas"]

    tfs = w.nlp.term_frequency(terms=None, document=nodes_lemmas, type="frequency")
    idfs = w.nlp.inverse_document_frequency(
        terms=None,
        documents=other_nodes_lemmas,
        term_document=nodes_lemmas,
        type="regular",
    )

    tf_idfs = {lemma: tfs[lemma] * idfs[lemma] for lemma in tqdm(nodes_lemmas)}

    wc = WordCloud(
        background_color="white", width=1800, height=1000, collocations=False
    ).generate_from_frequencies(tf_idfs)

    return wc


def rank_dict(dict_: Dict[str, float], verbose=False, reverse=False):
    res = sorted(dict_.items(), key=lambda x: x[1], reverse=reverse)
    if verbose:
        print("Top 5 elements:")
        for name, val in res[:5]:
            print(f"{val:.3f} \t- {name}")
    return res