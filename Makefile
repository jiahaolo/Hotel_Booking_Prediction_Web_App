data/hotel_bookings.csv:
	python3 run.py download_from_s3 --s3_path 's3://2022-msia423-lo-jiahao/raw/hotel_booking.csv' --local_path 'data/hotel_bookings.csv'

db:
	python3 run.py create_db

raw: data/hotel_bookings.csv

data/clean_bookings.csv: data/hotel_bookings.csv config/config.yaml
	python3 run.py model_pipeline --step clean --input 'data/sample/hotel_bookings.csv' --config=config/config.yaml --output 'data/clean_bookings.csv'

cleaned: data/clean_bookings.csv

data/X_train.csv: data/clean_bookings.csv config/config.yaml
	python3 run.py model_pipeline --step train --input 'data/clean_bookings.csv' --output 'data/X_train.csv' 'data/y_train.csv' 'data/X_test.csv' 'data/y_test.csv' 'models/dt_model.pkl'

data/y_train.csv: data/clean_bookings.csv config/config.yaml
	python3 run.py model_pipeline --step train --input 'data/clean_bookings.csv' --output 'data/X_train.csv' 'data/y_train.csv' 'data/X_test.csv' 'data/y_test.csv' 'models/dt_model.pkl'

data/X_test.csv: data/clean_bookings.csv config/config.yaml
	python3 run.py model_pipeline --step train --input 'data/clean_bookings.csv' --output 'data/X_train.csv' 'data/y_train.csv' 'data/X_test.csv' 'data/y_test.csv' 'models/dt_model.pkl'

data/y_test.csv: data/clean_bookings.csv config/config.yaml
	python3 run.py model_pipeline --step train --input 'data/clean_bookings.csv' --output 'data/X_train.csv' 'data/y_train.csv' 'data/X_test.csv' 'data/y_test.csv' 'models/dt_model.pkl'

data/performance.csv: data/y_test.csv data/y_pred.csv data/y_pred_proba.csv
	python3 run.py model_pipeline --step evaluate --input data/y_test.csv data/y_pred_proba.csv data/y_pred.csv --output data/performance.csv

metrics: data/performance.csv

models/dt_model.pkl: data/clean_bookings.csv config/config.yaml
	python3 run.py model_pipeline --step train --input 'data/clean_bookings.csv' --output 'data/X_train.csv' 'data/y_train.csv' 'data/X_test.csv' 'data/y_test.csv' 'models/dt_model.pkl'

model: models/dt_model.pkl

data/y_pred_proba.csv: data/X_test.csv models/dt_model.pkl config/config.yaml
	python3 run.py model_pipeline --step score --input data/X_test.csv models/dt_model.pkl --output data/y_pred_proba.csv data/y_pred.csv

data/y_pred.csv: data/X_test.csv models/dt_model.pkl config/config.yaml
	python3 run.py model_pipeline --step score --input data/X_test.csv models/dt_model.pkl --output data/y_pred_proba.csv data/y_pred.csv

flask: models/dt_model.pkl
	python3 app.py

tests:
	python3 -m pytest

clean:
	rm -rf data/hotel_bookings.csv data/clean_bookings.csv data/hotel_bookings.db data/X_train.csv data/y_train.csv data/X_test.csv data/y_test.csv data/y_pred_proba.csv data/y_pred.csv models/dt_model.pkl data/performance.csv

acquire: db raw

pipeline: cleaned model metrics

app: flask model

.PHONY : db raw cleaned model pipeline flask tests clean acquire app