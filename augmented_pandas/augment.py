from functools import wraps
from copy import deepcopy
import pandas as pd
from pandas.core.base import PandasObject

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
def augment_sorted_values(DF, column_name, sep):
    """
    Sorts the values in each row of a specified column in a DataFrame
    using vectorized operations for better performance.
    """
    # Split strings into lists of substrings
    split_data = DF[column_name].str.split(sep)
    
    # Sort each list of substrings
    sorted_data = split_data.map(np.sort)
    
    # Join the sorted substrings back into strings
    DF[f"{column_name}_sorted"] = sorted_data.str.join(sep)
    return DF



@as_method
def augment_count(DF, column_names):

    assert 'count' not in list(DF.columns)
    
    df_count = (
        DF[column_names]
        .value_counts(dropna = False)
        .reset_index()
    )

    return DF.merge(df_count,on = column_names, how = 'left')
