import networkx as nx
import numpy as np
import pandas as pd
import wojciech as w

def to_dataframe(G: nx.Graph,
                 properties = tuple()):

    # Error check
    valid_properties = ('betweenness',
                        'eigenvector centrality',
                        'degree',
                        'in-degree',
                        'out-degree')

    for property in properties:
        if property not in valid_properties:
            raise Exception('Invalid property: "' + property + '"')

    # ---
    data_frame = pd.DataFrame.from_dict(dict(G.nodes(data=True)),
                                        orient='index')

    for property in properties:
        if property == 'betweenness':
            data_frame[property] = \
                w.graph.betweenness(G)

        if property == 'degree':
            data_frame[property] = \
                w.graph.degrees(G)

        if property == 'eigenvector centrality':
            data_frame[property] = \
                w.graph.eigenvector_centrality(G)

        elif property == 'in-degree':
                data_frame[property] = \
                    w.graph.degrees(G, direction='in')

        elif property == 'out-degree':
            data_frame[property] = \
                w.graph.degrees(G, direction='out')

    return data_frame




