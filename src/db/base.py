from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from private.settings import DB_STRING

engine = create_engine(DB_STRING)

BaseModel = declarative_base()
Session = sessionmaker(bind=engine)
