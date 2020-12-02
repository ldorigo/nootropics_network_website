import networkx as nx

def erdos_renyi_like(G: nx.Graph):
    number_of_nodes = G.number_of_nodes()
    possible_connections = number_of_nodes * (number_of_nodes - 1)
    if not G.is_directed():
        possible_connections /= 2

    probability_of_connection = G.number_of_edges() / possible_connections

    G_erdos_renyi = nx.gnp_random_graph(number_of_nodes,
                                        probability_of_connection,
                                        directed=G.is_directed())

    return(G_erdos_renyi)