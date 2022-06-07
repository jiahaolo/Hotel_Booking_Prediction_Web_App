#!/usr/bin/env bash

# Download the data from s3
python3 run.py download_from_s3 --s3_path 's3://2022-msia423-lo-jiahao/raw/hotel_booking.csv' --local_path 'data/hotel_bookings.csv'

# Clean and generate feature
python3 run.py model_pipeline --step clean --input data/sample/hotel_bookings.csv --output data/clean_bookings.csv

# Saved split data and trained model
python3 run.py model_pipeline --step train --input data/clean_bookings.csv --output 'data/X_train.csv' 'data/y_train.csv' 'data/X_test.csv' 'data/y_test.csv' 'models/dt_model.pkl'

# Generate prediction
python3 run.py model_pipeline --step score --input 'data/X_test.csv' 'models/dt_model.pkl' --output 'data/y_pred_proba.csv' 'data/y_pred.csv'

# Compute and save metrics
python3 run.py model_pipeline --step evaluate --input 'data/y_test.csv' 'data/y_pred_proba.csv' 'data/y_pred.csv' --output data/performance.csv
