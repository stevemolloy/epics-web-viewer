import os
from sqlalchemy import ARRAY, Float, Column, Integer, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from time import sleep
from pyepics.bpm import BPMdata
import threading


Base = declarative_base()


class BPMSumSignal(Base):
    __tablename__ = 'bpm_sum_signal'
    id = Column(Integer, primary_key=True)
    signal = Column(ARRAY(Float))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


class LockedDBUpdate:
    def __init__(self, bpm):
        self.lock = threading.Lock()
        user = os.getenv('POSTGRESUSER')
        passwd = os.getenv('POSTGRESPASS')
        dbname = os.getenv('POSTGRESDBNAME')
        host = '0.0.0.0'
        port = '5432'
        engine = create_engine(f'postgresql://{user}:{passwd}@{host}:{port}/{dbname}', echo=True)

        Session = sessionmaker(bind=engine)
        self.session = Session()

        self.bpm = bpm

    def get_and_commit(self):
        with self.lock:
            try:
                self.session.add(BPMSumSignal(signal=[float(a) for a in self.bpm.sumSigAmp()]))
                self.session.commit()
            except TypeError:
                pass


if __name__ == "__main__":
    bpm = BPMdata(1)
    ldb = LockedDBUpdate(bpm)
    while True:
        ldb.get_and_commit()
        sleep(5)
