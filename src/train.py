"""
Module to train the decision tree model.
"""
import logging
import typing
import pickle

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


logger = logging.getLogger(__name__)


def train_test_split_data(data:pd.DataFrame, target_col:str, test_size: float = 0.4,
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

    if not isinstance(data, pd.DataFrame):
        logger.error("Invalid data")
        raise TypeError("data must be a pandas DataFrame")
    if not isinstance(target_col, str):
        logger.error("Invalid target column")
        raise TypeError("target_col must be a string")

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
    except KeyError as err:
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
        dt_model = DecisionTreeClassifier(random_state=random_state)
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


def train(input_path,x_train_path, y_train_path, x_test_path, y_test_path,
            model_path, target_column,initial_features, test_size, random_state):
    """
    Train the decision tree model.

    Args:
        input_path (str): The path to the input data.
        x_train_path (str): The path to the training features.
        y_train_path (str): The path to the training labels.
        x_test_path (str): The path to the testing features.
        y_test_path (str): The path to the testing labels.
        model_path (str): The path to the model.
        target_column (str): The target column.
        initial_features (list): The initial features used to train the model.
        test_size (float): The proportion of the data to use for testing.
        random_state (int): The seed for the random number generator.
    """

    # Load the data
    logger.info("Loading the data")
    data = pd.read_csv(input_path)

    # Split the data into a training and testing set
    logger.info("Splitting data into training and testing set")
    x_train, x_test, y_train, y_test = train_test_split_data(data, target_column, test_size, random_state)

    # Train the decision tree model
    logger.info("Training the decision tree model")
    dt_model = train_dt_model(x_train, y_train, initial_features, random_state)

    # Save the model
    logger.info("Saving the model")
    with open(model_path, 'wb') as file:
        pickle.dump(dt_model, file)

    # Save the training and testing data
    logger.info("Saving the training and testing data")
    x_train.to_csv(x_train_path, index=False)
    y_train.to_csv(y_train_path, index=False)
    x_test.to_csv(x_test_path, index=False)
    y_test.to_csv(y_test_path, index=False)
