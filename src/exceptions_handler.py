from fastapi.responses import JSONResponse
from src.exceptions import AppException

async def app_exception_handler(request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_key": exc.error_key,
            "error_message": exc.error_message
        },
    )