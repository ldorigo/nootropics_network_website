from typing import List, Tuple
import dash_bootstrap_components as dbc
import dash_html_components as html


def make_table_from_items(items: List[Tuple], title):
    table = dbc.Table(
        children=[
            html.Thead(title),
            html.Tbody(
                [
                    html.Tr([html.Th(name.title()), html.Td(value)])
                    for name, value in items
                ]
            ),
        ],
        borderless=True,
        striped=True,
        hover=True,
    )
    return table
