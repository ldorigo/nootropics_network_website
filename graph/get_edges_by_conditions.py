import networkx as nx
import numpy as np


def get_edges_by_conditions(G: nx.Graph, conditional_functions):
    '''
    :param G: networkx Graph
    :param conditional_functions: conditional function or a list derof

    :return: list of edge labels (tuples containing labels of nodes that
             edge connects) satisfying the conditions

    :Example:

    >>> conditional_functions = [lambda x: x['polarity'] > 0,
    >>>                          lambda x: x['subjectivity'] > 0.5]
    >>> nodes = get_edges_by_conditions(G, conditional_functions)
    '''

    if not isinstance(conditional_functions, list):
        conditional_functions = [conditional_functions]

    return [edge_label for edge_label
            in list(G.edges)
            if check_edge(G.edges[edge_label], conditional_functions)]


def check_edge(edge, conditional_functions):
    for conditional_function in conditional_functions:
        if not conditional_function(edge):
            return False
    return True
