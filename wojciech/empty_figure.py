import matplotlib.pyplot as plt


def empty_figure():
    figure = plt.figure(figsize=(12, 8))
    axes = figure.gca()

    return figure, axes
