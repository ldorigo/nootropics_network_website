#%%

import json
from typing import Dict, List, Tuple, Union

import networkx as nx
import numpy as np
import plotly.graph_objects as go

try:
    from library_functions.config import Config
except:
    from project.library_functions.config import Config

# %%
with open(Config.Path.contents_per_substance, "r+") as f:
    contents_per_substance = json.load(f)
with open(Config.Path.urls_per_substance, "r+") as f:
    url_per_substance = json.load(f)


def get_edge_traces(
    graph: nx.Graph,
    positions: Dict[Union[str, int], Tuple[int, int]] = None,
    edge_weight_attribute: str = None,
    edge_hover_attributes: List[str] = None,
):
    edges_x = []
    edges_y = []
    widths = []
    colors = []
    names = []
    counts = []
    max_width = 20

    for e1, e2, data in graph.edges(data=True):
        x0, y0 = positions[e1]
        x1, y1 = positions[e2]
        # edges_x.append([x0, x1, x1 + 1, x0 + 1, x0])
        edges_x.append([x0, x1])
        # edges_y.append([y0, y1, y1, y0, y0])
        edges_y.append([y0, y1])
        names.append((e1, e2))

    if edge_weight_attribute:
        values = [data[edge_weight_attribute] for _, _, data in graph.edges(data=True)]
        logs = np.log(values)
        maxlog = np.max(logs)
        maxval = np.max(values)

        alphas = (logs / maxlog) ** 2

        colors = [f"rgba(40,40,40,{a:.4f})" for a in alphas]
        widths = (logs / maxlog) * max_width
    else:
        widths = np.repeat(1, len(edges_x))
        colors = np.repeat("rgba(40,40,40,0.1)", len(edges_x))

    edge_traces = []
    for i in range(len(edges_x)):
        if widths[i] > 0:
            trace = go.Scatter(
                x=edges_x[i],
                y=edges_y[i],
                line={"width": widths[i], "color": colors[i]},
                hoverinfo="text" if edge_hover_attributes else "none",
                mode="lines",
                fill="toself",
            )
            if edge_hover_attributes:
                text = f"Link between {names[i][0]} and +{names[i][1]}. <br>"
                if "count" in edge_hover_attributes:
                    text += f"This link came up {counts[i]} times."
                trace.text = text
            edge_traces.append(trace)

    return edge_traces


def split_text_at(text: str, length: int) -> str:
    words = text.split()

    results = []
    line_length = 0
    for word in words:
        if line_length < length:
            results.append(word)
            line_length += len(word)
        else:
            results.append("<br>")
            results.append(word)
            line_length = len(word)

    return " ".join(results)


def get_nodes_hover(graph: nx.Graph) -> List[str]:
    node_hovers = []

    for name, data in graph.nodes(data=True):
        hover = f"Nootropic: {name}, Degree: {graph.degree(name)}. <br>"

        if "categories" in data:
            hover += f"\n Part of {len(data['categories'])} categories. <br><br>"

        hover += f'"{split_text_at(contents_per_substance[name][:120], 40)}..."<br> <br> <br> '

        hover += f"Read more: {url_per_substance[name]}"
        node_hovers.append(hover)
    return node_hovers


def get_nodes_trace(
    graph: nx.Graph,
    node_weight_attribute: str = None,
    node_color_attribute: str = None,
    node_size_attribute: str = None,
    positions: Dict[Union[str, int], Tuple[int, int]] = None,
):
    nodes_x = []
    nodes_y = []
    colors = [] if node_color_attribute else "rgba(0,0,0,0.5)"
    sizes = [] if node_size_attribute else 12
    for node, data in graph.nodes(data=True):
        nodes_x.append(positions[node][0])
        nodes_y.append(positions[node][1])
        if node_color_attribute:
            if node_color_attribute != "degree":
                assert (
                    node_color_attribute in data
                ), f"Color attribute {node_color_attribute} not found in node data"
                if data[node_color_attribute]:
                    colors.append(data[node_color_attribute][0])
                else:
                    colors.append("None")
            else:
                colors.append(graph.degree(node))

        if node_size_attribute:
            if node_size_attribute != "degree":
                assert (
                    node_size_attribute in data
                ), f"Size attribute {node_size_attribute} not found in node data"
                sizes.append(data[node_size_attribute])
            else:
                sizes.append(graph.degree(node))

    hovers = get_nodes_hover(graph)

    node_names = list(graph.nodes)

    node_trace = go.Scatter(
        x=nodes_x,
        y=nodes_y,
        text=hovers,
        marker_color=colors,
        marker={"size": sizes, "sizemin": 5, "sizeref": 5},
        mode="markers",
        hoverinfo="text",
    )

    return node_trace


def draw_graph_plotly(
    graph: nx.Graph,
    positions: Dict[Union[str, int], Tuple[int, int]] = None,
    edge_weight_attribute: str = None,
    edges_only: bool = False,
    node_color_attribute: str = None,
    node_size_attribute: str = None,
    edge_hover_attributes: List[str] = None,
    size_dict: Dict[str, int] = None,
):

    # If no positions are passed, compute spring layout positioning
    if not positions:
        positions = nx.layout.spring_layout(graph, weight=edge_weight_attribute)

    edge_traces = get_edge_traces(
        graph=graph,
        positions=positions,
        edge_weight_attribute=edge_weight_attribute,
        edge_hover_attributes=edge_hover_attributes,
    )
    node_trace = get_nodes_trace(
        graph=graph,
        positions=positions,
        node_color_attribute=node_color_attribute,
        node_size_attribute=node_size_attribute,
    )

    data = edge_traces if edges_only else edge_traces + [node_trace]

    annotations = compute_annotations(graph=graph)
    figure = go.Figure(
        data=data,
        layout=go.Layout(
            # autosize=False,
            # width=1200,
            # height=1200,
            showlegend=False,
            margin={"l": 20, "r": 20, "t": 25, "b": 25},
            xaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
            yaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
        ),
    )
    if size_dict:
        figure.update_layout(
            autosize=False, width=size_dict["width"], height=size_dict["height"]
        )
    figure.add_annotation(annotations)
    return figure


def compute_annotations(graph: nx.Graph):
    annotations = go.layout.Annotation(
        text="Test",
        align="left",
        showarrow=False,
        xref="paper",
        yref="paper",
        x=1.1,
        y=0.8,
        bordercolor="black",
        borderwidth=1,
    )

    return annotations


# %%
