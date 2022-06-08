"""
This module contains functions used to make prediction based on the new user input.
"""
import logging
import typing
import pickle
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

def predict(df:pd.DataFrame, model_path:str) -> typing.Tuple[str,float]:
    """
    Make prediction based on the new user input.

    Args:
        df (pd.DataFrame): The dataframe of the new user input.
        model_path (str): The path of the trained model.

    Returns:
        prediction(str): The prediction of the new user input.
        prediction_proba(float): The probability of the prediction.
    """
    if not isinstance(df, pd.DataFrame):
        logger.error("Invalid input data")
        raise ValueError("df must be a pandas DataFrame")

    if not isinstance(model_path, str):
        logger.error("Invalid model path")
        raise ValueError("model_path must be a string")

    try:
        logging.info("Predicting based on the new user input")
        # Load the model
        with open(model_path, "rb") as model_file:
            model = pickle.load(model_file)

        # log transformation
        df["lead_time"] = df["lead_time"].apply(lambda x: np.log(int(x)+1))

        # Make prediction
        prediction_bin = model.predict(df)
        prediction_proba = model.predict_proba(df)

        if prediction_bin == 1:
            prediction = "Booking is likely to be cancelled"
        else:
            prediction = "Booking is likely to be confirmed"
    except FileNotFoundError as e:
        logger.error("Model file not found")
        raise e
    except KeyError as e:
        logger.error("Invalid column name")
        raise e
    except ValueError as e:
        logger.error("Invalid input data")
        raise e
    return prediction, prediction_proba
