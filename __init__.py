import pandas as pd
import numpy as np
import os
import xlwings as xw
from IPython.display import display

from copy import deepcopy
from functools import wraps
from pandas.core.base import PandasObject
from pyperclip import copy as copy_
from pyperclip import paste as paste_

def as_method(func):
    """
    This decrator makes a function also available as a method.
    The first passed argument must be a DataFrame.
    """
    # from functools import wraps
    # from copy import deepcopy
    # import pandas as pd
    # from pandas.core.base import PandasObject

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*deepcopy(args), **deepcopy(kwargs))

    setattr(PandasObject, wrapper.__name__, wrapper)

    return wrapper


@as_method
def ur(DF, bl_print=True):
    """Returns Unique Rows."""

    DF_unique = DF.drop_duplicates()

    if bl_print:
        print(len(DF), "\t| Length of DataFrame")
        print(len(DF_unique), "\t| Length of DataFrame without dupps\n")

    return DF_unique


@as_method
def dr(DF, lst_col=None, keep=False, bl_print=True):
    """Shows duplicated_rows"""

    if bl_print:
        print(f"{len(DF)} \t| length of original DataFrame")

    if lst_col is not None:
        df_return = DF[DF[lst_col].duplicated(keep=keep)].sort_values(lst_col)
    else:
        df_return = DF[DF.duplicated(keep=keep)]  # .sort_values(list())

    if bl_print:
        print(f"{len(df_return)} \t| length of duplicated rows")

    return df_return


@as_method
def augment_reason_column(DF, str_template, column_name="Reason", print_row=0, round_=1):
    from pandas.api.types import is_numeric_dtype
    import re

    # Just like R:)
    # lst_ = str_template.split("`")

    # This one is far more flexible:
    lst_ = re.split("'|\"|`", str_template)

    series_ = ""
    for i in lst_:
        if i in DF.columns:
            if is_numeric_dtype(DF[i]):
                series_ += DF[i].round(round_).map(str)
            else:
                series_ += DF[i].map(str)
        else:
            series_ += i

    DF[column_name] = series_

    print(series_.values[print_row])

    return DF


@as_method
def rc(df, lst_ordered, bl_left=True):
    """
    Reorders columns
    """
    lst_col = [i for i in df.columns if i not in lst_ordered]

    if bl_left:
        return df[lst_ordered + lst_col]

    else:
        return df[lst_col + lst_ordered]


@as_method
def display_(DF):
    display(DF)
    return DF


def load_xl():
    DF = xw.load().reset_index()
    display(DF)
    return DF


@as_method
def vc(DF, column_name):
    return (DF[column_name]
            .value_counts(dropna=False)
            .reset_index()
            )
