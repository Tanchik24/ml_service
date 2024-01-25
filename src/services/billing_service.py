from src.exceptions import InsufficientFundsError
from src.repositories.UserRepository import user_repository

class BillingService:
    def is_enough_for_model(self, model_cost, user_cost):
        if user_cost < model_cost:
            raise InsufficientFundsError()

    async def update_balance(self, user_id, user_balance, model_cost):
        await user_repository.update(user_id, {"balance": user_balance - model_cost})

billig_service = BillingService()