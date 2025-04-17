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


def _assure_same_length(DF1, DF2):
    assert len(DF1) == len(DF2), "DataFrames must have the same length"


def _assure_only_new_columns(DF1, DF2, new_columns = None):

    expected_columns = set(DF1.columns).union(new_columns)
    unexpected_columns = set(DF2.columns) - expected_columns

    assert not unexpected_columns, (
        f"There are unexpected columns: {unexpected_columns}"
    )
    

def as_augment(same_length=True, new_columns=None):
    """
    A decorator that makes a function available as a method.
    The first argument must be a DataFrame.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Deepcopy input arguments to avoid side effects
            
            df_input = args[0]  # The first argument should be the DataFrame
            
            df_return = func(*deepcopy(args), **deepcopy(kwargs))

            # Validate DataFrame length if same_length is True
            if same_length:
                _assure_same_length(df_return, df_input)

            # Validate expected columns if new_columns is specified
            if new_columns:
                _assure_only_new_columns(df_return, df_input, new_columns)

            return df_return

        # Add the function as a method to PandasObject
        setattr(PandasObject, func.__name__, wrapper)

        return wrapper

    return decorator



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
def vc(DF, column_name):
    return (DF[column_name]
            .value_counts(dropna=False)
            .reset_index()
            )


@as_method
def augment_sorted_values(df, column_name, sep):
    """
    Sorts the values in each row of a specified column in a DataFrame
    using vectorized operations for better performance.
    """
    # Split strings into lists of substrings
    split_data = df[column_name].str.split(sep)
    
    # Sort each list of substrings
    sorted_data = split_data.map(np.sort)
    
    # Join the sorted substrings back into strings
    df[f"{column_name}_sorted"] = sorted_data.str.join(sep)
    return df


# Example usage
# (pd.DataFrame({'A': ["b=a ", "c=d", "x=y", "y=x"]})
# .augment_sorted_values("A", sep="=")
# )

@as_method
def augment_count(DF, column_names):

    assert 'count' not in list(DF.columns)
    
    df_count = (
        DF[column_names]
        .value_counts(column_names, dropna = False)
        .reset_index()
    )

    return DF.merge(df_count,on = column_names, how = 'left')
