import pandas as pd
import wojciech as w
import matplotlib.pyplot as plt


def plot_conditional_frequency_distribution(cfd,
                                            axes: plt.Axes = None):
    df_cfd = pd.DataFrame.from_dict(cfd, orient='index')

    new_figure_created = False
    if axes is None:
        new_figure_created = True
        figure = plt.figure(figsize=(12, 8))
        axes = figure.gca()

    df_cfd.plot.bar(ax=axes)

    if new_figure_created:
        w.format_figure(figure)

    return axes
