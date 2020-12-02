import networkx as nx

from operator import itemgetter


def most_frequent_edges(G: nx.Graph,
                        n=None,
                        printout=False):
    edges_count = nx.get_edge_attributes(G, "count")
    edges_count_sorted = sorted(edges_count.items(),
                                key=itemgetter(1),
                                reverse=True)

    if n is not None:
        edges_count_sorted = \
            edges_count_sorted[:min(len(edges_count_sorted), n)]

    if printout:
        print('\nMost frequent edges:')
        for index, (edge, count) in enumerate(edges_count_sorted):
            print(f'\t{index + 1}. {edge}, {count} occurrences')

    return edges_count_sorted
