from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.exceptions import MissingTokenException, InvalidTokenException
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
    ALGORITHM = config.ALGORITHM

    def create_access_token(self, payload: Dict) -> str:
        return jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)

    async def get_current_user_from_header(self,
                                           credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> UserDB:

        if credentials is None:
            logger.info('No authorization token provided')
            raise MissingTokenException()

        token = credentials.credentials
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            user_id = payload.get("user_id")
            username = payload.get("username")
            email = payload.get("email")

            if user_id is None:
                raise InvalidTokenException()

            user = User(id=user_id, username=username, email=email)
            return user

        except JWTError:
            raise InvalidTokenException()


security = Security()
