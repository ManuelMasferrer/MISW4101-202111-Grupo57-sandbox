from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///cuentasclaras.sqlite')
Session = sessionmaker(bind=engine)

Base = declarative_base()
session = Session()