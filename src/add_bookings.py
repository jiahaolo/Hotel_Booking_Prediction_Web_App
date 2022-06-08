"""Creates, ingests data into, and enables querying of a table of
 bookings for the hotels to query from and display results to the user."""

import logging.config
import sqlite3
import typing

import flask
import sqlalchemy
import sqlalchemy.orm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)

Base: typing.Any = declarative_base()


class Bookings(Base):
    """Creates a data model for the database to be set up for hotel bookings.
    """

    # Define the table name
    __tablename__ = "bookings"

    # Define the columns of the table
    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    hotel = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=False)
    arrival_date_day_of_month = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=False)
    arrival_date_week_number = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=False)
    reservation_day = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=False)
    reservation_month = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=False)
    reservation_weekday = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=False)
    lead_time = sqlalchemy.Column(sqlalchemy.Integer, primary_key=False)
    stays_in_week_nights = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=False)
    stays_in_weekend_nights = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=False)
    total_of_special_requests = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=False)
    market_segment = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=False)

    def __repr__(self):
        return f"<Booking {self.id}>"


class BookingManager:
    """Creates a SQLAlchemy connection to the bookings table.
    Args:
        app (:obj:`flask.app.Flask`): Flask app object for when connecting from
            within a Flask app. Optional.
        engine_string (str): SQLAlchemy engine string specifying which database
            to write to. Follows the format
    """

    def __init__(self, app: typing.Optional[flask.app.Flask] = None,
                 engine_string: typing.Optional[str] = None):
        if app:
            # If app is provided, use it to create the engine
            self.database = SQLAlchemy(app)
            self.session = self.database.session
        elif engine_string:
            # If engine_string is provided, use it to create the engine
            engine = sqlalchemy.create_engine(engine_string)
            session_maker = sqlalchemy.orm.sessionmaker(bind=engine)
            self.session = session_maker()
        else:
            raise ValueError(
                "Need either an engine string or a Flask app to initialize")

    def close(self) -> None:
        """Closes SQLAlchemy session
        Returns: None
        """
        # Close the session
        self.session.close()

    def add_booking(self, hotel: int,
                    arrival_date_day_of_month: int,
                    arrival_date_week_number: int,
                    reservation_day: int,
                    reservation_month: int,
                    reservation_weekday: int,
                    lead_time: int,
                    stays_in_week_nights: int,
                    stays_in_weekend_nights: int,
                    total_of_special_requests: int,
                    market_segment: int) -> None:
        """
        Adds a booking to the database.

        Args:

            hotel (int): The hotel number of the booking.
            arrival_date_day_of_month (int): The day of the month of the arrival
                date.
            arrival_date_week_number (int): The week number of the arrival date.
            reservation_day (int): The day of the month of the reservation.
            reservation_month (int): The month of the reservation.
            reservation_weekday (int): The weekday of the reservation.
            lead_time (int): The lead time of the booking.
            stays_in_week_nights (int): The number of nights staying in the week.
            stays_in_weekend_nights (int): The number of nights staying in the
                weekend.
            total_of_special_requests (int): The total number of special requests
                for the booking.
            market_segment (int): The market segment of the booking.

        Returns: None
        """
        try:
            # Create a new booking object
            session = self.session
            booking = Bookings(hotel=hotel,
                               arrival_date_day_of_month=arrival_date_day_of_month,
                               arrival_date_week_number=arrival_date_week_number,
                               reservation_day=reservation_day,
                               reservation_month=reservation_month,
                               reservation_weekday=reservation_weekday,
                               lead_time=lead_time,
                               stays_in_week_nights=stays_in_week_nights,
                               stays_in_weekend_nights=stays_in_weekend_nights,
                               total_of_special_requests=total_of_special_requests,
                               market_segment=market_segment)

            # Add the booking to the database
            session.add(booking)
            session.commit()
            logger.info("Booking added to database.")
        except sqlalchemy.exc.IntegrityError as e:
            logger.error("Error adding booking to database: %s", e)
            session.rollback()
        except sqlalchemy.exc.OperationalError as e:
            logger.error("Error adding booking to database: %s", e)
            session.rollback()
        except sqlite3.OperationalError as e:
            logger.error(
            "Error page returned. Not able to add booking to local sqlite database")


def create_db(engine_string: str) -> None:
    """Create database with Bookings() data model from provided engine string.
    Args:
        engine_string (str): SQLAlchemy engine string specifying which database
            to write to
    Returns: None
    """
    try:
        # Create the database
        engine = sqlalchemy.create_engine(engine_string)
        Base.metadata.create_all(engine)
        logger.info("Database created.")
    except sqlalchemy.exc.OperationalError as e:
        logger.error("Error creating database: %s", e)
    except sqlite3.OperationalError as e:
        logger.error("Error creating database: %s", e)
