import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS


def plot_wordcloud(text,
                   title=None,
                   axes: plt.Axes = None):

    if isinstance(text, list):
        text = ' '.join(text)

    wc = WordCloud(max_words=100,
                   collocations=False,
                   stopwords=set(STOPWORDS),
                   margin=10,
                   random_state=1).generate(text)

    new_figure_created = False
    if axes is None:
        new_figure_created = True
        figure = plt.figure(figsize=(12, 8))
        axes = figure.gca()

    default_colors = wc.to_array()
    axes.imshow(default_colors, interpolation="bilinear")
    axes.set_axis_off()

    if title is not None:
        axes.set_title(title, fontsize=20)

    return axes
