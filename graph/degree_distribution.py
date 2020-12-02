import numpy as np
import networkx as nx
import wojciech as w


def degree_distribution(G: nx.Graph,
                        direction: str = None,
                        as_probability_distribution=False,
                        cumulative=False):

    node_degrees = w.graph.degrees(G, direction=direction)

    bin_edges = np.arange(np.max(node_degrees) + 1)
    degrees = bin_edges[:-1]
    distribution, _ = np.histogram(node_degrees, bins=bin_edges)

    if as_probability_distribution:
        distribution = distribution / G.number_of_nodes()

    if cumulative:
        distribution = np.cumsum(distribution)

    return degrees, distribution