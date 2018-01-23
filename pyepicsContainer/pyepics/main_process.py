import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import threading
from time import sleep
import initialise_db as dbc
from epics import PV

user = os.getenv('POSTGRES_USER')
passwd = os.getenv('POSTGRES_PASSWORD')
dbname = os.getenv('POSTGRES_DB')
# host = '0.0.0.0'
host = 'postgres'
port = '5432'
engine = create_engine(
        f'postgresql://{user}:{passwd}@{host}:{port}/{dbname}',
        isolation_level="READ UNCOMMITTED",
        echo=True
    )

CCStrace1 = dbc.CCStrace1


class LockedDBUpdate:
    def __init__(self, process_variable):
        self.lock = threading.Lock()

        db_session = sessionmaker(bind=engine)
        self.session = db_session()

        self.pv = process_variable

    def get_and_commit(self):
        with self.lock:
            try:
                self.session.add_all([
                    CCStrace1(signal=[float(a) for a in self.pv.get() if abs(float(a))<1.0]),
                ])
                self.session.commit()
            except TypeError:
                pass


process_variable = PV('CCS1:trace1:ArrayData')
updater = LockedDBUpdate(process_variable)

while True:
    updater.get_and_commit()
    sleep(1)

