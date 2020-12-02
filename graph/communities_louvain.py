import community
import networkx as nx
from collections import Counter


def communities_louvain(G: nx.Graph,
                        return_communities_of_1=False):

    # compute the best partition
    partition = community.best_partition(G)

    community_numbers = set(partition.values())
    communities = dict()

    if not return_communities_of_1:
        # Find the detected communities with more than 1 member
        number_of_nodes_in_community = Counter(partition.values())

        communities_with_more_than_1 = \
            [community_number for community_number
             in community_numbers
             if number_of_nodes_in_community[community_number] > 1]

    for node, community_number in partition.items():
        if return_communities_of_1:
            if community_number not in communities.keys():
                communities[community_number] = list()
            communities[community_number].append(node)
        else:
            if community_number in communities_with_more_than_1:
                if community_number not in communities.keys():
                    communities[community_number] = list()
                communities[community_number].append(node)

    return communities
