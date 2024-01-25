from fastapi import APIRouter, Depends
from src.services.user_service import UserService, user_service
from src.schemas.user import User
from src.schemas.predictor import Predictior
from src.core.security import security
from src.exceptions import AccessDeniedError

def get_user_service():
    return user_service

def get_checker():
    return security.check_sccess

router = APIRouter(prefix="/developer", tags=["developer"])


@router.post("/model")
async def get_balance(
    modelname: str, file_path: str, cost: int,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(security.get_current_user_from_header)):
    if current_user.dev != 'True':
        raise AccessDeniedError()
    model = Predictior(modelname=modelname, file_path=file_path, cost=cost)
    await user_service.add_model(model)