import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import svd
import seaborn as sns
import pandas as pd


class MachineLearningData:
    attributeNames = None
    classNames = None
    X = None
    y = None

    def __init__(self, X=None, attributeNames=None, y=None, classNames=None):
        self.X = X
        self.attributeNames = attributeNames
        self.y = y
        self.classNames = classNames

    def attribute_correlation_matrix(self):
        return np.corrcoef(self.X.T)

    def attribute_mean(self, names_of_attributes='all'):
        if names_of_attributes == 'all':
            return np.mean(self.X, axis=0)
        else:
            return_as_array = True
            if isinstance(names_of_attributes, str):
                names_of_attributes = [names_of_attributes]
                return_as_array = False

            index_attributes = [self.attributeNames.index(name_of_attribute)
                                for name_of_attribute in names_of_attributes]

            mean = np.mean(self.X[:, index_attributes], axis=0)

            if return_as_array:
                return mean
            else:
                return mean[0]

    def attribute_std(self,
                      names_of_attributes='all',
                      empirical=False):
        if names_of_attributes == 'all':
            return np.std(self.X, axis=0)
        else:
            return_as_array = True
            if isinstance(names_of_attributes, str):
                names_of_attributes = [names_of_attributes]
                return_as_array = False

            index_attributes = [self.attributeNames.index(name_of_attribute)
                                for name_of_attribute in names_of_attributes]

            if empirical:
                ddof = 1  # std denominator = N - 1
            else:
                ddof = 0  # std denominator = N - 0 = N
            std = np.std(self.X[:, index_attributes], axis=0, ddof=ddof)

            if return_as_array:
                return std
            else:
                return std[0]

    def C(self):
        return len(self.classNames)

    def get_attribute(self, name_of_attribute):
        return self.X[:, self.attributeNames.index(name_of_attribute)]

    def delete_attributes(self, attribute_names):
        if isinstance(attribute_names, str):
            attribute_names = [attribute_names]

        for attribute_name in attribute_names:
            index_column_to_delete = self.attributeNames.index(attribute_name)
            self.attributeNames.pop(index_column_to_delete)
            self.X = np.delete(self.X, index_column_to_delete, axis=1)

    def delete_data_rows(self, row_indices):
        self.X = np.delete(self.X, row_indices, axis=0)
        self.y = np.delete(self.y, row_indices, axis=0)

    def M(self):
        return self.X.shape[1]

    def N(self):
        return self.X.shape[0]

    def plot_attribute_correlation_matrix(self):
        # figure = plt.figure()
        # axes = plt.axes()
        # plt.imshow(self.attribute_correlation_matrix(),
        #             vmin=-1, vmax=1)
        # plt.xticks(range(self.M()), self.attributeNames, rotation=90)
        # plt.yticks(range(self.M()), self.attributeNames, rotation=0)
        # plt.colorbar()
        # plt.tight_layout()
        # plt.show()

        sns.set_style("white")

        # Generate a large random dataset
        rs = np.random.RandomState(33)
        d = pd.DataFrame(data=self.X,
                         columns=self.attributeNames)

        # Compute the correlation matrix
        corr = d.corr()

        # Generate a mask for the upper triangle
        mask = np.triu(np.ones_like(corr, dtype=bool))

        # Set up the matplotlib figure
        f, ax = plt.subplots(figsize=(11, 9))

        # Generate a custom diverging colormap
        cmap = sns.diverging_palette(230, 20, as_cmap=True)

        # Draw the heatmap with the mask and correct aspect ratio
        sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1, vmin=-1, center=0,
                    square=True, linewidths=.5, cbar_kws={"shrink": .5})

        plt.show()

    def plot_attributes(self,
                        name_attribute_x,
                        name_attribute_y=None,
                        outlier_threshold_std_from_median=2,
                        axes: plt.Axes = None,
                        annotate=True,
                        marker_size=2):

        x = self.get_attribute(name_attribute_x)

        show_plot_at_end = False
        if axes is None:
            figure = plt.figure()
            axes = plt.axes()
            figure.set_facecolor('white')
            axes.set_facecolor('white')
            show_plot_at_end = True

        plot_options = \
            {'marker': 'o', 'markersize': marker_size,
             'linestyle': 'None', 'linewidth': 0.5}

        if name_attribute_y is None:
            # Statistics
            N = len(x)
            mean = np.mean(x)
            median = np.median(x)
            std = np.std(x)

            # Find outliers
            outliers_threshold_low = \
                median - (2 * outlier_threshold_std_from_median * std)
            outliers_threshold_high = \
                median + (2 + outlier_threshold_std_from_median * std)
            number_of_outliers = np.sum(np.logical_or(
                x > outliers_threshold_high,
                x < outliers_threshold_low
            ))

            # Plot
            if annotate:
                axes.set_title(f"{name_attribute_x}\n"
                               f"N: {N}, "
                               f"$ \mu $: {mean:.1e}, "
                               f"median: {median:.1e}, "
                               f"$ \sigma $: {std:.1e}\n"
                               f"outliers (> {outlier_threshold_std_from_median:.1f} "
                               f"$ \sigma $ from median): {number_of_outliers}")
                axes.set_xlabel('Element index')
                axes.set_ylabel('Attribute value')

            legend_entries = list()
            for class_index in range(len(self.classNames)):
                legend_entries.append(self.classNames[class_index])
                logical_index_in_class = self.y == class_index
                index_in_class = np.arange(len(self.y))[logical_index_in_class]
                x_in_class = x[index_in_class]
                axes.plot(index_in_class, x_in_class, **plot_options)

            # Median line
            if annotate:
                axes.plot([1, len(x)], [median, median],  # median
                          'k-', linewidth=1)

            axes.set_xlim(0)

            legend_entries.append('Median')

        else:
            y = self.get_attribute(name_attribute_y)

            if annotate:
                axes.set_xlabel(name_attribute_x)
                axes.set_ylabel(name_attribute_y)
            legend_entries = list()
            for class_index in range(len(self.classNames)):
                legend_entries.append(self.classNames[class_index])
                logical_index_in_class = self.y == class_index
                x_in_class = x[logical_index_in_class]
                y_in_class = y[logical_index_in_class]
                axes.plot(x_in_class, y_in_class, **plot_options)

        if annotate:
            axes.legend(legend_entries)

        if show_plot_at_end:
            plt.show()

    def plot_attributes_boxplot(self, mode: str = 'raw',
                                y_scale: str = 'lin'):
        if mode == 'raw':
            X = self.X
            mode_string = ', raw data'
        elif mode == 'centered and normalized':
            X = self.X_centered()
            mode_string = ', data centered ($\mu = 0$) and normalized ' \
                          'with $\sigma$'
        elif mode == 'centered':
            X = self.X_centered(normalize_data_by_std=False)
            mode_string = ', data centered with mean = 0'
        else:
            raise Exception('Unknown mode: "' + str(mode) + '"')

        figure = plt.figure()
        axes = plt.axes()
        plt.title('Attribute overview' + mode_string)
        plt.boxplot(X, labels=self.attributeNames)
        plt.ylabel('Attribute values')
        plt.xticks(rotation=90)
        if y_scale == 'log':
            axes.set_yscale('log')
        plt.show()

    def plot_attribute_reconstruction_from_svd(self, attribute_name,
                                               number_of_principal_components='all',
                                               axes: plt.Axes = None,
                                               marker_size=3):

        original_data = self.get_attribute(attribute_name)
        reconstruction = self.reconstruction_from_principal_components(
            number_of_principal_components=number_of_principal_components,
            attribute_names=[attribute_name])

        if axes is None:
            figure = plt.figure()
            axes = plt.axes()
            figure.set_facecolor('white')
            axes.set_facecolor('white')
            axes.set_title(attribute_name
                           + f", {number_of_principal_components} principal "
                             f"components")
            axes.set_xlabel('Original data')
            axes.set_ylabel('Reconstructed data')

        axes.scatter(original_data, reconstruction, s=marker_size)
        # plt.show()

    def plot_principal_components_vs_original_attributes(self,
                                                         principal_component_numbers='all',
                                                         normalize_data_by_std=True,
                                                         new_figure=True):

        principal_components = self.principal_components(
            normalize_data_by_std=normalize_data_by_std)

        if principal_component_numbers == 'all':
            principal_component_indices = range(self.M())
        else:
            principal_component_indices = \
                np.array(principal_component_numbers) - 1

        if new_figure:
            figure = plt.figure()
            axes = plt.axes()
        else:
            figure = plt.gcf()
            axes = plt.gca()

        figure.set_facecolor('white')
        axes.set_facecolor('white')

        bar_width = 0.75 / len(principal_component_indices)
        original_attribute_numbers = np.arange(1, self.M() + 1)

        # Plot the significance of each of the original

        for principal_component_index in principal_component_indices:
            plt.bar(original_attribute_numbers
                    + principal_component_index * bar_width,
                    principal_components[:, principal_component_index],
                    width=bar_width)

        plt.xticks(original_attribute_numbers
                   + (len(principal_component_indices) - 1) / 2 * bar_width,
                   self.attributeNames,
                   rotation=90)
        plt.title('Contribution of original attributes to principal '
                  'components\n'
                  'Data normalized with their standard deviation')
        plt.xlabel('Original attribute', size=12)
        plt.ylabel('PCA coefficients', size=12)
        plt.grid(linewidth=0.3)
        legend_strings = ['PC ' + str(principal_component_index + 1)
                          for principal_component_index in
                          principal_component_indices]
        plt.legend(legend_strings,
                   bbox_to_anchor=(1.005, 1.03),
                   loc='upper left')
        plt.show()

    def plot_variance_explained(self,
                                normalize_data_by_std=True,
                                threshold=0.9,
                                new_figure=True):

        # compute the diagonal of the PCA's sigma matrix
        s = self.svd(compute_uv=False,
                     normalize_data_by_std=normalize_data_by_std)

        # Compute variance explained by principal components
        rho = (s * s) / (s * s).sum()

        if new_figure:
            figure = plt.figure()
            axes = plt.axes()
        else:
            figure = plt.gcf()
            axes = plt.gca()

        figure.set_facecolor('white')
        axes.set_facecolor('white')

        # Plot variance explained
        plt.figure()
        plt.plot(range(1, len(rho) + 1), rho * 100, 'x-')
        plt.plot(range(1, len(rho) + 1), np.cumsum(rho) * 100, 'o-')
        plt.plot([1, len(rho)], np.array([threshold, threshold]) * 100, 'k--')
        plt.title('Variance explained by principal components', size=18)
        plt.xlabel('Principal component', size=14)
        plt.ylabel('Variance explained [%]', size=14)
        plt.ylim(0, 105)
        plt.legend(['Individual', 'Cumulative', 'Threshold'])
        plt.grid()
        plt.show()

    def principal_components(self, normalize_data_by_std=True):
        _, _, Vh = svd(self.X_centered(normalize_data_by_std),
                       full_matrices=False)
        return Vh.T

    def projection_onto_principal_components(self,
                                             normalize_data_by_std=True, ):

        return (self.X_centered() @ self.principal_components(
            normalize_data_by_std=normalize_data_by_std))

    def reconstruction_from_principal_components(self,
                                                 attribute_names='all',
                                                 number_of_principal_components='all',
                                                 normalize_data_by_std=True):
        if number_of_principal_components == 'all':
            number_of_principal_components = self.M()

        projection = self.projection_onto_principal_components(
            normalize_data_by_std=normalize_data_by_std)
        projection = projection[:, :number_of_principal_components]

        principal_components = \
            self.principal_components()[:, :number_of_principal_components]

        reconstruction_raw = projection @ principal_components.T
        if normalize_data_by_std:
            reconstruction = reconstruction_raw * self.attribute_std()
        reconstruction = reconstruction + self.attribute_mean()

        if attribute_names != 'all':
            attribute_indices = [self.attributeNames.index(attribute_name)
                                 for attribute_name in attribute_names]

            reconstruction = reconstruction[:, attribute_indices]

        return reconstruction

    def svd(self, normalize_data_by_std=True, compute_uv=True):
        return svd(self.X_centered(normalize_data_by_std),
                   full_matrices=False,
                   compute_uv=compute_uv)

    def X_centered(self, normalize_data_by_std=True):
        # Subtract the attribute mean the attribute values
        X_centered = self.X - (np.ones((self.N(), 1)) * self.attribute_mean())

        if normalize_data_by_std:
            X_centered = X_centered / self.attribute_std()

        return X_centered
