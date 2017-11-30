import os
from sqlalchemy import ARRAY as Array, Float, Column, Integer, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from time import sleep
from pyepics.bpm import BPMdata

user = os.getenv('POSTGRESUSER')
passwd = os.getenv('POSTGRESPASS')
dbname = os.getenv('POSTGRESDBNAME')
host = '0.0.0.0'
port = '5432'
engine = create_engine(f'postgresql://{user}:{passwd}@{host}:{port}/{dbname}', echo=True)

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class BPMSumSignal(Base):
    __tablename__ = 'bpm_sum_signal'
    id = Column(Integer, primary_key=True)
    signal = Column(Array(Float))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


if __name__ == "__main__":
    bpm = BPMdata(1)
    while True:
        try:
            session.add(BPMSumSignal(signal=[float(a) for a in bpm.sumSigAmp()]))
            session.commit()
        except TypeError:
            pass
        sleep(5)
