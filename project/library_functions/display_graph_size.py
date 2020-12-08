import networkx as nx
import numpy as np
import pandas as pd

from IPython.core.display import display
from typing import Dict


def display_graph_size(graphs: Dict[str, nx.Graph]):

    pandas_dict = {
        'Nodes': [graph.number_of_nodes()
                  for graph in graphs.values()],
        'Edges': [graph.number_of_edges()
                  for graph in graphs.values()]
    }

    df_graph_size = (pd.DataFrame
                     .from_dict(pandas_dict)
                     .set_index(pd.Index(list(graphs.keys()))))

    display(df_graph_size)