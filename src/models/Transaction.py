from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.api.dependencies.create_db import Base
from src.core.config import config

class Transaction(Base):
    __tablename__ = config.TRANSACTION_DB

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    transaction_type = Column(String)
    credits = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
