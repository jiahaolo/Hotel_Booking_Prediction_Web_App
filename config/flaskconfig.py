import os

DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 5000
APP_NAME = "hotel_bookings"
SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "0.0.0.0"
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100

host = os.environ.get('MYSQL_HOST')
user = os.environ.get('MYSQL_USER')
password = os.environ.get('MYSQL_PASSWORD')
database = os.environ.get('DATABASE_NAME')
port = os.environ.get('MYSQL_PORT')


SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
if SQLALCHEMY_DATABASE_URI is None:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{pw}@{host}:{port}/{db}'.format(user=user,pw=password,host=host,port=port,db=database)
