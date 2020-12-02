import networkx as nx
import numpy as np


def betweenness(G: nx.Graph):
    betweenness = nx.betweenness_centrality(G)
    return np.fromiter(dict(betweenness).values(), dtype=float)
