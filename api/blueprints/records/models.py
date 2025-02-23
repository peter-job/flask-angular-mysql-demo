import datetime as dt

from sqlalchemy import TIMESTAMP, Column, Float, Integer, String

from api import db


class Record(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String(100), nullable=False)
    ph_level = Column(Float, nullable=False)
    turbidity = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    created_at = Column(
        TIMESTAMP, default=dt.datetime.now(dt.timezone.utc), nullable=False
    )
    updated_at = Column(TIMESTAMP, nullable=True, onupdate=dt.datetime.now)
    deleted_at = Column(TIMESTAMP, nullable=True)
