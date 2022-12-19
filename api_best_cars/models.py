import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from . import db


class Cars(db.Model):
    """Описание модели автомобиля."""

    __tablename__ = "cars"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(), default=datetime.datetime.now)
    model = db.Column(db.String(50), nullable=False, unique=True)
    year = db.Column(db.Integer)
    engine = db.Column(db.String(50), nullable=False)
    max_speed_lower_limit = db.Column(db.Integer, default=None)
    max_speed_upper_limit = db.Column(db.Integer, default=None)
    released_copies = db.Column(db.String(50), default=None)
    eletric_engine_type = relationship(
        "ElectricEngine", backref="car", lazy=True, cascade="all, delete"
    )
    combustion_engine_type = relationship(
        "CombustionEngine", backref="car", lazy=True, cascade="all, delete"
    )

    def __str__(self):
        return self.model


class ElectricEngine(db.Model):
    """Характеристики электрического типа двигателя."""

    __tablename__ = "electric_engine"
    id = db.Column(db.Integer, primary_key=True)
    power_reserve = db.Column(db.String(50), default=None)
    car_id = db.Column(db.Integer, ForeignKey("cars.id"))


class CombustionEngine(db.Model):
    """Характеристики двигателя внутренего сгорания."""

    __tablename__ = "combustion_engine"
    id = db.Column(db.Integer, primary_key=True)
    horsepower = db.Column(db.Integer, default=None)
    kW = db.Column(db.Integer, default=None)
    car_id = db.Column(db.Integer, ForeignKey("cars.id"))
