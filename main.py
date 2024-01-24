import os
import uvicorn
from src.api.dependencies import create_db
from fastapi import FastAPI
from src.api.endpoints.authentication import router as auth_router
from src.api.endpoints.biil import router as bill_router
from src.api.endpoints.prediction import router as prediction_router
from src.api.endpoints.developer import router as dev_router
from src.exceptions_handler import app_exception_handler
from src.exceptions import AppException


app = FastAPI()

app.include_router(auth_router)
app.include_router(bill_router)
app.include_router(prediction_router)
app.include_router(dev_router)
app.add_exception_handler(AppException, app_exception_handler)

@app.on_event("startup")
async def startup_event():
    await create_db()
    
if __name__ == "__main__":

    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "7998"))

    uvicorn.run(app, host=host, port=port)
