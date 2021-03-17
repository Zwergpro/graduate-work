from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from private.settings import DB_STRING

engine = create_engine(DB_STRING)
Session = sessionmaker(bind=engine)
