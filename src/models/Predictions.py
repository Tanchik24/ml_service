from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BOOLEAN
from sqlalchemy.orm import relationship
from datetime import datetime
from src.api.dependencies.create_db import Base
from src.core.config import config

class Prediction(Base):
    __tablename__ = config.PREDICTIONS_DB

    id = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey(config.USER_DB + '.id'))
    model_id = Column(Integer, ForeignKey(config.MODEL_DB + '.id'))
    result = Column(String, nullable=True)
    cost = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    duration = Column(Integer, nullable=True)
    is_successful = Column(BOOLEAN, nullable=True)
