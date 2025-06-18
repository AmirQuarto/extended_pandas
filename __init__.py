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
from .augment import *

PandasObject.view = xlwings.view

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
def flatten_columns(DF, sep = "_"):
    
    DF.columns = [sep.join(col).strip() for col in DF.columns.values]

    return DF


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

    if lst_col is not None:
        df_return = DF[DF[lst_col].duplicated(keep=keep)].sort_values(lst_col)
    else:
        df_return = DF[DF.duplicated(keep=keep)]  # .sort_values(list())

    if bl_print:
        print(f"{len(DF)} \t| length of original DataFrame")
        print(f"{len(df_return)} \t| length of duplicated rows")

    return df_return


@as_method
def rc(df, lst_ordered = None, bl_left=True):
    """
    Reorders columns
    """

    if lst_ordered is None:
        print(list(df.columns))
        copy_(list(df.columns))
        return DF
        
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
def vc(DF, str_column, rounding_precision=2, order_by_str_column=False):
    """Shows value_counts"""
    if type(str_column) == list:
        assert (
            len(str_column) == 1
        ), "If you use list as input argument, it must have length of 1!"
        str_column = str_column[0]

    df_vc = (
        DF[str_column]
        .value_counts(dropna=False)
        .reset_index()
        # .rename(columns={str_column: "count", "index": str_column})
    )



    if order_by_str_column:
        print(f"Sorting values based on this column: {str_column}")
        df_vc.sort_values(str_column, inplace=True)

    df_vc["cumulative_sum"] = df_vc["count"].cumsum()

    df_vc["%_of_total"] = df_vc["count"] / df_vc["count"].sum()

    df_vc["cumulative_sum_in_%"] = df_vc["cumulative_sum"] / df_vc["count"].sum()

    return df_vc.reset_index(drop=True).round(rounding_precision)


@as_method
def flatten_columns(DF, sep = "_"):
    
    DF.columns = [sep.join(col).strip() for col in DF.columns.values]

    return DF

