import networkx as nx
import numpy as np


def get_nodes_by_conditions(G: nx.Graph, conditional_functions):
    '''
    :param G: networkx Graph
    :param conditional_functions: conditional function or a list derof

    :return: list of node labels (tuples containing labels of nodes that
             edge connects) satisfying the conditions

    :Example:

    >>> conditional_functions = [lambda x: x['polarity'] > 0,
    >>>                          lambda x: x['subjectivity'] > 0.5]
    >>> nodes = get_nodes_by_conditions(G, conditional_functions)
    '''

    if not isinstance(conditional_functions, list):
        conditional_functions = [conditional_functions]

    return [node_label for node_label
            in list(G.nodes)
            if check_node(G.nodes[node_label], conditional_functions)]


def check_node(node, conditional_functions):
    for conditional_function in conditional_functions:
        if not conditional_function(node):
            return False
    return True
