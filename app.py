import logging.config
import traceback
import sys

import yaml
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for

# For setting up the Flask-SQLAlchemy database session
from config.flaskconfig import HOTEL_TYPE, YAML_PATH
from src.add_bookings import BookingManager, Bookings
from src.predict import predict

# Initialize the Flask application
app = Flask(__name__, template_folder='app/templates',
            static_folder='app/static')

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config['LOGGING_CONFIG'])
logger = logging.getLogger(app.config['APP_NAME'])
logger.debug(
    'Web app should be viewable at %s:%s if docker run command maps local '
    'port to the same port as configured for the Docker container '
    'in config/flaskconfig.py (e.g. `-p 5000:5000`). Otherwise, go to the '
    'port defined on the left side of the port mapping '
    '(`i.e. -p THISPORT:5000`). If you are running from a Windows machine, '
    'go to 127.0.0.1 instead of 0.0.0.0.', app.config['HOST'], app.config['PORT'])

# Initialize the database session
booking_manager = BookingManager(app)

# Reading yaml file
logger.info('Reading configuration file')
try:
    with open(YAML_PATH, 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
except FileNotFoundError:
    logger.error('Configuration file not found')
    sys.exit(1)
except TypeError:
    logger.error('Please check the type of the object')
    sys.exit(1)
except AttributeError:
    logger.error('Please check the attribute of the object')
    sys.exit(1)
logger.info('Configuration file read')


@app.route('/', methods=['GET', 'POST'])
def index():
    '''Main view that enables user to add bookings.

    Create view into index page that user adds new bookings.

    Returns:
        Rendered html template

    '''
    if request.method == 'GET':
        try:
            logger.debug('Index page accessed')
            return render_template('index.html', hotel_type=HOTEL_TYPE)
        except Exception:
            traceback.print_exc()
            logger.warning('Hotel booking information not found.')
            return render_template('error.html')


@app.route('/predict', methods=['POST', 'GET'])
def add_entry():
    '''View that process a POST with new booking input

    Returns:
        redirect to index page
    '''

    if request.method == 'GET':
        return 'Please visit the homepage to add bookings and get predictions.'

    if request.method == 'POST':

        try:
            logger.debug(request.form['hotel_type'])
            booking_dict = {
                'hotel': request.form['hotel_type'],
                'arrival_date_day_of_month': request.form['arrival_day_of_month'],
                'arrival_date_week_number': request.form['arrival_week_number'],
                'day': request.form['reservation_day'],
                'month': request.form['reservation_month'],
                'weekday': request.form['reservation_weekday'],
                'lead_time': request.form['lead_time'],
                'stays_in_week_nights': request.form['stays_in_week_nights'],
                'stays_in_weekend_nights': request.form['stays_in_weekend_nights'],
                'total_of_special_requests': request.form['total_of_special_requests'],
                'market_segment': request.form['market_segment']
            }

            logger.debug(booking_dict)

            booking_df = pd.DataFrame(booking_dict, index=[0])
            if booking_df['hotel'][0] == 'City Hotel':
                booking_df['hotel'] = int(1)
                hotel_no = 1
            else:
                booking_df['hotel'] = int(0)
                hotel_no = 0
            prediction, prediction_prob = predict(
                booking_df, **cfg['predict']['predict'])

            logger.debug(prediction)
            logger.debug(prediction_prob)

            booking_manager.add_booking(hotel=hotel_no,
                                        arrival_date_day_of_month=request.form['arrival_day_of_month'],
                                        arrival_date_week_number=request.form['arrival_week_number'],
                                        reservation_day=request.form['reservation_day'],
                                        reservation_month=request.form['reservation_month'],
                                        reservation_weekday=request.form['reservation_weekday'],
                                        lead_time=request.form['lead_time'],
                                        stays_in_week_nights=request.form['stays_in_week_nights'],
                                        stays_in_weekend_nights=request.form['stays_in_weekend_nights'],
                                        total_of_special_requests=request.form['total_of_special_requests'],
                                        market_segment=request.form['market_segment'])
            logger.info('New booking from %s added',
                        request.form['hotel_type'])

            url_for_post = url_for(
                'response', prediction=prediction, prediction_prob=round(prediction_prob[0][1], 2))

            return redirect(url_for_post)

        except Exception:
            traceback.print_exc()
            logger.warning('Hotel booking information not found.')
            return render_template('error.html')

@app.route('/predict.html/<prediction>/<prediction_prob>', methods=['GET', 'POST'])
def response(prediction, prediction_prob):
    '''View that displays the prediction.

    Create view into index page that user adds new bookings.

    Returns:
        Rendered html template

    '''
    if request.method == 'GET':
        try:
            logger.debug('Prediction page accessed')
            res = booking_manager.session.query(Bookings)
            logger.debug(res)
            logger.debug(res.all())
            return render_template('predict.html', prediction=prediction,
                                        prediction_prob=prediction_prob, responses=res)
        except Exception:
            traceback.print_exc()
            logger.warning('Hotel booking information not found.')
            return render_template('error.html')
    elif request.method == 'POST':
        return 'POST'

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'],
            host=app.config['HOST'])
