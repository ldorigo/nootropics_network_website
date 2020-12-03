#%%

import json
from typing import Dict, List, Tuple, Union

import networkx as nx
from networkx.algorithms.bipartite.basic import color
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

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
    node_color_attribute: str = None,
    node_size_attribute: str = None,
    positions: Dict[Union[str, int], Tuple[int, int]] = None,
):

    nodes_df = pd.DataFrame(dict(graph.nodes(data=True))).T.convert_dtypes()
    nodes_df["x"] = [x for x, y in positions.values()]
    nodes_df["y"] = [y for x, y in positions.values()]
    nodes_df["degree"] = dict(graph.degree()).values()
    nodes_df["empty"] = 0

    if node_color_attribute and nodes_df[node_color_attribute].dtype == "object":
        nodes_df[node_color_attribute] = nodes_df[node_color_attribute].apply(
            lambda x: x[0] if x else "None"
        )
    # if not node_color_attribute:
    #     node_color_attribute = "empty"
    # if not node_size_attribute:
    #     node_size_attribute = "empty"
    hovers = get_nodes_hover(graph)

    # node_names = list(graph.nodes)

    # This is stupid but plotly is retarted
    if node_color_attribute and node_size_attribute:
        node_trace = px.scatter(
            nodes_df,
            x="x",
            y="y",
            color=node_color_attribute,
            size=node_size_attribute,
        )
    elif node_color_attribute:
        node_trace = px.scatter(
            nodes_df,
            x="x",
            y="y",
            color=node_color_attribute,
        )
    elif node_size_attribute:
        node_trace = px.scatter(
            nodes_df,
            x="x",
            y="y",
            color=node_size_attribute,
        )
    else:
        node_trace = px.scatter(
            nodes_df,
            x="x",
            y="y",
        )

    node_trace.update_traces(hovertext=hovers, hoverinfo="text")
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
    for trace in edge_traces:
        node_trace.add_trace(trace)

    node_trace.update_layout(showlegend=False)
    # annotations = compute_annotations(graph=graph)
    # figure = go.Figure(
    #     data=data,
    #     layout=go.Layout(
    #         # autosize=False,
    #         # width=1200,
    #         # height=1200,
    #         # showlegend=False,
    #         margin={"l": 20, "r": 20, "t": 25, "b": 25},
    #         xaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
    #         yaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
    #     ),
    # )
    # if size_dict:
    #     figure.update_layout(
    #         autosize=False, width=size_dict["width"], height=size_dict["height"]
    #     )
    # figure.add_annotation(annotations)
    return node_trace


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
