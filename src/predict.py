"""
This module contains functions used to make prediction based on the new user input.
"""
import logging
import pickle
import numpy as np



def predict(df, model_path):
    """
    Make prediction based on the new user input.
    """
    logging.info("Predicting based on the new user input")
    # Load the model
    with open(model_path, "rb") as model_file:
        model = pickle.load(model_file)
    
    # log transformation
    df['lead_time'] = df['lead_time'].apply(lambda x: np.log(int(x)+1))

    # Make prediction
    prediction_bin = model.predict(df)
    prediction_proba = model.predict_proba(df)

    if prediction_bin == 1:
        prediction = "Booking is likely to be cancelled"
    else:
        prediction = "Booking is likely to be confirmed"
    return prediction, prediction_proba
