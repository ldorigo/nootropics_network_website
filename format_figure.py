import matplotlib.pyplot as plt


def format_figure(fig: plt.Figure,
                  title: str = None,
                  x_label: str = None,
                  y_label: str = None,
                  title_y_position: float = 0.93):
    fig.set_figwidth(12)
    fig.set_figheight(8)
    fig.set_facecolor("white")
    if title is not None:
        fig.suptitle(title,
                     y=title_y_position,
                     verticalalignment='top',
                     fontsize=24)

    axes = fig.axes
    for ax in axes:
        ax.spines['top'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.set_facecolor("white")
        ax.xaxis.grid(which="both", linewidth=0.5)
        ax.yaxis.grid(which="both", linewidth=0.5)
        ax.xaxis.label.set_fontsize(18)
        ax.yaxis.label.set_fontsize(18)
        ax.title.set_fontsize(20)

    if x_label is not None:
        fig.text(0.5, 0.04, x_label,
                 ha='center',
                 fontdict={'size': 18})

    if y_label is not None:
        fig.text(0.04, 0.5, y_label,
                 va='center',
                 rotation='vertical',
                 fontdict={'size': 18})
