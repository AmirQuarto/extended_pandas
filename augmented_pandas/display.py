from IPython.display import display

from .augment import *



@as_method
def display_(DF):
    display(DF)
    return DF


@as_method
def display_fulltext(DF):
    import pandas as pd
    with pd.option_context('display.max_colwidth', None):
        display(DF)
    return DF


@as_method
def display_allcols(DF):
    with pd.option_context('display.max_columns', None):
        display(DF)
    return DF


@as_method
def display_all_(DF):
    import pandas as pd
    with pd.option_context('display.max_columns', None,
                           'display.max_colwidth', None):
        display(DF)
    return DF
