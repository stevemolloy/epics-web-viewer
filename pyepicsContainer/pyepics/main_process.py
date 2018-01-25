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

        self.pv = process_variable

    def get_and_commit(self):
        db_session = sessionmaker(bind=engine)
        self.session = db_session()

        with self.lock:
            try:
                self.session.add_all([
                    CCStrace1(signal=[float(a) for a in self.pv.get()]),
                ])
                self.session.commit()
            except TypeError:
                pass
        self.session.close()

    def keep_DBsize_sane(self):
        db_session = sessionmaker(bind=engine)
        self.session = db_session()

        with self.lock:
            num = self.session.query(CCStrace1).count()
            desc_id = self.session.query(CCStrace1).order_by(CCStrace1.id.desc()).first().id
            if num > 50:
                limit = desc_id - 25
                self.session.query(CCStrace1).filter(CCStrace1.id < limit).delete()
        self.session.close()
        print(f'num = {num}')
        print(f'desc_id = {desc_id}')


#process_variable = PV('CCS1:trace1:ArrayData')
process_variable = PV('CAM1:image1:ArrayData')
updater = LockedDBUpdate(process_variable)

while True:
    updater.get_and_commit()
    updater.keep_DBsize_sane()
    sleep(1)

