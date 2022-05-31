"""
The module contains functions to access and interact with S3.
"""

import logging
import re
import typing
import argparse

import boto3
import botocore
import pandas as pd


logger = logging.getLogger(__name__)


def parse_s3(s3_path: str) -> typing.Tuple[str, str]:
    """
    Parses the S3 path.

    Args:
        s3_path (str): The path to the S3 file.

    Returns:
        A tuple containing the bucket name and the path to the file in S3.
    """
    regex = r's3://([\w._-]+)/([\w./_-]+)'

    matched = re.match(regex, s3_path)
    s3bucket = matched.group(1)
    s3_path = matched.group(2)

    return s3bucket, s3_path

# uploading data to S3


def upload_to_s3(local_path: str, s3_path: str) -> None:
    """
    Uploads a file to S3.

    Args:
        local_path (str): The path to the local file to be uploaded.
        s3_path (str): The path to the file in S3.

    Returns:
        None.
    """
    s3bucket, s3_just_path = parse_s3(s3_path)

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(s3bucket)

    try:
        bucket.upload_file(local_path, s3_just_path)
    except botocore.exceptions.NoCredentialsError:
        logger.error(
            'Please provide AWS credentials via AWS_ACCESS_KEY_ID \
            and AWS_SECRET_ACCESS_KEY env variables.')
    else:
        logger.info('Data uploaded from %s to %s', local_path, s3_path)


def upload_to_s3_pandas(local_path: str, s3_path: str, sep: str = ';') -> None:
    """
    Uploads a file to S3.

    Args:
        local_path (str): The path to the local file to be uploaded.
        s3_path (str): The path to the file in S3.
        sep (str): The separator used in the file.

    Returns:
        None.
    """
    df = pd.read_csv(local_path, sep=sep)

    try:
        df.to_csv(s3_path, sep=sep)
    except botocore.exceptions.NoCredentialsError:
        logger.error(
            'Please provide AWS credentials via AWS_ACCESS_KEY_ID and \
                AWS_SECRET_ACCESS_KEY env variables.')
    else:
        logger.info('Data uploaded from %s to %s', local_path, s3_path)


def download_from_s3(local_path: str, s3_path: str) -> None:
    """
    Downloads a file from S3.

    Args:
        local_path (str): The path to the local file to be downloaded.
        s3_path (str): The path to the file in S3.

    Returns:
        None.
    """

    s3bucket, s3_just_path = parse_s3(s3_path)

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(s3bucket)

    try:
        bucket.download_file(s3_just_path, local_path)
    except botocore.exceptions.NoCredentialsError:
        logger.error(
            'Please provide AWS credentials via AWS_ACCESS_KEY_ID \
                and AWS_SECRET_ACCESS_KEY env variables.')
    else:
        logger.info('Data downloaded from %s to %s', s3_path, local_path)


def download_from_s3_pandas(local_path: str, s3_path: str, sep: str = ';'):
    """
    Downloads a file from S3.


    Args:
        local_path (str): _description_
        s3_path (str): _description_
        sep (str, optional): _description_. Defaults to ';'.
    """
    try:
        df = pd.read_csv(s3_path, sep=sep)
    except botocore.exceptions.NoCredentialsError:
        logger.error(
            'Please provide AWS credentials via AWS_ACCESS_KEY_ID \
                and AWS_SECRET_ACCESS_KEY env variables.')
    else:
        df.to_csv(local_path, sep=sep)
        logger.info('Data uploaded from %s to %s', local_path, s3_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sep',
                        default=';',
                        help="CSV separator if using pandas")
    parser.add_argument('--pandas', default=False, action='store_true',
                        help='If used, will load data via pandas')
    parser.add_argument('--download', default=False, action='store_true',
                        help='If used, will load data via pandas')
    parser.add_argument('--s3_path', default='s3://2022-msia423-lo-jiahao/raw/hotel_booking.csv',
                        help='If used, will load data via pandas')
    parser.add_argument('--local_path', default='data/sample/hotel_bookings.csv',
                        help='Where to load data to in S3')
    args = parser.parse_args()

    if args.download:
        if args.pandas:
            download_from_s3_pandas(args.local_path, args.s3_path, args.sep)
        else:
            download_from_s3(args.local_path, args.s3_path)
    else:
        if args.pandas:
            upload_to_s3_pandas(args.local_path, args.s3_path, args.sep)
        else:
            upload_to_s3(args.local_path, args.s3_path)
