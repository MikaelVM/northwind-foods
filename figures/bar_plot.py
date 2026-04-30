"""Module for creating and saving bar plots from a DataFrame."""
from pathlib import Path
import matplotlib.pyplot as plt

import pandas as pd

def bar_plot(
        dataframe: pd.DataFrame,
        *,
        x_col: str,
        y_col: str,
        title: str,
        x_label: str,
        y_label: str,
        save_path: Path,
        save_format: str = 'png',
        size_width: int = 10,
        size_height: int = 6,
        rotation: int = 50
) -> None:
    """Create a bar plot from a DataFrame and save it to a file.

    Args:
        dataframe (pd.DataFrame): The DataFrame containing the data to plot.
        x_col (str): The name of the column to use for the x-axis.
        y_col (str): The name of the column to use for the y-axis.
        title (str): The title of the plot.
        x_label (str): The label for the x-axis.
        y_label (str): The label for the y-axis.
        save_path (Path): The path where the plot image will be saved.
    """
    plt.figure().set_size_inches(size_width, size_height)
    plt.bar(dataframe[x_col], dataframe[y_col])
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=rotation)
    plt.savefig(save_path, format=save_format)
    plt.close()
