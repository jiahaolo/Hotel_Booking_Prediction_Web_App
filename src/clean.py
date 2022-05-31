"""
This module contains functions used to import and clean the data.
"""

import logging
import typing

import pandas as pd
import numpy as np
from sklearn import preprocessing

logger = logging.getLogger(__name__)


def delete_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Deletes duplicates from a dataframe.

    Args:
        df (pd.DataFrame): The dataframe to be cleaned.

    Returns:
        A dataframe with duplicates removed.
    """
    logger.info('Deleting duplicates')
    return df.drop_duplicates()


def fill_missing_values(df: pd.DataFrame, value: float = 0) -> pd.DataFrame:
    """
    Fills missing values in a dataframe.

    Args:
        df (pd.DataFrame): The dataframe to be cleaned.

    Returns:
        A dataframe with missing values filled.
    """
    logger.info('Filling missing values with %f', value)
    return df.fillna(value)


def drop_error_rows(df: pd.DataFrame, cond: typing.List[str] = None) -> pd.DataFrame:
    """
    Drops rows with errors.

    Args:
        df (pd.DataFrame): The dataframe to be cleaned.

    Returns:
        A dataframe with rows with errors dropped.
    """
    if cond is None:
        logger.info('Dropping default error rows')
        cond = ['adults', 'children', 'babies', 'adr']

    df = df[~((df[cond[0]] == 0) & (df[cond[1]] == 0) & (df[cond[2]] == 0))]
    df = df[df[cond[3]] > 0]
    logger.info('Rows with errors dropped')
    return df


def get_datetime_features(df: pd.DataFrame, date_col: str = 'reservation_status_date') -> pd.DataFrame:
    """
    Extracts datetime features from a dataframe.

    Args:
        df (pd.DataFrame): The input datafra,.

    Returns:
        A dataframe with datetime features extracted.
    """
    logger.info('Converting %s to datetime features', date_col)
    df[date_col] = pd.to_datetime(df[date_col])
    df['year'] = df[date_col].dt.year
    df['month'] = df[date_col].dt.month
    df['day'] = df[date_col].dt.day
    df['weekday'] = df[date_col].dt.weekday
    logger.info('Datetime features extracted')
    return df


def label_encoding(df: pd.DataFrame, columns: typing.List[str] = None) -> pd.DataFrame:
    """
    Encodes a dataframe using label encoding.

    Args:
        df (pd.DataFrame): The dataframe to be cleaned.
        columns (list): The list of columns to be encoded.

    Returns:
        A dataframe with columns encoded.
    """
    if columns is None:
        logger.info('Encoding default columns')
        columns = ['hotel', 'meal', 'market_segment', 'distribution_channel',
                   'reserved_room_type', 'deposit_type', 'customer_type', 'year']
    for col in columns:
        l_encoder = preprocessing.LabelEncoder()
        l_encoder.fit(df[col])
        df[col] = l_encoder.transform(df[col])
    logger.info('Columns encoded')
    return df


def log_transform(df: pd.DataFrame, cols: typing.List = None) -> pd.DataFrame:
    """
    Transforms a column in a dataframe using log transformation.

    Args:
        df (pd.DataFrame): The input dataframe.
        col (str): The column to be transformed.

    Returns:
        A dataframe with the column transformed.
    """
    if cols is None:
        logger.info('Log transforming default columns')
        cols = ['lead_time', 'arrival_date_week_number', 'arrival_date_day_of_month',
                'agent', 'company', 'adr']
    for col in cols:
        df[col] = df[col].apply(lambda x: np.log(x+1))

    logger.info('Columns transformed')
    return df


def drop_columns(df: pd.DataFrame, columns: typing.List = None) -> pd.DataFrame:
    """
    Drops columns from a dataframe.

    Args:
        df (pd.DataFrame): The dataframe to be cleaned.
        columns (list): The list of columns to be dropped.

    Returns:
        A dataframe with columns dropped.
    """
    if columns is None:
        logger.info('Dropping default columns')
        columns = ['days_in_waiting_list', 'arrival_date_year', 'arrival_date_year', 'assigned_room_type',
                   'booking_changes', 'reservation_status', 'country', 'days_in_waiting_list',
                   'reservation_status_date', 'arrival_date_month']
    return df.drop(columns, axis=1)


def get_clean_data(input_path: str, output_path: str) -> pd.DataFrame:
    """
    Imports and cleans the data.

    Args:
        input_path (str): The path to the input data.
        output_path (str): The path to the output data.

    Returns:
        A dataframe with the cleaned data.
    """
    logger.info('Importing data')
    df = pd.read_csv(input_path)
    logger.info('Deleting duplicates')
    df = delete_duplicates(df)
    logger.info('Filling missing values')
    df = fill_missing_values(df)
    logger.info('Dropping error rows')
    df = drop_error_rows(df)
    logger.info('Extracting datetime features')
    df = get_datetime_features(df)
    logger.info('Encoding columns')
    df = label_encoding(df)
    logger.info('Transforming unused columns')
    df = log_transform(df)
    logger.info('Dropping columns')
    df = drop_columns(df)
    logger.info('Saving data')
    df.to_csv(output_path)
    return df


def get_features(df: pd.DataFrame, target_col: str = 'is_canceled') -> pd.DataFrame:
    """
    Extracts features from a dataframe.

    Args:
        df (pd.DataFrame): The full cleaned dataframe.

    Returns:
        A dataframe with features extracted.
    """
    logger.info('Extracting features')
    df = df.drop([target_col], axis=1)
    return df


def get_target(df: pd.DataFrame, target_col: str = 'is_canceled') -> pd.DataFrame:
    """
    Extracts target from a dataframe.

    Args:
        df (pd.DataFrame): The full cleaned dataframe.

    Returns:
        A dataframe with target extracted.
    """
    logger.info('Extracting target')
    return df[target_col]
