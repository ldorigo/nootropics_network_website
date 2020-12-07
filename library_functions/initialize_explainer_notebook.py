# Imports
try:
    import library_functions as lf
except ModuleNotFoundError:
    import project.library_functions as lf

try:
    from library_functions.config import Config
except ModuleNotFoundError:
    from project.library_functions.config import Config

import numpy as np
import pandas as pd
import warnings
import wojciech as w

from IPython.core.interactiveshell import InteractiveShell
from IPython.display import Markdown, display


# Define a function that will print a markdown text.
def printmd(string):
    display(Markdown(string))


# Disable warnings
warnings.filterwarnings('ignore')

# Define maximum of rows to show for the pandas tables
pd.options.display.max_rows = 100

# Show all code outputs in the cell outputs
InteractiveShell.ast_node_interactivity = "all"
