from src.api.dependencies.create_db import Base
from sqlalchemy import Column, Integer, String
from src.core.config import config


class UserDB(Base):
    __tablename__ = config.USER_DB

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, index=True, unique=True)
    email = Column(String, unique=False)
    hashed_password = Column(String, unique=False)
    balance = Column(Integer, default=1000)
