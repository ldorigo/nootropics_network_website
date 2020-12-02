import networkx as nx

def largest_connected_component(G: nx.Graph,
                                connection='weak'):
    if G.is_directed():
        if connection == 'weak':
            largest_connected_component_nodes =\
                max(nx.weakly_connected_components(G), key=len)
        elif connection == 'strong':
            largest_connected_component_nodes = \
                max(nx.strongly_connected_components(G), key=len)
        else:
            raise Exception('Invalid connection: "' + connection + '".')

    else:
        largest_connected_component_nodes = \
            max(nx.connected_components(G), key=len)

    return G.subgraph(largest_connected_component_nodes).copy()
