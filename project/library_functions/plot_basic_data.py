import plotly.graph_objects as go
from plotly.subplots import make_subplots

try:
    import library_functions as lf
except ModuleNotFoundError:
    import project.library_functions as lf


def get_wiki_plots_figure():
    pages_distribution = make_subplots(
        rows=4,
        cols=1,
        subplot_titles=(
            "Page Length (N. of Characters)",
            "Amount of Links per Page",
            "Amount of Synonyms (redirects) per Page",
            "Amount of Categories per Page",
        ),
    )
    pages_distribution.add_trace(
        go.Histogram(
            x=lf.get_page_lengths(),
            xbins_end=10000,
            xbins_size=500,
            hovertemplate=f"Length (N. of Characters):  %{{x}} <br>Number of pages:  %{{y}}",
        ),
        row=1,
        col=1,
    )
    # pages_distribution.update_xaxes(, row=1, col=1)
    pages_distribution.add_trace(
        go.Histogram(
            x=lf.get_number_of_links(),
            xbins_end=15,
            hovertemplate=f"Amount of Links:  %{{x}} <br>Number of pages:  %{{y}}",
        ),
        row=2,
        col=1,
    )
    pages_distribution.add_trace(
        go.Histogram(
            x=lf.get_number_of_synonyms(),
            xbins_end=20,
            xbins_size=1,
            hovertemplate=f"Amount of Synonyms (redirects):  %{{x}} <br>Number of pages:  %{{y}}",
        ),
        row=3,
        col=1,
    )
    pages_distribution.add_trace(
        go.Histogram(
            x=lf.get_number_of_categories(),
            xbins_end=15,
            xbins_size=1,
            hovertemplate=f"Amount of Categories:  %{{x}} <br>Number of pages:  %{{y}}",
        ),
        row=4,
        col=1,
    )

    pages_distribution.update_layout(
        margin={"l": 10, "r": 10, "t": 25, "b": 10},
        xaxis={},
        yaxis={},
        showlegend=False,
        clickmode="event+select",
        height=650,
    )

    for annotation in pages_distribution.layout.annotations:
        annotation.update(x=0.025, xanchor="left")
    return pages_distribution


def get_reddit_plots_figure():
    posts_distribution = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=(
            "Post Length (N. of Characters)",
            "Amount of Nootropics Mentions per Post",
        ),
    )
    posts_distribution.add_trace(
        go.Histogram(
            x=lf.get_post_lengths(),
            xbins_end=2000,
            hovertemplate=f"Length (N. of Characters):  %{{x}} <br>Number of posts:  %{{y}}",
        ),
        row=1,
        col=1,
    )
    # pages_distribution.update_xaxes(, row=1, col=1)
    posts_distribution.add_trace(
        go.Histogram(
            x=lf.get_n_of_matches_per_post(),
            xbins_end=15,
            xbins_size=1,
            hovertemplate=f"Amount of mentions:  %{{x}} <br>Number of posts:  %{{y}}",
        ),
        row=2,
        col=1,
    )

    posts_distribution.update_layout(
        # margin={"l": 20, "r": 20, "t": 25, "b": 25},
        xaxis={},
        yaxis={},
        showlegend=False,
        clickmode="event+select",
        height=650,
    )

    for annotation in posts_distribution.layout.annotations:
        annotation.update(x=0.025, xanchor="left")
    return posts_distribution