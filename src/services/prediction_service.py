from src.ml.MLModel import MLModel
import time
from src.repositories.ModelRepository import model_repository
from src.repositories.PredictionRepository import prediction_repository
from fastapi import BackgroundTasks
from redis import Redis
from src.ml.preprocess import CSVDataProcessor
from src.schemas.user import User
from src.schemas.predictor import PredictionResponse, PredictionInfo
from src.exceptions import ModelNotFoundError, JobNotFoundError, ModelStillProcessingError
import pandas as pd
import logging
from Worker import queue

redis_conn = Redis()


def handle_prediction(model_info, data_json, create_time):
    model = MLModel()
    data = pd.read_json(data_json)
    start_time = time.time()

    try:
        prediction = model.get_prediction(model_info['name'], model_info['path'], data)
        total_time = time.time() - start_time
        return {"model_info": model_info, "results": prediction, "total_time": total_time, "status": 'success', 'create_time': create_time}
    except Exception as e:
        logging.error(f"Ошибка при выполнении предсказания: {e}")
        return {"model_info": model_info, "error": str(e), "status": 'error', 'create_time': create_time}


def check_job_status(job_id):
    job = queue.fetch_job(job_id)
    while not job.is_finished and not job.is_failed:
        time.sleep(1)
        job.refresh()

    if job.is_failed:
        error_message = job.meta.get('error', 'Unknown error')
        logging.error(f"Задача {job_id} завершилась с ошибкой: {error_message}")
        prediction_repository.update(job.id, {"is_successful": False, "error": error_message})
        print('надо было и дальше учиться на биоинженера')
    else:
        print('Как тебе такое, Маск')
        duration = job.meta.get('total_time', 0)
        prediction_repository.update(job.id, {"is_successful": True, "duration": duration})
        logging.info(f"Задача {job_id} успешно завершена")

    job.save_meta()


class PredictionService:
    def __init__(self):
        self.model = MLModel()
        self.data_preprocessor = CSVDataProcessor()
        self.mapper = {1: 'GBM', 0: 'LGG'}

    async def get_model_from_db(self, model):
        model_info = await model_repository.get_by_modelname(modelname=model)
        if model_info is None:
            raise ModelNotFoundError()
        return model_info

    async def predict(self, background_tasks: BackgroundTasks, user: User, model: str, file):
        model_info = await self.get_model_from_db(model)
        data = await self.data_preprocessor.process(file)
        data_json = data.to_json()
        model_dict = {'name': model_info.modelname, 'path': model_info.file_path, 'id': model_info.id}
        create_time = time.time()
        job = queue.enqueue(handle_prediction, model_dict, data_json, create_time)
        background_tasks.add_task(check_job_status, job.id)
        prediction = PredictionInfo(id=job.id,
                                    user_id=user.id,
                                    model_id=model_info.id,
                                    cost=model_info.cost,
                                    timestamp=create_time)
        await prediction_repository.add(prediction.dict())
        return job.id

    async def get_job_status(self, job_id):
        job = queue.fetch_job(job_id)
        if not job:
            raise JobNotFoundError()

        if job.is_finished:
            latest_result = job.latest_result()
            results = latest_result.return_value
        else:
            raise ModelStillProcessingError

        pred = [self.mapper[result] for result in results['results']]

        response = PredictionResponse(
            prediction_id=job.id,
            prediction_model_id=results['model_info']['id'],
            created_at=results['create_time'],
            prediction_results=pred
        )

        return response


prediction_service = PredictionService()
