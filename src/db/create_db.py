from src.db.base import engine
from src.db.models import BaseModel


if __name__ == '__main__':
    BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)
