import os
from sqlalchemy import ARRAY, Float, Column, Integer, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.util.queue import Empty
from time import sleep

Base = declarative_base()

user = os.getenv('POSTGRES_USER')
passwd = os.getenv('POSTGRES_PASSWORD')
dbname = os.getenv('POSTGRES_DB')
# host = '0.0.0.0'
host = 'postgres'
port = '5432'
engine = create_engine(
        f'postgresql://{user}:{passwd}@{host}:{port}/{dbname}',
        echo=True
    )


class BPMSumAmplitude(Base):
    __tablename__ = 'bpm_sum_signal'
    id = Column(Integer, primary_key=True)
    signal = Column(ARRAY(Float))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


class BPMSumPhase(Base):
    __tablename__ = 'bpm_phase_signal'
    id = Column(Integer, primary_key=True)
    signal = Column(ARRAY(Float))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


while True:
    try:
        print(engine)
        Base.metadata.create_all(engine)
        break
    except Empty:
        sleep(2)
