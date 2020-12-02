import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import wojciech as w
import plotly.graph_objects as go


def plot_distribution(
    G: nx.Graph,
    quantity,
    as_probability_distribution=False,
    axes: plt.Axes = None,
    annotate=True,
    as_partial=(1, 1),
    attribute_name=None,
    attribute_function=None,
    attribute_function_name="",
    attribute_parent="node",
    axis_scaling="lin-lin",
    bins=None,
    label=None,
    show_cumulative=False,
    plot_options_dict: dict = None,
    plot_type="scatter",
    plotting_backend="matplotlib",
    **kwargs,
):

    # Check input for errors.
    valid_quantities = (
        "attribute",
        "degree",
        "in-degree",
        "out-degree",
        "shortest path length",
    )

    if quantity not in valid_quantities:
        raise Exception('Invalid quantity: "' + quantity + '".')

    # Load quantities.
    if quantity == "attribute":
        if attribute_function is None:
            x_label = (
                f"{attribute_parent.capitalize()} attribute: " f'"{attribute_name}"'
            )
        else:
            x_label = (
                f"{attribute_function_name}("
                f"{attribute_parent} attribute: "
                f'"{attribute_name}")'
            )

        if attribute_parent == "node":
            if as_probability_distribution:
                y_label = "Probability of attribute value"
            else:
                y_label = "Number of nodes"

        else:
            if as_probability_distribution:
                y_label = "Probability of attribute value"
            else:
                y_label = "Number of edges"

        title = f'Distribution of attribute: "{attribute_name}"'

        if attribute_parent == "node":
            attributes_dict = dict(nx.get_node_attributes(G, attribute_name))
            attribute_values = list(attributes_dict.values())

        elif attribute_parent == "edge":
            attributes_dict = dict(nx.get_edge_attributes(G, attribute_name))
            attribute_values = list(attributes_dict.values())
        else:
            raise ValueError(f'Invalid attribute object: "{attribute_parent}"')

        if attribute_function is not None:
            attribute_values = list(map(attribute_function, attribute_values))

        # Make sure attribute values is a numpy array
        attribute_values = np.array(attribute_values)

        # Remove NaNs
        nan_indices = np.isnan(attribute_values)
        attribute_values = attribute_values[~nan_indices]

        if bins is None:
            distribution, bins = np.histogram(attribute_values)
        else:
            distribution, bins = np.histogram(attribute_values, bins=bins)

        if as_probability_distribution:
            distribution = distribution / len(attribute_values)

        bin_centers = [np.mean([bins[i], bins[i + 1]]) for i in range(len(bins) - 1)]

    elif quantity in ["degree", "in-degree", "out-degree"]:
        x_label = "Node degree"
        if as_probability_distribution:
            y_label = "Probability of node degree"
        else:
            y_label = "Number of nodes"

        if quantity == "degree":
            direction = None
            title = "Degree distribution"

        elif quantity == "in-degree":
            direction = "in"
            title = "In-degree distribution"

        elif quantity == "out-degree":
            direction = "out"
            title = "Out-degree distribution"

        bin_centers, distribution = w.graph.degree_distribution(
            G,
            direction=direction,
            as_probability_distribution=as_probability_distribution,
        )

    elif quantity == "shortest path length":
        bin_centers, distribution = w.graph.shortest_path_length_distribution(
            G, as_probability_distribution=as_probability_distribution
        )

        title = "Shortest path length distribution"
        x_label = "Path length"
        if as_probability_distribution:
            y_label = "Probability of path length"
        else:
            y_label = "Number of paths"

    # Plot
    if plot_options_dict is None:
        if plot_type == "scatter":
            plot_options_dict = {
                "marker": "o",
                "markerfacecolor": "black",
                "markersize": 3,
                "linestyle": "None",
                "linewidth": 0.5,
                "color": "blue",
            }
        else:
            plot_options_dict = dict()

    if "color" in kwargs:
        plot_options_dict["color"] = kwargs["color"]

    if plot_type == "bar":
        number_of_parts = as_partial[0]
        part_number = as_partial[1]
        width_bin = bin_centers[1] - bin_centers[0]
        width_all_bars = 0.9 * width_bin
        width_bar = width_all_bars / number_of_parts

        adjustment = (
            np.linspace(0, width_all_bars, number_of_parts, endpoint=False)
            - width_all_bars / 2
            + width_bar / 2
        )[part_number - 1]
        bin_centers = bin_centers + adjustment

    if axis_scaling == "lin-lin":
        if plot_type == "scatter":
            x_start = min(bin_centers)
            x_end = max(bin_centers)
        elif plot_type == "bar":
            x_start = min(bin_centers) + np.min(adjustment) - 1.5 * width_bar
            x_end = max(bin_centers) + np.min(adjustment) + 1.5 * width_bar
    elif axis_scaling == "log-log":
        x_start = 1
        x_end = 10 ** np.ceil(np.log10(max(bin_centers)))
        if plotting_backend == "plotly":
            # plotly needs the log10 of the range for logplots
            x_start = np.log10(x_start)
            x_end = np.log10(x_end)
    else:
        raise Exception('Unknown axis scaling: "' + axis_scaling + '"')

    if plotting_backend == "matplotlib":
        new_figure_created = False
        if axes is None:
            new_figure_created = True
            figure = plt.figure()
            figure.set_facecolor("white")
            axes = figure.gca()
            axes.set_facecolor("white")

        if annotate:
            axes.set_title(title)
            axes.set_xlabel(x_label)
            axes.set_ylabel(y_label)

        if plot_type == "scatter":
            axes.plot(bin_centers, distribution, label=label, **plot_options_dict)
            axes.grid()
        elif plot_type == "bar":
            axes.bar(
                bin_centers,
                distribution,
                width=width_bar,
                label=label,
                **plot_options_dict,
            )
        else:
            raise Exception('Unknown plot type: "' + plot_type + '"')

        axes.set_xlim(x_start, x_end)

        if axis_scaling == "lin-lin":
            pass
        elif axis_scaling == "log-log":
            axes.set_xscale("log")
            axes.set_yscale("log")
        else:
            raise Exception('Unknown axis scaling: "' + axis_scaling + '"')

        if show_cumulative:
            cumulative_curve = axes.plot(
                bin_centers, np.cumsum(distribution), color="#eb9b34"
            )
            axes.legend((cumulative_curve[0],), ("Cumulative",))

        if as_partial[0] > 1:
            axes.legend()

        if new_figure_created:
            w.format_figure(figure)

        return axes

    elif plotting_backend == "plotly":
        if plot_type == "scatter":
            traces = [
                go.Scatter(
                    name="Distribution",
                    x=bin_centers,
                    y=distribution,
                    marker={"color": plot_options_dict["color"]},
                    mode="markers",
                    hovertemplate=f"{x_label}: %{{x}} <br> {y_label}: %{{y}}",
                )
            ]
        elif plot_type == "bar":
            traces = [
                go.Bar(
                    name="Distribution",
                    x=bin_centers,
                    y=distribution,
                    hovertemplate=f"{x_label}: %{{x}} <br> {y_label}: %{{y}}",
                )
            ]
        if show_cumulative:
            traces += [
                go.Scatter(
                    x=bin_centers,
                    y=np.cumsum(distribution),
                    name="Cumulative Distribution",
                    mode="lines",
                    hovertemplate=f"{x_label}: %{{x}} <br> Total {y_label}: %{{y}}",
                )
            ]
        figure = go.Figure(
            data=traces,
            layout=go.Layout(
                title=title,
                xaxis_title=x_label,
                yaxis_title=y_label,
                autosize=True,
                width=800,
                height=600,
                showlegend=True,
                margin={"l": 20, "r": 20, "t": 25, "b": 25},
                xaxis={
                    "type": "log" if axis_scaling == "log-log" else "linear",
                    "range": [x_start, x_end],
                },
                yaxis={"type": "log" if axis_scaling == "log-log" else "linear"},
            ),
        )

        return figure
    else:
        raise AssertionError("plotting_backeng can only be 'matplotlib' or 'plotly'")