# MSiA423 Hotel Booking Cancellation Prediction

Developer: Jia Hao Lo

## Project Charter

### Vision
The project aims to predict the cancellation of hotel booking for the hotels to carry out demand prediction, customer retention and profit maximization. The hotels can utilize the prediction to optimize their business strategies and be prepared for the upcoming cancellations. The key drivers for booking cancelation will also be identified for the hotel to understand the patterns and reasons for cancellation, and act accordingly based on the insights.

### Mission
The project will build a predictive model to predict whether a hotel booking will be cancelled based on details of the booking provided by the user, and identify key drivers of hotel booking cancellation. Different machine learning models will be compared against each other based on selected evaluation metric to select the model with best performance in predicting cancellation.

The data is extracted from Hotel Booking Demand Datasets written by Nuno Antonio, Ana de Almeida and Luis Nunes.

Source:

Nuno Antonio, Ana de Almeida, Luis Nunes,
Hotel booking demand datasets,
Data in Brief,
Volume 22,
2019,
Pages 41-49,
ISSN 2352-3409,
https://doi.org/10.1016/j.dib.2018.11.126. (https://www.sciencedirect.com/science/article/pii/S2352340918315191)


Abstract: This data article describes two datasets with hotel demand data. One of the hotels (H1) is a resort hotel and the other is a city hotel (H2). Both datasets share the same structure, with 31 variables describing the 40,060 observations of H1 and 79,330 observations of H2. Each observation represents a hotel booking. Both datasets comprehend bookings due to arrive between the 1st of July of 2015 and the 31st of August 2017, including bookings that effectively arrived and bookings that were canceled. Since this is hotel real data, all data elements pertaining hotel or costumer identification were deleted. Due to the scarcity of real business data for scientific and educational purposes, these datasets can have an important role for research and education in revenue management, machine learning, or data mining, as well as in other fields.

Extracted from:

https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand?resource=download


### Success Criteria

1. Machine Learning Performance Metric:

   F1-score will be used as the model evaluation metric. The final model with F1-score more than 0.9 on testing data will be selected for deployment.

2. Business Outcome Metric:

    * Cost reduction from optimizing wasted resources on cancelled booking

    * Revenue increment from preventing cancellation by addressing the key drivers accordingly.

## Directory Structure

```
2022-msia423-lo-jiahao-assignment1/
┃
┣ README.md                                         <- You are here
┣ app/                                              <- Directory for files required for application
┃ ┣ static/                                         <- CSS file that remains static
┃ ┗ templates/                                      <- HIML file for the application pages
┃
┣ config/                                           <- Directory for configuration files
┃ ┣ logging/                                        <- Configuration of python loggers
┃ ┣ config.yaml                                     <- Configuration of source code
┃ ┗ flaskconfig.py                                  <- Configuration for Flask
┃
┣ data/                                             <- Folder that contains data and artifacts of the project
┃ ┗ sample                                          <- Folder for original data to be uploaded to s3
┣ deliverables/                                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder
┣ dockerfiles/                                      <- Directory for all project-related Dockerfiles
┃ ┣ Dockerfile                                      <- Dockerfile for building image to execute run.py
┃ ┣ Dockerfile.app                                  <- Dockerfile for building image to execute app.py
┃ ┣ Dockerfile.make                                 <- Dockerfile for building image to run the pipeline with Makefile
┃ ┣ Dockerfile.pipeline                             <- Dockerfile for building image to run the pipeline with shell script
┃ ┗ Dockerfile.test                                 <- Dockerfile for building image to run unit tests
┃
┣ models/                                           <- Directory for trained model objects
┃
┣ src/                                              <- Source code of the project
┃ ┣ access_s3.py                                    <- Module with functions to access s3 buckets
┃ ┣ add_bookings.py                                 <- Module with function to create and interact with database
┃ ┣ clean.py                                        <- Module with functions to clean and featurize the data
┃ ┣ evaluate.py                                     <- Module with functions to create predictions and evaluate metrics of the trained model object
┃ ┣ predict.py                                      <- Module with functions to make prediction based on user's input on web app
┃ ┗ train.py                                        <- Module with functions to split data and train model
┃
┣ tests/                                            <- Files necessary for running model tests
┃ ┣ test_access_s3.py                               <- Module with test functions for access_s3.py
┃ ┣ test_clean.py                                   <- Module with test functions for clean.py
┃ ┣ test_evaluate.py                                <- Module with test functions for evaluate.py
┃ ┣ test_predict.py                                 <- Module with test functions for predict.py
┃ ┗ test_train.py                                   <- Module with test functions for train.py
┃
┣ app.py                                            <- Python code to execute the app
┣ Makefile                                          <- Makefile to simplify the running of the pipeline
┣ requirements.txt                                  <- Python package dependencies
┣ run-pipeline.sh                                   <- Shell script to simplify the running of the pipeline
┣ run-tests.sh                                      <- Shell script to simplify the running of the test
┗ run.py                                            <- Simplifies the execution of one or more of the src scripts
```

