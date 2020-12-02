import networkx as nx
import numpy as np


def shuffle_attribute(G: nx.Graph, attribute_name):
    G_attribute_shuffled = G.copy()

    # Extract the old attribute values
    nodes, attribute_values = \
        zip(*nx.get_node_attributes(G, attribute_name).items())

    # Create the new attribute values by shuffling the old ones
    new_attribute_values = np.random.permutation(attribute_values)

    # Set the values of the attributes to the shuffled values
    new_attribute_values_dict = {node: {attribute_name: new_attribute_value}
                                 for node, new_attribute_value
                                 in zip(nodes, new_attribute_values)}

    nx.set_node_attributes(G_attribute_shuffled, new_attribute_values_dict)

    return G_attribute_shuffled
