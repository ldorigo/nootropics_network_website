# %% Functions to place nodes on a 2d space
import json
import networkx as nx
from fa2 import ForceAtlas2

try:
    import library_functions as lf
except ModuleNotFoundError:
    import project.library_functions as lf
try:
    from config import Config
except ModuleNotFoundError:
    from project.config import Config

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


def get_fa2_layout(
    graph: nx.Graph,
    edge_weight_attribute: str = None,
    saved: str = None,
    save: str = None,
):
    """Generate a layout using the fa2 algorithm, or load one from disk.

    Args:
        graph (nx.Graph): graph for which to compute the layout
        edge_weight_attribute (str, optional): Which edge attribute to use for computing the layout. WARNING: only works with latest fa2 version.
        saved (str, optional): If not none, load the layout from the given path instead of computing it. Defaults to None.
        save (str, optional): if not none, save the layout to the given path. Defaults to None.

    Returns:
        Dict: networkx layout giving the position of nodes
    """

    if saved:
        with open(Config.Path.shared_data_folder / saved, "r") as f:
            layout = json.load(f)
            assert (
                len(layout) == graph.number_of_nodes()
            ), "Loaded layout does not have the same amount of nodes as the given graph"
            for node in graph.nodes:
                assert (
                    node in layout
                ), "The graph contains a node that was not found in the layout"
            return layout
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

    if save:
        with open(Config.Path.shared_data_folder / save, "w") as f:
            json.dump(f, layout)
    return layout


def get_circle_layout(graph: nx.Graph):
    return nx.drawing.layout.circular_layout(graph)
