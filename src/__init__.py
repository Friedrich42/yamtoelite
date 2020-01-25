import os

import sqlalchemy as sqla
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src import conf

Base = declarative_base()
Session = sessionmaker()
db_session = Session()


def config(db_filename):
    os.makedirs(os.path.dirname(db_filename), exist_ok=True)
    open(db_filename, 'a').close()

    engine = sqla.create_engine(f'sqlite:///{db_filename}')
    Base.metadata.create_all(bind=engine)
    Session.configure(bind=engine)
    return Session()
