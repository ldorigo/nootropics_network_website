from typing import List, Tuple
import dash_bootstrap_components as dbc
import dash_html_components as html


def make_table_from_items(items: List[Tuple], title: str):

    if len(items[0]) == 2:
        # if two elements per item, then just plaintext
        body = [
            html.Tr([html.Th(name.title()), html.Td(value)]) for name, value in items
        ]
    else:
        # if 3, then third element is a link
        body = [
            html.Tr([html.Th(html.A(href=link, children=name.title())), html.Td(value)])
            for name, value, link in items
        ]

    table = dbc.Table(
        children=[
            html.Thead(
                html.Tr(
                    html.Th(colSpan=2, children=title, style={"text-align": "center"})
                )
            ),
            html.Tbody(body),
        ],
        borderless=True,
        striped=True,
        hover=True,
    )
    return table
