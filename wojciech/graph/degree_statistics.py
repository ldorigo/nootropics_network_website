import networkx as nx
import numpy as np
from scipy import stats
import wojciech as w

def degree_statistics(G: nx.Graph,
                      node_labels = None,
                      printout = False):
    all_degrees = w.graph.degrees(G,
                                  node_labels=node_labels)

    if G.is_directed():
        in_degrees = w.graph.degrees(G,
                                     node_labels=node_labels,
                                     direction='in')
        out_degrees = w.graph.degrees(G,
                                      node_labels=node_labels,
                                      direction='out')


    statistics = dict()

    statistics['average degree'] = np.mean(all_degrees)
    if G.is_directed():
        statistics['average in-degree'] = np.mean(in_degrees)
        statistics['average out-degree'] = np.mean(out_degrees)

    statistics['median degree'] = np.median(all_degrees)
    if G.is_directed():
        statistics['median in-degree'] = np.median(in_degrees)
        statistics['median out-degree'] = np.median(out_degrees)

    mode_all_degrees, count_mode_in_degrees = np.asarray(stats.mode(all_degrees))
    if G.is_directed():
        mode_in_degrees, count_mode_in_degrees = np.asarray(stats.mode(in_degrees))
        mode_out_degrees, count_mode_out_degrees =\
            np.asarray(stats.mode(out_degrees))

    statistics['mode degree'] = mode_all_degrees[0]
    if G.is_directed():
        statistics['mode in-degree'] = mode_in_degrees[0]
        statistics['mode out-degree'] = mode_out_degrees[0]

    statistics['minimum degree'] = np.min(all_degrees)
    if G.is_directed():
        statistics['minimum in-degree'] = np.min(in_degrees)
        statistics['minimum out-degree'] = np.min(out_degrees)

    statistics['maximum degree'] = np.max(all_degrees)
    if G.is_directed():
        statistics['maximum in-degree'] = np.max(in_degrees)
        statistics['maximum out-degree'] = np.max(out_degrees)

    if printout:
        print('Overall degree:')
        print('\tMinimum: ', statistics['minimum degree'])
        print('\tMaximum: ', statistics['maximum degree'])
        print(f"\tAverage: {statistics['average degree']:.2f}")
        print('\tMedian: ', statistics['median degree'])
        print('\tMode: ', statistics['mode degree'])

        if G.is_directed():
            print()
            print('In-degrees:')
            print('\tMinimum: ', statistics['minimum in-degree'])
            print('\tMaximum: ', statistics['maximum in-degree'])
            print(f"\tAverage: {statistics['average in-degree']:.2f}")
            print('\tMedian: ', statistics['median in-degree'])
            print('\tMode: ', statistics['mode in-degree'])
            print()
            print('Out-degrees:')
            print('\tMinimum: ', statistics['minimum out-degree'])
            print('\tMaximum: ', statistics['maximum out-degree'])
            print(f"\tAverage: {statistics['average out-degree']:.2f}")
            print('\tMedian: ', statistics['median out-degree'])
            print('\tMode: ', statistics['mode out-degree'])

    return statistics
