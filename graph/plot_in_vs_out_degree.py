import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid1 import make_axes_locatable
import networkx as nx
import numpy as np
import wojciech as w


def plot_in_vs_out_degree(G: nx.Graph,
                          plot_type='heatmap',  # scatter / heatmap
                          axes: plt.Axes = None,
                          colormap_norm='lin'):
    # Error check
    valid_plot_types = ('scatter',
                        'heatmap')

    if plot_type not in valid_plot_types:
        raise Exception('Invalid plot type: "' + plot_type + '"')

    valid_colormap_norms = ('lin',
                            'log')

    if colormap_norm not in valid_colormap_norms:
        raise Exception('Invalid colormap norm: "' + colormap_norm + '"')

    ##
    in_degrees = w.graph.degrees(G, direction='in')
    out_degrees = w.graph.degrees(G, direction='out')
    max_degree = np.max((in_degrees, out_degrees))

    if plot_type == 'heatmap':
        bins = np.arange(max_degree + 1)
        heatmap, xedges, yedges = \
            np.histogram2d(in_degrees, out_degrees, bins=bins)
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

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

        axes.scatter(in_degrees,
                     out_degrees,
                     **plot_options)

        axes.set_xlabel('In-degree')
        axes.set_ylabel('Out-degree')
        axes.set_xlim(0)
        axes.set_ylim(0)

    elif plot_type == 'heatmap':
        if colormap_norm == 'lin':
            cnorm = None
        elif colormap_norm == 'log':
            cnorm = LogNorm(vmin=1, vmax=np.max(heatmap))

        plot = axes.imshow(heatmap.T,
                           extent=extent,
                           origin='lower',
                           cmap='Reds',
                           norm=cnorm)
        axes.set_xlim((0, np.ceil(max(in_degrees))))
        axes.set_ylim((0, np.ceil(max(out_degrees))))

        # create an axes on the right side of ax. The width of cax will be 7%
        # of ax and the padding between cax and ax will be fixed at 0.07 inch.
        divider = make_axes_locatable(axes)
        colorbar_axes = divider.append_axes("right", size="7%", pad=0.07)
        figure.colorbar(plot, cax=colorbar_axes)

    if new_figure_created:
        w.format_figure(figure)

    return axes
