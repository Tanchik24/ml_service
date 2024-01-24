from src.repositories.UserRepository import user_repository
from src.schemas.user import User
from src.exceptions import UserNotFoundError
from src.schemas.predictor import Predictior
from src.repositories.ModelRepository import model_repository


class UserService:

    async def check_balance(self, user: User) -> int:
        user_info = await user_repository.get_by_username(username=user.username)
        if user_info is None:
            raise UserNotFoundError()
        return user_info.balance

    async def add_model(self, model: Predictior):
        await model_repository.add(model.dict())

user_service = UserService()