import matplotlib.pyplot as plt
import wojciech as w


def plot_comparison_of_attribute_distributions(
        graphs,
        graph_names,
        attribute_name,
        attribute_parent,
        attribute_function,
        attribute_function_name,
        as_probability_distribution=False,
        bins=100,
        show=True
):
    figure, axess = plt.subplots(len(graphs), 1,
                                 figsize=(12, 4 * len(graphs) + 1),
                                 sharex='all',
                                 sharey='all')

    for index, (graph, graph_name, axes) \
            in enumerate(zip(graphs, graph_names, axess)):

        figure.suptitle(f'Distribution of the {attribute_parent} attribute: '
                        f'"{attribute_name}"',
                        y=min(0.98 + 0.003 * (len(graphs) - 1), 0.995),
                        size=20)

        w.graph.plot_distribution(
            graph,
            quantity='attribute',
            attribute_name=attribute_name,
            attribute_parent=attribute_parent,
            attribute_function=attribute_function,
            attribute_function_name=attribute_function_name,
            as_probability_distribution=as_probability_distribution,
            plot_type='bar',
            bins=bins,
            axes=axes,
            annotate=False
        )

        axes.set_title(graph_name)
        if as_probability_distribution:
            axes.set_ylabel('Probability of value')
        else:
            axes.set_ylabel('Count')

        if index == len(graphs) - 1:
            if attribute_function is not None:
                axes.set_xlabel(f'{attribute_function_name}({attribute_name})')
            else:
                axes.set_xlabel(f'{attribute_name}')

        axes.spines['top'].set_color('white')
        axes.spines['right'].set_color('white')
        axes.set_facecolor('white')
        axes.xaxis.label.set_fontsize(14)
        axes.yaxis.label.set_fontsize(14)
        axes.title.set_fontsize(16)

    if show:
        plt.show()

    return axess
