import plotly.graph_objects as go
from plotly.subplots import make_subplots
from project.library_functions import (
    get_page_lengths,
    get_number_of_links,
    get_number_of_categories,
    get_number_of_synonyms,
)


def get_wiki_plots_figure():
    pages_distribution = make_subplots(
        rows=4,
        cols=1,
        subplot_titles=(
            "Length (N. of Characters)",
            "Amount of Links",
            "Amount of Synonyms (redirects)",
            "Amount of categories",
        ),
    )
    pages_distribution.add_trace(
        go.Histogram(
            x=get_page_lengths(),
            hovertemplate=f"Length (N. of Characters):  %{{x}} <br>Number of pages:  %{{y}}",
        ),
        row=1,
        col=1,
    )
    # pages_distribution.update_xaxes(, row=1, col=1)
    pages_distribution.add_trace(
        go.Histogram(
            x=get_number_of_links(),
            hovertemplate=f"Amount of Links:  %{{x}} <br>Number of pages:  %{{y}}",
        ),
        row=2,
        col=1,
    )
    pages_distribution.add_trace(
        go.Histogram(
            x=get_number_of_synonyms(),
            hovertemplate=f"Amount of Synonyms (redirects):  %{{x}} <br>Number of pages:  %{{y}}",
        ),
        row=3,
        col=1,
    )
    pages_distribution.add_trace(
        go.Histogram(
            x=get_number_of_categories(),
            hovertemplate=f"Amount of categories:  %{{x}} <br>Number of pages:  %{{y}}",
        ),
        row=4,
        col=1,
    )

    pages_distribution.update_layout(
        # margin={"l": 20, "r": 20, "t": 25, "b": 25},
        xaxis={},
        yaxis={},
        showlegend=False,
        clickmode="event+select",
        height=650,
    )
    return pages_distribution