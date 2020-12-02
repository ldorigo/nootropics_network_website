import networkx as nx

from operator import itemgetter


def most_central_nodes(G: nx.Graph,
                       by='degree',
                       n=None,
                       printout=False):

    if by == 'degree':
        most_linked = sorted(G.degree, key=itemgetter(1), reverse=True)

    elif by == 'in-degree':
        most_linked = sorted(G.in_degree, key=itemgetter(1), reverse=True)

    elif by == 'out-degree':
        most_linked = sorted(G.out_degree, key=itemgetter(1), reverse=True)

    elif by == 'betweenness':
        most_linked = sorted(nx.betweenness_centrality(G).items(),
                             key=itemgetter(1), reverse=True)

    elif by == 'eigenvector':
        most_linked = sorted(nx.eigenvector_centrality(G).items(),
                             key=itemgetter(1), reverse=True)
    else:
        raise ValueError(f'Unknown property: "{by}"')

    if n is None:
        n = len(most_linked)

    most_linked = most_linked[:min(n, len(most_linked))]

    if printout:
        print(f'\nNodes with highest {by} centrality:')
        for node, centrality_score in most_linked[:10]:
            print(f'\t{node}: {centrality_score:.3f}')