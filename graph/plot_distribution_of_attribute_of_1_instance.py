import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import wojciech as w
import typing as t


def plot_distribution_of_attribute_of_1_instance(
        graphs: t.Union[nx.Graph, t.Iterable[nx.Graph]],
        instance,
        instance_label,
        attribute_name,
        graph_names: t.Union[str, t.Iterable[str]] = None,
        axess: t.Union[plt.Axes, t.Iterable[plt.Axes]] = None,
        title=None,
        annotate='all',
        x_label_size=14,
        y_label_size=14,
        title_size=14,
        bins=100
):
    # Sanitize input
    if not isinstance(graphs, list):
        graphs = [graphs]

    if graph_names is None:
        graph_names = [None for graph in graphs]

    if not isinstance(graph_names, list):
        graph_names = [graph_names]

    if not isinstance(annotate, list):
        annotate = [annotate]

    # Get the figure and axes handles
    new_figure_created = False
    if axess is None:
        new_figure_created = True
        figure, axess = plt.subplots(len(graphs), 1,
                                     figsize=(12, 4 * len(graphs) + 1),
                                     sharey='all',
                                     sharex='all')

    if not isinstance(axess, (list, np.ndarray)):
        axess = [axess]

    figure = axess[0].get_figure()

    # Set the title of the figure
    if ('title' in annotate) or ('all' in annotate):
        if title is None:
            title = f'Distribution of attribute: "{attribute_name}" ' \
                    f'for {instance}: "{instance_label}"'
        figure.suptitle(title,
                        y=min(0.98 + 0.003 * (len(graphs) - 1), 0.995),
                        verticalalignment='top',
                        fontsize=20)

    for index, (graph, graph_name, axes) in \
            enumerate(zip(graphs, graph_names, axess)):

        if instance == 'node':
            if graph.has_node(instance_label):
                attribute_values = graph.nodes[instance_label][attribute_name]
            else:
                attribute_values = []

        elif instance == 'edge':
            if graph.has_edge(*instance_label):
                attribute_values = graph.edges[instance_label][attribute_name]
            else:
                attribute_values = []
        else:
            raise ValueError(f'Invalid instance "{instance}"')

        axes.hist(attribute_values, bins=bins)

        if graph_name is not None:
            axes.set_title(graph_name)

        if ('x_label' in annotate) or ('all' in annotate):
            if index == len(graphs) - 1:
                axes.set_xlabel(attribute_name.capitalize())

        if ('y_label' in annotate) or ('all' in annotate):
            axes.set_ylabel('Count')

        axes.xaxis.label.set_fontsize(x_label_size)
        axes.yaxis.label.set_fontsize(y_label_size)
        axes.title.set_fontsize(title_size)
        axes.spines['top'].set_color('white')
        axes.spines['right'].set_color('white')
        axes.set_facecolor("white")

    if new_figure_created:
        plt.show()

    return axess
