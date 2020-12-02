import networkx as nx


def remove_isolates(G: nx.Graph):
    G.remove_nodes_from(list(nx.isolates(G)))
    return G