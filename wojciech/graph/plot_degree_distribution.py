import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import wojciech as w


def plot_degree_distribution(G: nx.Graph,
                             direction: str = None,
                             as_probability_distribution=False,
                             axes: plt.Axes = None,
                             annotate=['all'],
                             label=None,
                             axis_scaling='lin-lin',
                             show_cumulative=False,
                             plot_options_dict: dict = None,
                             plot_type='scatter',
                             **kwargs):

    if isinstance(annotate, str):
        annotate = [annotate]

    # Histogram
    degrees, distribution = w.graph.degree_distribution(
        G,
        direction=direction,
        as_probability_distribution=as_probability_distribution
    )

    # Plot
    if plot_options_dict is None:
        if plot_type == 'scatter':
            plot_options_dict = \
                {'marker': 'o', 's': 3, 'c': 'blue'}
        elif plot_type == 'bar':
            plot_options_dict = {'color': 'blue'}
        else:
            plot_options_dict = dict()

    if 'color' in kwargs:
        if plot_type == 'scatter':
            plot_options_dict['c'] = kwargs['color']
        else:
            plot_options_dict['color'] = kwargs['color']

    if 'marker_size' in kwargs:
        if plot_type == 'scatter':
            plot_options_dict['s'] = kwargs['marker_size']

    new_figure_created = False
    if axes is None:
        new_figure_created = True
        figure = plt.figure()
        figure.set_facecolor('white')
        axes = figure.gca()
        axes.set_facecolor('white')

    if direction is None:
        title = 'Degree distribution'
    elif direction == 'in':
        title = 'In-degree distribution'
    elif direction == 'out':
        title = 'Out-degree distribution'
    else:
        raise Exception('Invalid direction: "' + direction + '"')

    if as_probability_distribution:
        y_label = 'Probability of node degree'
    else:
        y_label = 'Number of nodes'

    if ('title' in annotate) or ('all' in annotate):
        axes.set_title(title)
    if ('x_label' in annotate) or ('all' in annotate):
        axes.set_xlabel('Node degree')
    if ('y_label' in annotate) or ('all' in annotate):
        axes.set_ylabel(y_label)

    if plot_type == 'scatter':
        plot = axes.scatter(degrees, distribution,
                         label=label, **plot_options_dict)
        axes.grid()
    elif plot_type == 'bar':
        plot = axes.bar(degrees, distribution,
                        label=label, **plot_options_dict)
    else:
        raise Exception('Unknown plot type: "' + plot_type + '"')

    if axis_scaling == 'lin-lin':
        if plot_type == 'scatter':
            axes.set_xlim(0, max(degrees))
        elif plot_type == 'bar':
            axes.set_xlim(-1, max(degrees))

    elif axis_scaling == 'log-log':
        axes.set_xscale('log')
        axes.set_yscale('log')
        axes.set_xlim(0.8, 10 ** np.ceil(np.log10(max(degrees))))
    else:
        raise Exception('Unknown axis scaling: "' + axis_scaling + '"')

    if show_cumulative:
        cumulative_curve = axes.plot(degrees, np.cumsum(distribution),
                                     color='#eb9b34')
        axes.legend((cumulative_curve[0],), ('Cumulative',))

    if new_figure_created:
        w.format_figure(figure)

    return axes, (degrees, distribution)
