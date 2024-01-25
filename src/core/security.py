from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.exceptions import MissingTokenException, InvalidTokenException, AccessDeniedError
from jose import jwt, JWTError
import logging
from src.models.User import UserDB
from src.core.config import config
from typing import Dict
from src.schemas.user import User

logger = logging.getLogger(__name__)


class Security:
    bearer_scheme = HTTPBearer()
    SECRET_KEY = config.SECRET_KEY
    DEVELOP_KEY = config.DEVELOP_KEY
    ALGORITHM = config.ALGORITHM

    def create_access_token(self, payload: Dict, developer: bool) -> str:
        if developer:
            KEY = self.DEVELOP_KEY
        else:
            KEY = self.SECRET_KEY
        return jwt.encode(payload, KEY, algorithm=self.ALGORITHM)

    async def get_current_user_from_header(self,
                                           credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> UserDB:

        if credentials is None:
            logger.info('Нет токена')
            raise MissingTokenException()

        token = credentials.credentials
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            user_id = payload.get("user_id")
            username = payload.get("username")
            email = payload.get("email")
            dev = payload.get('dev')

            if user_id is None:
                raise AccessDeniedError()


            user = User(id=user_id, username=username, email=email, dev=dev)
            return user

        except JWTError:
            raise InvalidTokenException()

    async def check_sccess(self, token: str = Depends(HTTPBearer())):
        print(token)
        print('ты сейчас тут')
        if token.credentials != self.DEVELOP_KEY:
            raise AccessDeniedError()


security = Security()
