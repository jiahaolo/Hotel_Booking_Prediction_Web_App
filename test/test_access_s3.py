"""
Unit tests for the access_s3 module.
"""

import pytest

from src.access_s3 import parse_s3

def test_parse_s3():
    """
    Happy path: Tests the parse_s3 function.
    """
    path_in = 's3://bucket/path/to/file.csv'
    bucket_true = 'bucket'
    path_true = 'path/to/file.csv'

    bucket, path = parse_s3(path_in)

    assert bucket == bucket_true
    assert path == path_true

def test_parse_s3_invalid_path():
    """
    Sad path: Tests the parse_s3 function with an invalid path.
    """
    path_in = 'saldalsd'

    with pytest.raises(AttributeError):
        parse_s3(path_in)

def test_parse_s3_none():
    """
    Sad path: Tests the parse_s3 function with None data type.
    """
    path_in = None

    with pytest.raises(TypeError):
        parse_s3(path_in)

def test_parse_s3_int():
    """
    Sad path: Tests the parse_s3 function with int data type.
    """
    path_in = 456

    with pytest.raises(TypeError):
        parse_s3(path_in)
