import datetime
from datetime import timedelta

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

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


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    psw = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    owner = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.email = kwargs.get('email')
        self.psw = generate_password_hash(kwargs.get('psw'))
        self.admin = kwargs.get('admin', False)
        self.owner = kwargs.get('owner', False)

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.id,
            expires_delta=expire_delta
        )
        return token
    
    @classmethod
    def authenticate(cls, email, psw):
        user = cls.query.filter(cls.email == email).first()
        if not check_password_hash(user.psw, psw):
            raise Exception('No user with this password')
        return user
