import networkx as nx
import numpy as np
import wojciech as w


def eigenvector_centrality(G: nx.Graph):
    eigenvector_centrality = nx.eigenvector_centrality(G)
    return np.fromiter(dict(eigenvector_centrality).values(), dtype=float)
