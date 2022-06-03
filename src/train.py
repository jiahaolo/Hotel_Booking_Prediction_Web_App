"""
Module to train the decision tree model.
"""
import logging
import typing
import pickle

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression


logger = logging.getLogger(__name__)


def train_test_split_data(data:pd.DataFrame, target_col:'str', test_size: float = 0.4,
                          random_state: int = 42) -> typing.Union[pd.DataFrame, pd.Series]:
    """
    Split the data into a training and testing set.
    Args:
        data (pd.DataFrame): The data to split.
        test_size (float): The proportion of the data to use for testing.
        random_state (int): The seed for the random number generator.
    Returns:
        pd.DataFrame: The training and testing data.
    """
    # Return whole data if test_size is 0
    if test_size == 0:
        logger.info("Test size is 0, returning whole data")
        return data

    if test_size < 0 or test_size >= 1:
        logger.error("Invalid test size")
        raise ValueError("test_size must be between 0 and 1")

    try:
        features = data.drop(target_col, axis=1)
        target = data[target_col]
        # Split the data into a training and testing set
        logger.info("Splitting data into training and testing set")
        x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=test_size,
                                                            random_state=random_state)

    # Catch exceptions for train_test_split
    except ValueError as err:
        logger.error("Error: %s", err)
        raise err
    except Exception as err:
        logger.error("Error: %s", err)
        raise err

    # Return the training and testing data
    return x_train, x_test, y_train, y_test


def train_dt_model(x_train: pd.DataFrame, y_train: pd.Series,  # pylint: disable=too-many-arguments
                   initial_features: typing.List[str],
                   random_state: int = 42) -> DecisionTreeClassifier:
    """
    Train the decision tree model.
    Args:
        x_train (pd.DataFrame): The training features.
        y_train (pd.Series): The training labels.
        initial_features (list): The initial features used to train the model.
    Returns:
        object: The trained model.
    """

    # Checking xtrain and ytrain
    if not isinstance(x_train, pd.DataFrame):
        logger.error("Invalid training features")
        raise ValueError("x_train must be a pandas DataFrame")

    if not isinstance(y_train, pd.Series):
        logger.error("Invalid training labels")
        raise ValueError("y_train must be a pandas Series")

    try:
        # Train the decision tree model
        logger.info("Training the decision tree model")
        dt_model = LogisticRegression(random_state=random_state)
        logger.info("Fitting the decision tree model")
        dt_model.fit(x_train[initial_features], y_train.values.ravel())

    # Catch exceptions for training the decision tree model
    except ValueError as err:
        logger.error("Error: %s", err)
        raise err
    except KeyError as err:
        logger.error("Error: %s", err)
        raise err
    except Exception as err:
        logger.error("Error: %s", err)
        raise err

    # Return the trained model
    return dt_model


def train(input_path, output_path, target_column,initial_features, test_size, random_state):
    """
    Train the decision tree model.
    Args:
        input_path (str): The path to the input data.
        output_path (str): The path to the output data.
        target_column (str): The name of the column to predict.
        test_size (float): The proportion of the data to use for testing.
        random_state (int): The seed for the random number generator.
    """
    # Load the data
    logger.info("Loading data")
    data = pd.read_csv(input_path, index_col=0)

    # Split the data into a training and testing set
    logger.info("Splitting data into training and testing set")
    x_train, _, y_train,_ = train_test_split_data(  # pylint: disable=unbalanced-tuple-unpacking
        data, target_column, test_size, random_state)

    # Train the decision tree model
    logger.info("Training the decision tree model")
    dt_model = train_dt_model(x_train, y_train, initial_features=initial_features,
                              random_state=random_state)

    # Save the trained model
    logger.info("Saving the decision tree model")

    with open(output_path, "wb") as file_handle:
        pickle.dump(dt_model, file_handle)
