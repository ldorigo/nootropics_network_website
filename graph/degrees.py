import networkx as nx
import numpy as np


def degrees(G: nx.Graph,
            node_labels=None,
            direction: str = None):
    if direction is None:
        node_degrees = G.degree(node_labels)
    elif direction == 'in':
        node_degrees = G.in_degree(node_labels)
    elif direction == 'out':
        node_degrees = G.out_degree(node_labels)
    else:
        raise Exception('Invalid direction: "' + direction + '"')

    return np.fromiter(dict(node_degrees).values(), dtype=int)
