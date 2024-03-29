from src.api.dependencies.create_db import Base
from sqlalchemy import Column, Integer, String, inspect
from src.core.config import config

class MLModel(Base):
    __tablename__ = config.MODEL_DB

    id = Column(Integer, primary_key=True, autoincrement=True)
    modelname = Column(String, index=True, unique=True)
    file_path = Column(String)
    cost = Column(Integer)

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}