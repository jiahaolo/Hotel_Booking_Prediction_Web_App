"""Creates, ingests data into, and enables querying of a table of
 bookings for the hotels to query from and display results to the user."""

import argparse
import logging.config
import os
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

    __tablename__ = 'bookings'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    hotel = sqlalchemy.Column(sqlalchemy.String(100), unique=False,
                              nullable=False)
    lead_time = sqlalchemy.Column(sqlalchemy.Integer, primary_key=False)
    arrival_date_year = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=False)
    arrival_date_month = sqlalchemy.Column(sqlalchemy.String(100), unique=False,
                                           nullable=False)
    arrival_week_number = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=False)
    arrival_date_day_of_month = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=False)
    stays_in_weekend_nights = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=False)
    stays_in_week_nights = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=False)
    adult = sqlalchemy.Column(sqlalchemy.Integer, primary_key=False)
    children = sqlalchemy.Column(sqlalchemy.Integer, primary_key=False)
    babies = sqlalchemy.Column(sqlalchemy.Integer, primary_key=False)
    meal = sqlalchemy.Column(sqlalchemy.String(100), unique=False,
                             nullable=False)
    country = sqlalchemy.Column(sqlalchemy.String(100), unique=False,
                                nullable=False)
    market_segment = sqlalchemy.Column(sqlalchemy.String(100), unique=False,
                                       nullable=False)
    distribution_channel = sqlalchemy.Column(sqlalchemy.String(100), unique=False,
                                             nullable=False)
    is_repeated_guest = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=False)
    previous_cancellations = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=False)
    previous_bookings_not_canceled = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=False)
    reserved_room_type = sqlalchemy.Column(sqlalchemy.String(100), unique=False,
                                           nullable=False)
    assigned_room_type = sqlalchemy.Column(sqlalchemy.String(100), unique=False,
                                           nullable=False)
    booking_changes = sqlalchemy.Column(sqlalchemy.Integer, primary_key=False)
    deposit_type = sqlalchemy.Column(
        sqlalchemy.String(100), unique=False, nullable=False)
    agent = sqlalchemy.Column(sqlalchemy.String(
        100), unique=False, nullable=False)
    company = sqlalchemy.Column(sqlalchemy.String(
        100), unique=False, nullable=False)
    days_in_waiting_list = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=False)
    customer_type = sqlalchemy.Column(
        sqlalchemy.String(100), unique=False, nullable=False)
    asr = sqlalchemy.Column(sqlalchemy.Float, primary_key=False)
    required_car_parking_spaces = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=False)
    total_of_special_requests = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=False)
    reservation_status = sqlalchemy.Column(sqlalchemy.String(100), unique=False,
                                           nullable=False)
    reservation_status_date = sqlalchemy.Column(sqlalchemy.String(100), unique=False,
                                                nullable=False)

    def __repr__(self):
        return f'<Booking {self.title}>'


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
            self.database = SQLAlchemy(app)
            self.session = self.database.session
        elif engine_string:
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
        self.session.close()

    def add_booking(self, hotel: int, lead_time: int,
                    arrival_date_year: int, arrival_date_month: str, arrival_week_number: int,
                    arrival_date_day_of_month: int, stays_in_weekend_nights: int, stays_in_week_nights: int,
                    adult: int, children: int, babies: int, meal: str, country: str, market_segment: str,
                    distribution_channel: str, is_repeated_guest: str, previous_cancellations: str,
                    previous_bookings_not_canceled: str, reserved_room_type: str, assigned_room_type: str,
                    booking_changes: int, deposit_type: str, agent: str, company: str,
                    days_in_waiting_list: int, customer_type: str, asr: float,
                    required_car_parking_spaces, total_of_special_requests,
                    reservation_status, reservation_status_date) -> None:
        """Seeds an existing database with additional bookings.
        Args:
            hotel (int): Hotel ID
            lead_time (int): Lead time
            arrival_date_year (int): Arrival date year
            arrival_date_month (str): Arrival date month
            arrival_week_number (int): Arrival week number
            arrival_date_day_of_month (int): Arrival date day of month
            stays_in_weekend_nights (int): Stays in weekend nights
            stays_in_week_nights (int): Stays in week nights
            adult (int): Adult
            children (int): Children
            babies (int): Babies
            meal (str): Meal
            country (str): Country
            market_segment (str): Market segment
            distribution_channel (str): Distribution channel
            is_repeated_guest (str): Repeated guest
            previous_cancellations (str): Previous cancellations
            previous_bookings_not_canceled (str): Previous bookings not canceled
            reserved_room_type (str): Reserved room type
            assigned_room_type (str): Assigned room type
            booking_changes (int): Booking changes
            deposit_type (str): Deposit type
            agent (str): Agent
            company (str): Company
            days_in_waiting_list (int): Days in waiting list
            customer_type (str): Customer type
            asr (float): ASR
            required_car_parking_spaces (int): Required car parking spaces
            total_of_special_requests (int): Total of special requests
            reservation_status (str): Reservation status
            reservation_status_date (str): Reservation status date
        Returns: None
        """
        session = self.session
        booking = Bookings(hotel=hotel, lead_time=lead_time,
                           arrival_date_year=arrival_date_year, arrival_date_month=arrival_date_month, arrival_week_number=arrival_week_number,
                           arrival_date_day_of_month=arrival_date_day_of_month, stays_in_weekend_nights=stays_in_weekend_nights, stays_in_week_nights=stays_in_week_nights,
                           adult=adult, children=children, babies=babies, meal=meal, country=country, market_segment=market_segment,
                           distribution_channel=distribution_channel, is_repeated_guest=is_repeated_guest, previous_cancellations=previous_cancellations,
                           previous_bookings_not_canceled=previous_bookings_not_canceled, reserved_room_type=reserved_room_type, assigned_room_type=assigned_room_type,
                           booking_changes=booking_changes, deposit_type=deposit_type, agent=agent, company=company,
                           days_in_waiting_list=days_in_waiting_list, customer_type=customer_type, asr=asr,
                           required_car_parking_spaces=required_car_parking_spaces, total_of_special_requests=total_of_special_requests,
                           reservation_status=reservation_status, reservation_status_date=reservation_status_date)
        session.add(booking)
        session.commit()
        logger.info("Booking added to database.")


def create_db(engine_string: str) -> None:
    """Create database with Tracks() data model from provided engine string.
    Args:
        engine_string (str): SQLAlchemy engine string specifying which database
            to write to
    Returns: None
    """
    print(engine_string)
    engine = sqlalchemy.create_engine(engine_string)

    Base.metadata.create_all(engine)
    logger.info("Database created.")
