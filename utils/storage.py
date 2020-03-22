from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# For test
# argument echo would redirect all engine output to stdout
# engine = create_engine('sqlite:///db.sqlite', echo=True)

engine = create_engine('sqlite:///db.sqlite', echo=False)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
