"""
The module contains functions to access and interact with S3.
"""

import logging
import re
import typing

import boto3
import botocore


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

    try:
        matched = re.match(regex, s3_path)
        s3bucket = matched.group(1)
        s3_path = matched.group(2)
    except AttributeError as e:
        logger.error('Invalid S3 path: %s', s3_path)
        raise AttributeError from e
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
