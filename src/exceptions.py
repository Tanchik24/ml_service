from http import HTTPStatus


class AppException(Exception):
    def __init__(
            self,
            status_code: int,
            error_key: str,
            error_message: str = ""
    ) -> None:
        self.error_key = error_key
        self.error_message = error_message
        self.status_code = status_code
        super().__init__()


class UserNotFoundError(AppException):
    def __init__(
        self,
        status_code: int = HTTPStatus.NOT_FOUND,
        error_key: str = "user_not_found",
        error_message: str = "User is unknown"
    ):
        super().__init__(status_code, error_key, error_message)


class UserExists(AppException):
    def __init__(
        self,
        status_code: int = HTTPStatus.BAD_REQUEST,
        error_key: str = "user_exists",
        error_message: str = "User already exists"
    ):
        super().__init__(status_code, error_key, error_message)


class InvalidPassword(AppException):
    def __init__(
        self,
        status_code: int = HTTPStatus.BAD_REQUEST,
        error_key: str = "invalid_password",
        error_message: str = "Invalid password"
    ):
        super().__init__(status_code, error_key, error_message)


class MissingTokenException(AppException):
    def __init__(
        self,
        status_code: int = HTTPStatus.UNAUTHORIZED,
        error_key: str = "missing_token",
        error_message: str = "Access token missing"
    ):
        super().__init__(status_code, error_key, error_message)


class InvalidTokenException(AppException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.UNAUTHORIZED,
            error_key="invalid_token",
            error_message="Invalid token"
        )


class DataProcessingException(AppException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.BAD_REQUEST,
            error_key="data_processing_error",
            error_message="Error in data processing")


class ModelNotFoundError(AppException):
    def __init__(
        self,
        status_code: int = HTTPStatus.NOT_FOUND,
        error_key: str = "model_not_found",
        error_message: str = "Model is unknown"
    ):
        super().__init__(status_code, error_key, error_message)


class JobNotFoundError(AppException):
    def __init__(
        self,
        status_code: int = HTTPStatus.NOT_FOUND,
        error_key: str = "job_not_found",
        error_message: str = "Job is unknown"
    ):
        super().__init__(status_code, error_key, error_message)


class ModelStillProcessingError(AppException):
    def __init__(
        self,
        status_code: int = HTTPStatus.ACCEPTED,
        error_key: str = "model_still_processing",
        error_message: str = "Model is still processing the data"
    ):
        super().__init__(status_code, error_key, error_message)


class InsufficientFundsError(AppException):
    def __init__(
        self,
        status_code: int = HTTPStatus.PAYMENT_REQUIRED,
        error_key: str = "insufficient_funds",
        error_message: str = "Insufficient funds for the transaction"
    ):
        super().__init__(status_code, error_key, error_message)


class AccessDeniedError(AppException):
    def __init__(
        self,
        status_code: int = HTTPStatus.FORBIDDEN,
        error_key: str = "access_denied",
        error_message: str = "Access to the requested resource is denied"
    ):
        super().__init__(status_code, error_key, error_message)