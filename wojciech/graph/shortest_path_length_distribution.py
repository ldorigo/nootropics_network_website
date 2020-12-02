import networkx as nx
import numpy as np


def shortest_path_length_distribution(G: nx.Graph,
                                      as_probability_distribution=False):

    all_shortest_path_lengths_dict = dict(nx.shortest_path_length(G))
    number_of_nodes = G.number_of_nodes()

    # Preallocate
    shortest_path_lengths = np.zeros(number_of_nodes * (number_of_nodes - 1),
                                     dtype=int)
    index = 0
    for target_node, shortest_path_from_source_dict \
            in all_shortest_path_lengths_dict.items():
        for source_node, shortest_path_length \
                in shortest_path_from_source_dict.items():
            if target_node != source_node:
                shortest_path_lengths[index] = shortest_path_length
                index += 1

    bins = range(0, np.max(shortest_path_lengths) + 1)
    path_length = bins[:-1]
    distribution, _ = np.histogram(shortest_path_lengths, bins=bins)

    if as_probability_distribution:
        distribution = distribution / np.sum(distribution)

    return path_length, distribution
