"""Configures the subparsers for receiving command line arguments for each
 stage in the model pipeline and orchestrates their execution."""
import argparse
import logging.config
import sys
import pickle
import yaml
import pandas as pd


from config.flaskconfig import SQLALCHEMY_DATABASE_URI
from src.add_bookings import create_db, BookingManager
from src.access_s3 import upload_to_s3, download_from_s3
from src.clean import get_clean_data
from src.train import train_test_split_data, train
from src.evaluate import evaluate

logging.config.fileConfig("config/logging/local.conf")
logger = logging.getLogger()

if __name__ == "__main__":

    # Reading yaml file
    logger.info("Reading configuration file")
    try:
        with open("./config/config.yaml", "r") as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    except FileNotFoundError:
        logger.error("Configuration file not found")
        sys.exit(1)
    except TypeError:
        logger.error("Please check the type of the object")
        sys.exit(1)
    except AttributeError:
        logger.error("Please check the attribute of the object")
        sys.exit(1)
    logger.info("Configuration file read")

    # Add parsers for both creating a database and adding bookings to it
    parser = argparse.ArgumentParser(
        description="Running the model pipeline")
    subparsers = parser.add_subparsers(dest="subparser_name")

    # Sub-parser for creating a database
    sp_create = subparsers.add_parser("create_db",
                                      description="Create database")
    sp_create.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI for database")

    # Sub-parser for ingesting new data
    sp_ingest = subparsers.add_parser("ingest",
                                      description="Add data to database")
    sp_ingest.add_argument("--engine_string",
                           default="sqlite:///data/tracks.db",
                           help="SQLAlchemy connection URI for database")
    sp_ingest.add_argument("--hotel", default="Resort Hotel")
    sp_ingest.add_argument("--arrival_date_day_of_month", default=1)
    sp_ingest.add_argument("--arrival_date_week_number", default=1)
    sp_ingest.add_argument("--reservation_day", default=1)
    sp_ingest.add_argument("--reservation_month", default=1)
    sp_ingest.add_argument("--reservation_weekday", default=1)
    sp_ingest.add_argument("--lead_time", default=1)
    sp_ingest.add_argument("--stays_in_week_nights", default=1)
    sp_ingest.add_argument("--stays_in_weekend_nights", default=1)
    sp_ingest.add_argument("--total_of_special_requests", default=1)
    sp_ingest.add_argument("--market_segment", default=1)

    # Sub-parser for accessing s3
    sp_upload = subparsers.add_parser(
        "upload_to_s3", help="Upload raw data to s3")
    sp_upload.add_argument("--s3_path",
                           default="s3://2022-msia423-lo-jiahao/raw/hotel_booking.csv",
                           help="Path to the data in s3")
    sp_upload.add_argument("--local_path", default="data/sample/hotel_bookings.csv",
                           help="Path to the local raw data")

    # Sub-parser for downloading data from s3
    sp_upload = subparsers.add_parser(
        "download_from_s3", help="Downloading raw data from s3")
    sp_upload.add_argument("--s3_path",
                           default="s3://2022-msia423-lo-jiahao/raw/hotel_booking.csv",
                           help="Path to the data in s3")
    sp_upload.add_argument("--local_path", default="data/sample/hotel_bookings.csv",
                           help="Path to the local raw data")

    # Sub-parser for cleaning, training, and evaluate models
    sp_pipeline = subparsers.add_parser("model_pipeline",
                                        description="Acquire data, clean data, "
                                                    "featurize data, and run model-pipeline")
    sp_pipeline.add_argument("--step", help="Which step to run",
                             choices=["clean", "train", "evaluate"])
    sp_pipeline.add_argument("--input", "-i", nargs="+", default=None,
                             help="Path to input data (optional, default = None)")
    sp_pipeline.add_argument("--config", default="config/config.yaml",
                             help="Path to configuration file")
    sp_pipeline.add_argument("--output", "-o", nargs="+", default=None,
                             help="Path to save output (optional, default = None)")

    args = parser.parse_args()
    sp_used = args.subparser_name
    if sp_used == "create_db":
        print(SQLALCHEMY_DATABASE_URI)
        create_db(args.engine_string)
    elif sp_used == "ingest":
        bm = BookingManager(args.engine_string)
        bm.add_booking(args)
    elif sp_used == "upload_to_s3":
        upload_to_s3(args.local_path, args.s3_path)
    elif sp_used == "download_from_s3":
        download_from_s3(args.local_path, args.s3_path)
    elif sp_used == "model_pipeline":
        if args.step == "clean":
            get_clean_data(args.input[0], args.output[0])
        elif args.step == "train":
            train(args.input[0], args.output[0], **cfg["train"]["train"])
        elif args.step == "evaluate":
            data = pd.read_csv(args.input[0], index_col=0)
            x_train, x_test, y_train, y_test = train_test_split_data(
                data, **cfg["train"]["train_test_split_data"])
            evaluate(x_test, y_test,
                     args.input[1],  **cfg["evaluate"]["evaluate"])
    else:
        parser.print_help()
