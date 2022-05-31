"""
Module to evaluate the decision tree model.
"""

import logging
import typing
import pickle

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix, classification_report
from sklearn.exceptions import NotFittedError

logger = logging.getLogger(__name__)


def score_model(x_test: pd.DataFrame, dtree: DecisionTreeClassifier,
                initial_features: typing.List[str]) -> pd.DataFrame:
    """
    Score the model.
    Args:
        x_test (pd.DataFrame): The testing features.
        rf (DecisionTreeClassifier): The trained decision model.
        initial_features (list): The initial features used to train the model.
    Returns:
        ypred_proba_test: The predicted probabilities for the testing data.
        ypred_bin_test: The predicted labels for the testing data.
    """
    try:
        # Prediction of probabilities
        ypred_proba_test = dtree.predict_proba(x_test[initial_features])[:, 1]

        # Prediction of classes
        ypred_bin_test = dtree.predict(x_test[initial_features])

        # Return the model score
        return pd.DataFrame(ypred_proba_test), pd.DataFrame(ypred_bin_test)

    # Catching exceptions for model's predict_proba and predict
    except KeyError as err:
        logger.error("Error: %s", err)
        raise err

    except NotFittedError as err:
        logger.error("Error: %s", err)
        raise err

    except Exception as err:
        logger.error("Error: %s", err)
        raise err


def evaluate_model(y_test: pd.Series, ypred_proba_test: pd.Series,
                   ypred_bin_test: pd.Series) -> None:
    """
    Evaluate the model.
    Args:
        y_test (pd.Series): The testing labels.
        ypred_proba_test (pd.Series): The predicted probabilities.
        ypred_bin_test (pd.Series): The predicted classes.
    Returns:
        object: The model score.
    """
    try:
        auc = roc_auc_score(y_test, ypred_proba_test)
        confusion = confusion_matrix(y_test, ypred_bin_test)
        accuracy = accuracy_score(y_test, ypred_bin_test)
        class_report = classification_report(y_test, ypred_bin_test)

        logger.info("AUC on test: %f", auc)
        logger.info("Accuracy on test: %f", accuracy)
        logger.info(class_report)
        logger.info(pd.DataFrame(confusion,
                                 index=["Actual negative", "Actual positive"],
                                 columns=["Predicted negative", "Predicted positive"]))

    # Catch all exceptions
    except ValueError as err:
        logger.error("Error: %s", err)
        raise err
    except TypeError as err:
        logger.error("Error: %s", err)
        raise err
    except Exception as err:
        logger.error("Error: %s", err)
        raise err


def evaluate(x_test, ytest,dt_model_path,initial_features):
    """
    Evaluate the model.
    Args:
        x_test (pd.DataFrame): The testing features.
        ytest (pd.Series): The testing labels.
        dt_model_path (str): The path to the trained model.
    Returns:
        object: The model score.
    """
    try:
        # Load the model
        with open(dt_model_path, "rb") as file_handle:
            dtree = pickle.load(file_handle)

        # Get the model score
        ypred_proba_test, ypred_bin_test = score_model(
            x_test, dtree, initial_features)
        evaluate_model(ytest, ypred_proba_test, ypred_bin_test)

    # Catch all exceptions
    except ValueError as err:
        logger.error("Error: %s", err)
        raise err
    except TypeError as err:
        logger.error("Error: %s", err)
        raise err
    except Exception as err:
        logger.error("Error: %s", err)
        raise err
