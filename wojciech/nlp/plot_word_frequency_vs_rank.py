import matplotlib.pyplot as plt
from wojciech.nlp.word_frequency_vs_rank import word_frequency_vs_rank
from wojciech.format_figure import format_figure


def plot_word_frequency_vs_rank(text,
                                axes: plt.Axes = None,
                                label=None,
                                title=None,
                                annotate=True,
                                as_probability=False):

    vs_rank = word_frequency_vs_rank
    rank, frequency = vs_rank(text,
                              as_probability=as_probability)

    new_figure_created = False
    if axes is None:
        new_figure_created = True
        figure = plt.figure(figsize=(12, 8))
        axes = figure.gca()

    axes.scatter(rank, frequency, label=label)
    axes.set_yscale('log')
    axes.set_xscale('log')
    axes.grid()

    if annotate:
        axes.set_xlabel('Word rank')
        if as_probability:
            y_label = 'Probability of occurrence'
        else:
            y_label = 'Frequency of occurrence'

        axes.set_ylabel(y_label)

    if title is not None:
        axes.set_title(title)

    if new_figure_created:
        format_figure(figure)

    return axes
