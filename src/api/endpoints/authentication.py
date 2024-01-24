from fastapi import APIRouter, Depends
from src.schemas.auth import UserLogin, SignInResponse, UserCreate
from src.services.security_service import security_service, SecurityService

router = APIRouter(prefix="/authentication", tags=["authentication"])

def get_security_service():
    return security_service


@router.post("/signIn", response_model=SignInResponse)
async def sign_in(user_info: UserLogin, security_service: SecurityService = Depends(get_security_service)):
    response = await security_service.sign_in(user_info)
    return response


@router.post("/signUp", response_model=SignInResponse)
async def sign_up(user_info: UserCreate, security_service: SecurityService = Depends(get_security_service)) -> SignInResponse:
    response = await security_service.sign_up(user_info)
    return response
