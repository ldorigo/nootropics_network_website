import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import wojciech as w
from fa2 import ForceAtlas2


def plot_force_atlas_2(G: nx.Graph,
                       alpha=None,
                       edge_color=(0, 0, 0, 0.1),
                       node_color=np.array([(0, 0, 1, 0.6)]),
                       node_size=30,
                       edge_width=0.15,
                       iterations=100,
                       outboundAttractionDistribution=False,
                       edgeWeightInfluence=0.5,
                       jitterTolerance=0.05,
                       barnesHutOptimize=True,
                       barnesHutTheta=0.6,
                       scalingRatio=5,
                       strongGravityMode=False,
                       gravity=1,
                       verbose=True):
    if G.is_directed():
        G = G.to_undirected()

    # Calculate the positions of the nodes
    forceatlas2 = ForceAtlas2(
        # Behavior alternatives
        outboundAttractionDistribution=outboundAttractionDistribution,
        # Dissuade hubs
        linLogMode=False,  # NOT IMPLEMENTED
        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
        edgeWeightInfluence=edgeWeightInfluence,

        # Performance
        jitterTolerance=jitterTolerance,  # Tolerance
        barnesHutOptimize=barnesHutOptimize,
        barnesHutTheta=barnesHutTheta,
        multiThreaded=False,  # NOT IMPLEMENTED

        # Tuning
        scalingRatio=scalingRatio,
        strongGravityMode=strongGravityMode,
        gravity=gravity,

        # Log
        verbose=verbose)

    positions = forceatlas2.forceatlas2_networkx_layout(G,
                                                        pos=None,
                                                        iterations=iterations)

    # If required by user, compute node sizes.
    def compute_node_sizes(quantity_array):
        size_biggest_node = 300
        return (quantity_array / np.max(quantity_array) * size_biggest_node)

    if node_size == 'by degree':
        node_size = compute_node_sizes(w.graph.degrees(G))

    # Create the plot
    figure = plt.figure(figsize=(12, 8))
    axes = figure.gca()

    nx.draw(G,
            positions,
            edge_color=edge_color,
            node_size=node_size,
            node_color=node_color,
            width=edge_width,
            # alpha=alpha,
            ax=axes)