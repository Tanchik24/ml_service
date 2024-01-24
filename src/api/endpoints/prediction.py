from fastapi import APIRouter, Depends, UploadFile, File
from src.services.user_service import UserService, user_service
from src.services.prediction_service import prediction_service, PredictionService
from src.schemas.user import User
from src.schemas.predictor import PredictionResponse
from fastapi import BackgroundTasks
from src.core.security import security

router = APIRouter(prefix="/predict", tags=["predict"])


def get_user_service():
    return user_service

def get_prediction_service():
    return prediction_service

background_tasks = BackgroundTasks()

@router.post("/job_id")
async def create_prediction_from_file(model: str,
                                      prediction_service: PredictionService = Depends(get_prediction_service),
                                      file: UploadFile = File(...),
                                      user: User = Depends(security.get_current_user_from_header)) -> str:

    return await prediction_service.predict(background_tasks=background_tasks, user=user, model=model, file=file)


@router.post("/by_id")
async def create_prediction_from_file(job_id: str,
                                      prediction_service: PredictionService = Depends(get_prediction_service),
                                      user: User = Depends(security.get_current_user_from_header)) -> PredictionResponse:

    return await prediction_service.get_job_status(job_id)