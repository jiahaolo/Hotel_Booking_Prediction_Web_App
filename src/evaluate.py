"""
Module to evaluate the decision tree model.
"""

import logging
import typing
import pickle

import pandas as pd
import sklearn.tree
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix, classification_report, f1_score
from sklearn.exceptions import NotFittedError

logger = logging.getLogger(__name__)


def score_model(x_test_path: typing.Union[str, pd.DataFrame],
                model_path: typing.Union[str, sklearn.tree.DecisionTreeClassifier],
                initial_features: typing.List[str]) -> pd.DataFrame:
    """
    Score the model.
    Args:
        x_test_path (str/pd.DataFrame): The path or dataframe of the testing features.
        model_path (str/pd.DataFrame): The path or trained model object of the trained model.
        initial_features (list): The initial features.
    Returns:
        ypred_proba_test: The predicted probabilities.
        ypred_bin_test: The predicted labels.
    """
    if isinstance(x_test_path, str):
        try:
            # Load the testing data
            logger.info("Loading the testing data from %s", x_test_path)
            x_test = pd.read_csv(x_test_path)
        except FileNotFoundError as err:
            logger.error("Error: The file %s does not exist", x_test_path)
            raise FileNotFoundError from err
    elif isinstance(x_test_path, pd.DataFrame):
        x_test = x_test_path
    else:
        raise TypeError("x_test must be a string or a pd.DataFrame")

    if isinstance(model_path, str):
        try:
            # Load the model
            logger.info("Loading the model from %s", model_path)
            with open(model_path, "rb") as file_handle:
                dtree = pickle.load(file_handle)
        except FileNotFoundError as err:
            raise FileNotFoundError("Model file not found") from err

    elif isinstance(model_path, sklearn.tree.DecisionTreeClassifier):
        dtree = model_path

    try:
        # Prediction of probabilities
        ypred_proba_test = dtree.predict_proba(x_test[initial_features])[:, 1]

        # Prediction of classes
        ypred_bin_test = dtree.predict(x_test[initial_features])

    # Catching exceptions for model's predict_proba and predict
    except KeyError as err:
        logger.error("Error: %s", err)
        raise err

    except NotFittedError as err:
        logger.error("Error: %s", err)
        raise err

    # Return the model score
    return pd.DataFrame(ypred_proba_test), pd.DataFrame(ypred_bin_test)


def evaluate_model(y_test_path: str, ypred_proba_path: str,
                   ypred_bin_path: str) -> None:
    """
    Evaluate the model.
    Args:
        y_test_path (str): The path to the testing labels.
        ypred_proba_path (str): The path to the predicted probabilities.
        ypred_bin_path (str): The path to the predicted labels.
    Returns:
        auc (float): The area under the ROC curve.
        accuracy (float): The accuracy score.
        f1_scr (float): The f1 score.
        """
    if isinstance(y_test_path, str):
        try:
            # Load the testing labels
            logger.info("Loading the testing labels from %s", y_test_path)
            y_test = pd.read_csv(y_test_path)
        except FileNotFoundError as err:
            logger.error("Error: The file %s does not exist", y_test_path)
            raise FileNotFoundError from err
    elif isinstance(y_test_path, pd.DataFrame):
        y_test = y_test_path
    else:
        raise TypeError("y_test must be a string or a pd.DataFrame")

    if isinstance(ypred_proba_path, str):
        try:
            # Load the predicted probabilities
            logger.info(
                "Loading the predicted probabilities from %s", ypred_proba_path)
            ypred_proba = pd.read_csv(ypred_proba_path)
        except FileNotFoundError as err:
            logger.error("Error: The file %s does not exist", ypred_proba_path)
            raise FileNotFoundError from err
    elif isinstance(ypred_proba_path, pd.DataFrame):
        ypred_proba = ypred_proba_path
    else:
        raise TypeError("ypred_proba must be a string or a pd.DataFrame")

    if isinstance(ypred_bin_path, str):
        try:
            # Load the predicted labels
            logger.info("Loading the predicted labels from %s", ypred_bin_path)
            ypred_bin = pd.read_csv(ypred_bin_path)
        except FileNotFoundError as err:
            logger.error("Error: The file %s does not exist", ypred_bin_path)
            raise FileNotFoundError from err
    elif isinstance(ypred_bin_path, pd.DataFrame):
        ypred_bin = ypred_bin_path
    else:
        raise TypeError("ypred_bin must be a string or a pd.DataFrame")

    try:
        auc = roc_auc_score(y_test, ypred_proba)
        accuracy = accuracy_score(y_test, ypred_bin)
        f1_scr = f1_score(y_test, ypred_bin)
        confusion = confusion_matrix(y_test, ypred_bin)
        class_report = classification_report(y_test, ypred_bin)

        logger.info("AUC on test: %f", auc)
        logger.info("Accuracy on test: %f", accuracy)
        logger.info("F1 on test: %f", f1_scr)
        logger.info(class_report)
        logger.info(pd.DataFrame(confusion,
                                 index=["Actual negative", "Actual positive"],
                                 columns=["Predicted negative", "Predicted positive"]))
        return auc, accuracy, f1_scr

    # Catch all exceptions
    except ValueError as err:
        logger.error("Error: %s", err)
        raise err
    except TypeError as err:
        logger.error("Error: %s", err)
        raise err
