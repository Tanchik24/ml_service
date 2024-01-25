from fastapi import APIRouter, Depends
from src.services.user_service import UserService, user_service
from src.schemas.user import User
from src.schemas.predictor import Predictior
from src.core.security import security

router = APIRouter(prefix="/models", tags=["models"])

def get_user_service():
    return user_service


@router.get("/")
async def get_all_models(user_service: UserService = Depends(get_user_service), _: User = Depends(security.get_current_user_from_header)) -> list:
    models = await user_service.get_all_models()
    return models