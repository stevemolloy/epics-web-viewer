import os
from sqlalchemy import ARRAY, Float, Column, Integer, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.util.queue import Empty
from time import sleep
import threading

Base = declarative_base()

user = os.getenv('POSTGRES_USER')
passwd = os.getenv('POSTGRES_PASSWORD')
dbname = os.getenv('POSTGRES_DB')
# host = '0.0.0.0'
host = 'postgres'
port = '5432'
engine = create_engine(f'postgresql://{user}:{passwd}@{host}:{port}/{dbname}', echo=True)


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
        Base.metadata.create_all(engine)
        break
    except Empty:
        sleep(2)


class LockedDBUpdate:
    def __init__(self, bpmnum):
        self.lock = threading.Lock()

        db_session = sessionmaker(bind=engine)
        self.session = db_session()

        self.bpm = bpmnum

    def get_and_commit(self):
        with self.lock:
            try:
                self.session.add_all([
                    BPMSumAmplitude(signal=[float(a) for a in self.bpm.sumSigAmp()]),
                    BPMSumPhase(signal=[float(a) for a in self.bpm.sumSigPhase()]),
                ])
                self.session.commit()
            except TypeError:
                pass


if __name__ == "__main__":
    sleep(10)
    from bpm import BPMdata
    bpm = BPMdata(1)
    ldb = LockedDBUpdate(bpm)
    while True:
        print("hello!!!")
        ldb.get_and_commit()
        sleep(5)
