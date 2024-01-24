from fastapi import APIRouter, Depends
from src.services.user_service import UserService, user_service
from src.schemas.user import User
from src.core.security import security

router = APIRouter(prefix="/bill", tags=["bill"])

def get_user_service():
    return user_service


@router.get("/balance")
async def get_balance(
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(security.get_current_user_from_header)
) -> int:
    return await user_service.check_balance(current_user)
