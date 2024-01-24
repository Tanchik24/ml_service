from src.repositories.Repository import Repository
from src.models.Predictions import Prediction


class PredictionRepository(Repository):
    sqlalchemy_model = Prediction

prediction_repository = PredictionRepository()