"""
Unit tests for the predict.py module.
"""

import pickle
import pytest

import pandas as pd
import numpy as np
from src.predict import predict

X_test = pd.DataFrame({'hotel': {0: 0},
                       'arrival_date_day_of_month': {0: 2.772588722239781},
                       'arrival_date_week_number': {0: 3.7612001156935615},
                       'day': {0: 16},
                       'month': {0: 9},
                       'weekday': {0: 2},
                       'lead_time': {0: 5.267858159063328},
                       'stays_in_week_nights': {0: 3},
                       'stays_in_weekend_nights': {0: 0},
                       'total_of_special_requests': {0: 0},
                       'market_segment': {0: 5}})

with open('models/dt_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

predict_true = model.predict(X_test)
predict_proba_true = model.predict_proba(X_test)

if predict_true == 1:
    PREDICTION_TRUE = 'Booking is likely to be cancelled'
else:
    PREDICTION_TRUE = 'Booking is likely to be confirmed'

def test_predict():
    """
    Happy path: Test the predict function.
    """
    # Make prediction
    predict_bin_out, predict_proba_out = predict(X_test, 'models/dt_model.pkl')

    assert predict_bin_out == PREDICTION_TRUE
    assert np.array_equal(predict_proba_out,predict_proba_true)

def test_predict_wrong_columns():
    """
    Sad path: Test the predict function with wrong columns.
    """
    x_test_wrong = pd.DataFrame({'htl': {0: 0},
                                 'dom': {0: 2.772588722239781},
                                 'wkno': {0: 3.7612001156935615},
                                 'dy': {0: 16},
                                 'mn': {0: 9},
                                 'wkday': {0: 2},
                                 'ld_time': {0: 5.267858159063328},
                                 'stays_in_week': {0: 3},
                                 'stays_in_weekend': {0: 0},
                                 'special_requests': {0: 0},
                                 'segment': {0: 5}})

    with pytest.raises(KeyError):
        predict(x_test_wrong, 'models/dt_model.pkl')
