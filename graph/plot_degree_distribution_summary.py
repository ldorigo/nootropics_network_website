import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import powerlaw
import wojciech as w


def plot_degree_distribution_summary(graphs,
                                     directions=None,
                                     graph_names=None,
                                     graph_colors=None,
                                     title=None,
                                     title_y_position: float = 0.97,
                                     x_lim_lin=None,
                                     x_lim_log=None
                                     ):
    '''
        :param graphs: networkx Graph or a list of graphs
        :param directions: degree direction or a list of directions whose length
                           corresponds to number of graphs.
        :param graph_names: graph name or a list of names whose length
                            corresponds to number of graphs.
        :param graph_colors: graph color or a list of colors whose length
                            corresponds to number of graphs.
        :param title: title of the figure.
        :param title_y_position: the y position of the title of the figure.
        :param x_lim_lin: the x-axis limits for the lin-lin axes
        :param x_log_log: the x-axis limits for the log-log axes

        :return: a numpy array containing the grid of axes in the plot

        :Example:

        >>> plot_degree_distribution_summary(G)

        :Example:

        >>> graphs = [G1, G2]
        >>> graph_names = ['Graph 1', 'Graph 2']
        >>> graph_colors = ['red', 'blue']
        >>> directions = [None, 'in', 'out']
        >>> title = ['Comparison of Graph 1 and Graph 2']
        >>> title_y_position = 0.97
        >>> x_lim_lin = (0, 100)
        >>> x_lim_log = (1, 1000)
        >>> plot_degree_distribution_summary(graphs,
        >>>                                  graph_names=graph_names,
        >>>                                  graph_colors=graph_colors,
        >>>                                  title=title,
        >>>                                  title_y_position=title_y_position,
        >>>                                  x_lim_lin=x_lim_lin,
        >>>                                  x_lim_log=x_lim_log
        >>>                                  )
        '''

    if not isinstance(graphs, list):
        graphs = [graphs]

    # Assign default graph names.
    if graph_names is None:
        graph_names = [f'Graph {graph_number + 1}'
                       for graph_number in range(len(graphs))]

    # Assign default graph colors.
    if graph_colors is None:
        graph_colors = \
            plt.rcParams['axes.prop_cycle'].by_key()['color'][:len(graphs)]

    # Assign default directions
    if directions is None:
        if any([nx.is_directed(graph) for graph in graphs]):
            directions = [None, 'in', 'out']
        else:
            directions = [None]

    # Create a figure and axes for the plot
    figure, axes_all = plt.subplots(len(directions), 2,
                                    sharex='col', sharey='col',
                                    figsize=(12, 4 * len(directions) + 1))

    # Make sure that the axes_all 2 - dimensional, as we will use the
    # left column for lin-lin and right column for log-log plots.
    if len(axes_all.shape) < 2:
        axes_all = np.expand_dims(axes_all, axis=0)

    # Set the figure title
    if title is not None:
        figure.suptitle(title,
                        y=title_y_position,
                        verticalalignment='top',
                        fontsize=16)

    # Initialize min and max finders
    max_y_data = 0
    max_y_data_without_0_degree = 0
    min_y_data_without_0_degree = 1
    max_x_data = 0
    if len(graphs) == 1:
        lin_lin_graph_type = 'bar'
    else:
        lin_lin_graph_type = 'scatter'

    for graph, graph_name, graph_color \
            in zip(graphs, graph_names, graph_colors):

        common_plot_options = {'as_probability_distribution': True,
                               'color': graph_color}

        for index, (direction, axes_lin_lin, axes_log_log) \
                in enumerate(zip(directions, axes_all[:, 0],  axes_all[:, 1])):

            # Ignore  graphs
            if (direction is not None) & (not nx.is_directed(graph)):
                continue

            # Lin - lin axes
            if index == len(directions) - 1:
                annotate = ['title', 'x_label', 'y_label']
            else:
                annotate = ['title', 'y_label']

            # Define the plot options for the lin-lin graph
            lin_lin_plot_options = common_plot_options.copy()
            lin_lin_plot_options.update({'annotate': annotate,
                                         'axes': axes_lin_lin,
                                         'axis_scaling': 'lin-lin',
                                         'direction': direction,
                                         'label': graph_name,
                                         'plot_type': lin_lin_graph_type,
                                         })

            if lin_lin_graph_type == 'scatter':
                lin_lin_plot_options.update({'marker_size': 40})

            # Plot the degree distribution
            _, (degrees, distribution) = \
                w.graph.plot_degree_distribution(graph, **lin_lin_plot_options)

            # Apply axes formatting
            format_axes(axes_lin_lin)

            # Update min and max counters
            max_y_data = np.max((np.max(distribution), max_y_data))
            max_y_data_without_0_degree = np.max((np.max(distribution[1:]),
                                                  max_y_data_without_0_degree))
            min_y_data_nonzero =\
                np.min((np.min(distribution[distribution != 0]),
                        min_y_data_without_0_degree))
            max_x_data = np.max((np.max(degrees), max_x_data))

            # Log - log axes
            if index == len(directions) - 1:
                annotate = ['title', 'x_label']
            else:
                annotate = ['title']

            # Calculate power-law slope
            alpha =\
                powerlaw.Fit(w.graph.degrees(graph, direction=direction)).alpha

            # Define the plot options for the lin-lin graph
            log_log_plot_options = common_plot_options.copy()
            log_log_plot_options.update({'annotate': annotate,
                                         'axes': axes_log_log,
                                         'axis_scaling': 'log-log',
                                         'direction': direction,
                                         'label': rf'$\alpha$ = {alpha:.2f}',
                                         'marker_size': 40,
                                         'plot_type': 'scatter',
                                         })

            w.graph.plot_degree_distribution(graph, **log_log_plot_options)

            # Apply axes formatting
            format_axes(axes_log_log)

    # Adjust axes limits
    axes_all[0, 0].set_ylim((0, max_y_data + 0.05))
    axes_all[0, 1].set_ylim((
        np.power(10, np.floor(np.log10(min_y_data_nonzero))),
        np.power(10, np.ceil(np.log10(max_y_data_without_0_degree)))
    ))

    if x_lim_lin is not None:
        axes_all[0, 0].set_xlim(x_lim_lin)
    else:
        axes_all[0, 0].set_xlim((-3, max_x_data))

    if x_lim_log is not None:
        axes_all[0, 1].set_xlim(x_lim_log)
    else:
        axes_all[0, 1].set_xlim(
            (0.9, np.power(10, np.ceil(np.log10(max_x_data)))))


    # Show legends
    for index, (axes_lin_lin, axes_log_log) \
            in enumerate(zip(axes_all[:, 0], axes_all[:, 1])):
        if (len(graphs) > 1) & index == 0:
            axes_lin_lin.legend(prop={'size': 14})
        axes_log_log.legend(prop={'size': 14})

    # Show plots
    plt.show()

    return axes_all


def format_axes(axes):
    axes.spines['top'].set_color('white')
    axes.spines['right'].set_color('white')
    axes.xaxis.grid(which="both", linewidth=0.5)
    axes.yaxis.grid(which="both", linewidth=0.5)
    axes.xaxis.label.set_fontsize(12)
    axes.yaxis.label.set_fontsize(12)
    axes.title.set_fontsize(14)