## Docker Images

### 1. Docker image for data acquisition, model pipeline, and relational data components

```
docker build -f dockerfiles/Dockerfile -t final-project .
```

### 2. Docker image for web app

```
docker build -f dockerfiles/Dockerfile.app -t final-project-app .
```

### 3. Docker image for unit testing

```
docker build -f dockerfiles/Dockerfile.test -t final-project-tests .
```

### 3. Docker image for running with whole pipeline with shell script

```
docker build -f dockerfiles/Dockerfile.pipeline -t final-project-pipeline .
```

### 3. Docker image for running with whole pipeline with Makefile

```
docker build -f dockerfiles/Dockerfile.make -t make .
```

## Configurations

### 1. AWS credentials
AWS credential is required to access S3 bucket. Please export your access key ID and secret access key into the terminal with following command.

```
EXPORT AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY"
EXPORT AWS_SECRET_ACCESS_KEY="YOUR_SECRET_KEY"
```

### 2. Database connection URL configurations
A database connection URL is required for creating a database connection for both the relational data ingestion and web app components of the project.

Please provide a SQLALCHEMY_DATABASE_URI of either of the following formats: "{dialect}://{user}:{pasword}>@{host}:{port}/{database}" or "sqlite:///data/{databasename}.db" using the following command.

```
EXPORT SQLALCHEMY_DATABASE_URI="{dialect}://{user}:{pasword}>@{host}:{port}/{database}"
```
or

```
EXPORT SQLALCHEMY_DATABASE_URI="sqlite:///data/{databasename}.db"
```


## Running Model Pipeline
### 1. Acquire your data and persist it in S3

```
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source="$(pwd)",target=/app/ trial run.py upload_to_s3 --s3_path 's3://2022-msia423-lo-jiahao/raw/hotel_booking.csv' --local_path 'data/sample/hotel_bookings.csv'
```

The users can change the `s3_path` and `local_path` to their desired path.

### 2.  Load the raw data from your S3 bucket, and then save it to the appropriate directory

```
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source="$(pwd)",target=/app/ final-project run.py download_from_s3 --s3_path 's3://2022-msia423-lo-jiahao/raw/hotel_booking.csv' --local_path 'data/hotel_bookings.csv'
```

The users can change the `s3_path` and `local_path` to their desired path.

### 3. Clean the data and generate the features

```
docker run --mount type=bind,source="$(pwd)",target=/app/ trial run.py model_pipeline --step clean --input data/sample/hotel_bookings.csv --output data/clean_bookings.csv
```

### 4. Generate the trained model object and train/test split data and save them to the appropriate directories

```
docker run --mount type=bind,source="$(pwd)",target=/app/ final-project run.py model_pipeline --step train --input data/clean_bookings.csv --output data/X_train.csv data/y_train.csv data/X_test.csv data/y_test.csv models/dt_model.pkl
```

### 5.  Score your model, i.e. to produce predictions/labels and save them to the appropriate directory

```
docker run --mount type=bind,source="$(pwd)",target=/app/ final-project run.py model_pipeline --step score --input data/X_test.csv models/dt_model.pkl --output data/y_pred_proba.csv data/y_pred.csv
```

### 6. Compute the performance metrics and save them to the appropriate directory

```
docker run --mount type=bind,source="$(pwd)",target=/app/ final-project run.py model_pipeline --step evaluate --input data/y_test.csv data/y_pred_proba.csv data/y_pred.csv --output data/performance.csv
```

### Running the entire model pipeline
```
docker run --mount type=bind,source="$(pwd)",target=/app/ final-project-pipeline run-pipeline.sh
```

## Relational data table creation and ingestion

### 1. Create your data table in a database of our choosing (configured via the environment variable SQLALCHEMY_DATABASE_URI)

```
docker run -e SQLALCHEMY_DATABASE_URI --mount type=bind,source="$(pwd)",target=/app/ final-project run.py create_db
```

## Web app
### 1. Running web app
```
docker run -p 5000:5000 msia423-flask
```

## Testing
### Runing unit tests
```
docker run final-project-tests
```

or

```
docker run --mount type=bind,source="$(pwd)",target=/app/ final-project-pipeline run-tests.sh
```


## Running each stages of the project with Makefile
### 1. Creating database and download data from S3
```
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e SQLALCHEMY_DATABASE_URI  --mount type=bind,source="$(pwd)",target=/app/ make acquire
```

### 2. Running model pipeline
```
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e SQLALCHEMY_DATABASE_URI  --mount type=bind,source="$(pwd)",target=/app/ make pipeline
```

### 3. Running web app
```
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e SQLALCHEMY_DATABASE_URI  -p 5000:5000 --mount type=bind,source="$(pwd)",target=/app/ make app
```
