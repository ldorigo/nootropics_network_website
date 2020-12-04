from typing import Dict, List

import matplotlib
import matplotlib.cm as cm
import networkx as nx
import numpy as np
import plotly.express as px


def build_cytoscape_elements(
    graph: nx.Graph,
    positions: Dict,
    node_attributes: List = None,
    edge_attributes: List = None,
):
    if not node_attributes:
        node_attributes = []
    if not edge_attributes:
        edge_attributes = []

    properties = {"node_attributes": {}, "edge_attributes": {}}
    # Preparation: Set the right node attribute properties

    node_generator = ((node, data) for node, data in graph.nodes(data=True))
    firstnode, firstdata = next(node_generator)
    for attribute in node_attributes:
        properties["node_attributes"][attribute] = {}
        properties["node_attributes"][attribute]["values"] = []

        # If the node's attribute is a list, we take the first value for a discrete node or the average for a continuous. Not ideal but can't think of anything better
        if type(firstdata[attribute]) == list:
            # If the list is empty, we need to iterate over other nodes until we find one that isn't empty...
            if not firstdata[attribute]:
                while not firstdata[attribute]:
                    firstnode, firstdata = next(node_generator)
            if type(firstdata[attribute][0]) == str:
                att_value = firstdata[attribute][0]
            else:
                att_value = np.mean(firstdata[attribute])
        else:
            att_value = firstdata[attribute]

        # Determine wether it's a continuous or discrete attribute
        if type(att_value) in [int, float]:
            att_type = "continuous"
        else:
            att_type = "discrete"
        properties["node_attributes"][attribute]["type"] = att_type

        # If it's continuous, we need to determine the range to compute continuous color values:
        if att_type == "continuous":
            all_values = [np.mean(data) for _, data in graph.nodes(attribute)]
            min_val = min(all_values)
            max_val = max(all_values)

            norm = matplotlib.colors.Normalize(vmin=min_val, vmax=max_val, clip=True)
            mapper = cm.ScalarMappable(norm=norm, cmap=cm.Accent_r)
            # Add the mapper to the properties
            properties["node_attributes"][attribute]["color_mapper"] = mapper
        else:
            # If it's discrete: we will add it as a classname, so initialize an array of classnames
            properties["node_attributes"][attribute]["classnames"] = set()

    # And do the same for edges:
    edge_generator = ((e1, e2, data) for e1, e2, data in graph.edges(data=True))
    fe1, fe2, firstdata = next(edge_generator)
    for attribute in edge_attributes:
        properties["edge_attributes"][attribute] = {}
        properties["edge_attributes"][attribute]["values"] = []

        # If the edge's attribute is a list, we take the first value for a discrete edge or the average for a continuous. Not ideal but can't think of anything better
        if type(firstdata[attribute]) == list:

            # If the list is empty, we need to iterate over other nodes until we find one that isn't empty...
            if not firstdata[attribute]:
                while not firstdata[attribute]:
                    fe1, fe2, firstdata = next(edge_generator)

            if type(firstdata[attribute][0]) == str:
                att_value = firstdata[attribute][0]
            else:
                att_value = np.mean(firstdata[attribute])
        else:
            att_value = firstdata[attribute]

        # Determine wether it's a continuous or discrete attribute
        if type(att_value) in [int, float]:
            att_type = "continuous"
        else:
            att_type = "discrete"
        properties["edge_attributes"][attribute]["type"] = att_type

        # If it's continuous, we need to determine the range to compute continuous color values:
        if att_type == "continuous":
            all_values = [np.mean(data) for _, _, data in graph.edges(attribute)]
            min_val = min(all_values)
            max_val = max(all_values)

            norm = matplotlib.colors.Normalize(vmin=min_val, vmax=max_val, clip=True)
            mapper = cm.ScalarMappable(norm=norm, cmap=cm.Accent_r)
            # Add the mapper to the properties
            properties["edge_attributes"][attribute]["color_mapper"] = mapper

        else:
            # If it's discrete: we will add it as a classname, so initialize an array of classnames
            properties["edge_attributes"][attribute]["classnames"] = set()

    # Then, iterate over all nodes and add format them as cytoscape elements
    node_elements = []

    for node, data in graph.nodes(data=True):
        # At the very minimum, assign an id
        node_data = {"id": node}
        classes = ""
        for attribute in node_attributes:
            att_type = properties["node_attributes"][attribute]["type"]

            # If the node's attribute is a list, we take the first value for a discrete node or the average for a continuous. Not ideal but can't think of anything better
            if type(data[attribute]) == list:

                # If the list is empty: assign a dummy value if discrete
                if not data[attribute] and att_type == "discrete":
                    att_value = "None"
                elif att_type == "discrete":
                    att_value = data[attribute][0]
                else:
                    att_value = np.mean(data[attribute])
            else:
                att_value = data[attribute]

            if att_type == "discrete":
                # If attribute is discrete, add it as a class of the node
                att_value = att_value.replace(" ", "_")

                if classes:
                    classes += f" {att_value}"
                else:
                    classes = att_value
                # Also add it to the list of values in the properties
                properties["node_attributes"][attribute]["classnames"].add(att_value)
            else:
                # Otherwise:
                # If the attribute is continuous, then add both the raw data as well as its mapping on the color scale
                mapper = properties["node_attributes"][attribute]["color_mapper"]
                rgba = f"rgba{mapper.to_rgba(att_value)}"
                node_data[attribute + "_color"] = rgba

            node_data[attribute] = att_value

        node_elements.append(
            {
                "data": node_data,
                "position": {"x": positions[node][0], "y": positions[node][1]},
                "classes": classes,
                "locked": True,
            }
        )

    # Do the same for edges
    edge_elements = []
    for e1, e2, data in graph.edges(data=True):
        edge_data = {"source": e1, "target": e2}
        classes = ""
        for attribute in edge_attributes:
            att_type = properties["edge_attributes"][attribute]["type"]

            # If the edge's attribute is a list, we take the first value for a discrete edge or the average for a continuous. Not ideal but can't think of anything better
            if type(data[attribute]) == list:

                if not data[attribute] and att_type == "discrete":
                    att_value = "None"
                elif att_type == "discrete":
                    att_value = data[attribute][0]
                else:
                    att_value = np.mean(data[attribute])
            else:
                att_value = data[attribute]

            if att_type == "discrete":
                # replace spaces with underscores
                att_value = att_value.replace(" ", "_")

                # If attribute is discrete, add it as a class of the edge
                if classes:
                    classes += f" {att_value}"
                else:
                    classes = att_value
                # Also add it to the list of values in the properties
                properties["edge_attributes"][attribute]["classnames"].add(att_value)
            else:
                # Otherwise:
                # If the attribute is continuous, then add both the raw data as well as its mapping on the color scale
                mapper = properties["edge_attributes"][attribute]["color_mapper"]
                rgba = f"rgba{mapper.to_rgba(att_value)}"
                edge_data[attribute + "_color"] = rgba

            edge_data[attribute] = att_value

        edge_elements.append({"data": edge_data, "classes": classes})

    elements = node_elements + edge_elements

    return elements, properties


def make_stylesheet(properties, color_node_by: str = None):
    discrete_colorscale = (
        px.colors.qualitative.Alphabet * 10
    )  # make a long one to make sure no index out of bounds error
    color_mapping = None
    # Basic style for node and edges
    styling = [
        {
            "selector": "node",
            "style": {"background-color": "rgb(0.3,0.3,0.3)", "opacity": "0.6"},
        },
        {"selector": "edge", "style": {"opacity": "0.8"}},
    ]
    if color_node_by:
        if properties["node_attributes"][color_node_by]["type"] == "discrete":
            color_mapping = {}
            all_values = properties["node_attributes"][color_node_by]["classnames"]
            for index, value in enumerate(set(all_values)):
                if value in ["none", "None", "Other", "other", "L1-Other", "L0-Other"]:
                    color_mapping[value] = "black"
                else:
                    color_mapping[value] = discrete_colorscale[index]
                styling.append(
                    {
                        "selector": f".{value}",
                        "style": {"background-color": color_mapping[value]},
                    }
                )
        else:
            styling.append(
                {
                    "selector": "node",
                    "style": {"background-color": f"data({color_node_by}_color)"},
                }
            )

    return styling, color_mapping
