import os

DEBUG = True
LOGGING_CONFIG = 'config/logging/local.conf'
PORT = 5000
APP_NAME = 'hotel_bookings'
SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = '0.0.0.0'
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100

host = os.environ.get('MYSQL_HOST')
user = os.environ.get('MYSQL_USER')
password = os.environ.get('MYSQL_PASSWORD')
database = os.environ.get('DATABASE_NAME')
port = os.environ.get('MYSQL_PORT')
DIALECT ='mysql+pymysql'
HOTEL_TYPE = ['Resort Hotel', 'City Hotel']
MODEL_PATH = 'models/dt_model.pkl'


SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
if SQLALCHEMY_DATABASE_URI is None:
    if host is None:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///data/hotel_bookings.db'
    else:
        SQLALCHEMY_DATABASE_URI = '{dialect}://{user}:{pw}@{host}:{port}/{db}'.format(dialect=DIALECT,
                                                                                        user=user,
                                                                                        pw=password,host=host,
                                                                                    port=port,db=database)
