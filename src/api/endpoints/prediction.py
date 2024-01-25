from fastapi import APIRouter, Depends, UploadFile, File
from src.services.user_service import user_service
from src.services.prediction_service import prediction_service, PredictionService
from src.schemas.user import User
from src.schemas.predictor import PredictionResponse
from src.core.security import security

router = APIRouter(prefix="/predict", tags=["predict"])


def get_user_service():
    return user_service


def get_prediction_service():
    return prediction_service


@router.post("/")
async def create_prediction_from_file(model: str,
                                      prediction_service: PredictionService = Depends(get_prediction_service),
                                      file: UploadFile = File(...),
                                      user: User = Depends(security.get_current_user_from_header)) -> str:
    return await prediction_service.predict(user=user, model=model, file=file)


@router.get("/byId")
async def create_prediction_from_file(job_id: str,
                                      prediction_service: PredictionService = Depends(get_prediction_service),
                                      _: User = Depends(security.get_current_user_from_header)) -> PredictionResponse:
    return await prediction_service.get_job_results(job_id)


@router.get("/allPredictions")
async def create_prediction_from_file(prediction_service: PredictionService = Depends(get_prediction_service),
                                      user: User = Depends(security.get_current_user_from_header)) -> list:
    return await prediction_service.get_user_predictions(user)