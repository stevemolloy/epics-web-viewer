import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import threading
from time import sleep
import initialise_db as dbc
from bpm import BPMdata

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

BPMSumAmplitude = dbc.BPMSumAmplitude
BPMSumPhase = dbc.BPMSumPhase


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


bpm = BPMdata(1)
bpm_updater = LockedDBUpdate(bpm)

while True:
    bpm_updater.get_and_commit()
    sleep(1)
