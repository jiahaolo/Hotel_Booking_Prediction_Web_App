"""
Unit tests for the clean module.
"""

import pytest

import pandas as pd
import numpy as np

from src.clean import delete_duplicates, fill_missing_values, drop_error_rows
from src.clean import get_datetime_features, label_encoding, log_transform, drop_columns


def test_delete_duplicates():
    """
    Happy path: Tests the delete_duplicates function.
    """
    df_in = pd.DataFrame({'a': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10],
                          'b': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10],
                          'c': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10]})
    df_true = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                            'b': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                            'c': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})

    df_out = delete_duplicates(df_in).reset_index(drop=True)
    assert df_out.equals(df_true)


def test_delete_duplicates_non_df():
    """
    Unhappy path: Tests the delete_duplicates function with a non-dataframe.
    """
    df_in = 1

    with pytest.raises(TypeError):
        delete_duplicates(df_in)


def test_fill_missing_values():
    """
    Happy path: Tests the fill_missing_values function.
    """
    df_in = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6, 7, 8, np.nan, np.nan],
                          'b': [1, 2, 3, 4, 5, 6, np.nan, np.nan, 9, 10]})
    df_true = pd.DataFrame({'a': [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 0.0, 0.0],
                            'b': [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 0.0, 0.0, 9.0, 10.0]})

    df_out = fill_missing_values(df_in)
    assert df_out.equals(df_true)


def test_fill_mising_values_non_missing_values():
    """
    Unhappy path: Tests the fill_missing_values function with a dataframe without missing values.
    """
    df_in = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                          'b': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
    df_true = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                            'b': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})

    df_out = fill_missing_values(df_in)
    assert df_out.equals(df_true)


def test_drop_error_rows():
    """
    Happy path: Tests the drop_error_rows function.
    """
    df_in = pd.DataFrame({'adults': [0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                          'children': [0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                          'babies': [0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                          'adr': [1, 2, 3, 1, 2, 3, 4, 5, 6, 7, 8, 0, 0]})
    df_true = pd.DataFrame({'adults': [1, 2, 3, 4, 5, 6, 7, 8],
                            'children': [1, 2, 3, 4, 5, 6, 7, 8],
                            'babies': [1, 2, 3, 4, 5, 6, 7, 8],
                            'adr': [1, 2, 3, 4, 5, 6, 7, 8, ]})

    df_out = drop_error_rows(df_in).reset_index(drop=True)
    assert df_out.equals(df_true)


def test_drop_error_rows_wrong_columns():
    """
    Unhappy path: Tests the drop_error_rows function with wrong columns.
    """
    df_in = pd.DataFrame({'adlts': [0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                          'childr': [0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                          'baby': [0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                          'adrate': [1, 2, 3, 1, 2, 3, 4, 5, 6, 7, 8, 0, 0]})
    with pytest.raises(KeyError):
        drop_error_rows(df_in)


def test_get_datetime_features():
    """
    Happy path: Tests the get_datetime_features function.
    """
    df_in = pd.DataFrame({'reservation_status_date': [
                         "7/1/2005", "7/15/2005", "7/30/2005"]})
    df_true = pd.DataFrame({'reservation_status_date': [pd.to_datetime("7/1/2005"), pd.to_datetime("7/15/2005"), pd.to_datetime("7/30/2005")],
                            'year': [2005, 2005, 2005],
                            'month': [7, 7, 7],
                            'day': [1, 15, 30],
                            'weekday': [4, 4, 5], })
    df_out = get_datetime_features(df_in)
    assert df_out.equals(df_true)


def test_get_datetime_features_non_dt_columns():
    """
    Unhappy path: Tests the get_datetime_features function with non-datetime columns.
    """
    df_in = pd.DataFrame({'reservation_status_date': ["A", "B", "C"]})

    with pytest.raises(ValueError):
        get_datetime_features(df_in)


def test_label_encoding():
    """
    Happy path: Tests the test_label_encoding function
    """
    df_in = pd.DataFrame({'a': ['a', 'b', 'c', 'd', 'e'],
                          'b': ['f', 'g', 'h', 'i', 'j']})
    df_true = pd.DataFrame({'a': [0, 1, 2, 3, 4],
                            'b': [0, 1, 2, 3, 4]})
    df_out = label_encoding(df_in, ['a', 'b'])
    assert df_out.equals(df_true)


def test_label_encoding_wrong_data_type():
    """
    Unhappy path: Tests the test_label_encoding function with wrong data type
    """
    df_in = 64

    with pytest.raises(TypeError):
        label_encoding(df_in)


def test_log_transform():
    """
    Happy path: Tests the log_transform function
    """
    df_in = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                          'b': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
    df_true = pd.DataFrame({'a': map(lambda x: np.log(x+1),[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
                            'b': map(lambda x: np.log(x+1),[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])})
    df_out = log_transform(df_in, ['a', 'b'])
    assert df_out.equals(df_true)


def test_log_transform_wrong_data_type():
    """
    Unhappy path: Tests the log_transform function with wrong data type
    """
    df_in = pd.DataFrame({'a': ['a', 'b', 'c', 'd', 'e'],
                          'b': ['f', 'g', 'h', 'i', 'j']})

    with pytest.raises(KeyError):
        log_transform(df_in)


def test_drop_columns():
    """
    Happy path: Tests the drop_columns function
    """
    df_in = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                          'b': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
    df_true = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
    df_out = drop_columns(df_in, ['b'])
    assert df_out.equals(df_true)


def test_drop_columns_wrong_data_type():
    """
    Unhappy path: Tests the drop_columns function with wrong data type
    """
    df_in = 64

    with pytest.raises(TypeError):
        drop_columns(df_in, ['b'])
