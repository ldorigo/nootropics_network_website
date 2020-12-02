import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid1 import make_axes_locatable
import networkx as nx
import numpy as np
import wojciech as w


def plot_properties(G: nx.Graph,
                    x_property = None,
                    y_property = None,
                    plot_type ='scatter',  # scatter / heatmap
                    axes: plt.Axes = None,
                    colormap_norm = 'lin',
                    bins=10):
    # Error check
    #
    valid_graph_types = ('scatter',
                         'heatmap')

    if plot_type not in valid_graph_types:
        raise Exception('Invalid graph type: "' + plot_type + '"')

    #
    valid_colormap_norms = ('lin',
                            'log')

    if colormap_norm not in valid_colormap_norms:
        raise Exception('Invalid colormap norm: "' + colormap_norm + '"')

    #
    valid_properties = ('betweenness',
                        'eigenvector centrality',
                        'degree',
                        'in-degree',
                        'out-degree')

    for property in [x_property, y_property]:
        if property not in valid_properties:
            raise Exception('Invalid property: "' + property + '"')

    # Load properites
    def load_property(property_name):
        if property_name == 'betweenness':
            data = w.graph.betweenness(G)
        elif property_name == 'eigenvector centrality':
            data = w.graph.eigenvector_centrality(G)
        elif property_name == 'degree':
            data = w.graph.degrees(G)
        elif property_name == 'in-degree':
            data = w.graph.degrees(G, direction='in')
        elif property_name == 'out-degree':
            data = w.graph.degrees(G, direction='out')

        return  data

    x_data = load_property(x_property)
    y_data = load_property(y_property)
    max_of_data = np.max((x_data, y_data))

    # Plot
    new_figure_created = False
    if axes is None:
        new_figure_created = True
        figure = plt.figure(figsize=(12, 8))
        figure.set_facecolor('white')
        axes = figure.gca()
        axes.set_facecolor('white')

    if plot_type == 'scatter':
        plot_options = {'marker': 'o',
                        's': 5}

        axes.scatter(x_data,
                     y_data,
                     **plot_options)

        axes.set_xlabel(x_property)
        axes.set_ylabel(y_property)
        axes.set_xlim(np.floor(min(x_data)))
        axes.set_ylim(np.floor(min(y_data)))

    elif plot_type == 'heatmap':
        # create an axes on the right side of ax. The width of cax will be 7%
        # of ax and the padding between cax and ax will be fixed at 0.07 inch.
        if colormap_norm == 'lin':
            cnorm = None;
        elif colormap_norm == 'log':
            cnorm = LogNorm()

        heatmap, xedges, yedges, image =\
            axes.hist2d(x_data, y_data, bins=bins, cmap='Reds', norm=cnorm)

        divider = make_axes_locatable(axes)
        colorbar_axes = divider.append_axes("right", size=0.1, pad=0.07)
        figure.colorbar(image, cax=colorbar_axes)

    if new_figure_created:
        w.format_figure(figure)

    return axes