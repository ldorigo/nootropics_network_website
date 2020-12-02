# %% Functions to place nodes on a 2d space
import networkx as nx
from fa2 import ForceAtlas2

try:
    import library_functions as lf
except ModuleNotFoundError:
    import project.library_functions as lf

# %%


forceatlas2 = ForceAtlas2(
    # Behavior alternatives
    outboundAttractionDistribution=True,  # Dissuade hubs
    linLogMode=False,  # NOT IMPLEMENTED
    adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
    edgeWeightInfluence=1.0,
    # Performance
    jitterTolerance=0.5,  # Tolerance
    barnesHutOptimize=True,
    barnesHutTheta=1.2,
    multiThreaded=False,  # NOT IMPLEMENTED
    # Tuning
    scalingRatio=1,
    strongGravityMode=True,
    gravity=0.1,
    # Log
    verbose=True,
)


def get_fa2_layout(graph: nx.Graph, edge_weight_attribute: str = None):
    try:
        if edge_weight_attribute:
            layout = forceatlas2.forceatlas2_networkx_layout(
                graph, pos=None, weight_attr=edge_weight_attribute, iterations=1000
            )
        else:
            layout = forceatlas2.forceatlas2_networkx_layout(
                graph, pos=None, iterations=1000
            )
    except TypeError:
        print(
            "You need to install force atlas from source because the pip version doesn't support weighted edges. "
        )
        print("See https://github.com/bhargavchippada/forceatlas2 ")
        raise
    return layout


def get_circle_layout(graph: nx.Graph):
    return nx.drawing.layout.circular_layout(graph)
