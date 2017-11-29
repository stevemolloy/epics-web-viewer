import sqlalchemy
import os


def connect(user, password, db, host='localhost', port=5432):
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)
    con = sqlalchemy.create_engine(url, client_encoding='utf8')
    meta = sqlalchemy.MetaData(bind=con, reflect=True)
    return con, meta


if __name__ == "__main__":
    user = os.getenv('POSTGRESUSER')
    passwd = os.getenv('POSTGRESPASS')
    dbname = os.getenv('POSTGRESDBNAME')
    connex, metadata = connect(user=user, password=passwd, db=dbname, host='0.0.0.0')
    print(connex)
    print(metadata)
